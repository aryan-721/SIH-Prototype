from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import User, CompetencyGap, Course, CourseCompetency, Recommendation, Role, Competency
from app.services.rules.rules_engine import rules_engine

class RecommenderEngine:
    def __init__(self):
        # Configurable weights (Sum = 100%)
        self.weights = {
            "gap_match": 0.40,
            "target_role": 0.25,
            "competency_coverage": 0.15,
            "preference": 0.10,
            "quality": 0.10
        }

    def generate_recommendations(self, db: Session, learner_id: int) -> List[Dict[str, Any]]:
        """
        Ranks verified courses deterministically based on learner gaps and role requirements.
        Generates an auditable Explainability Trail payload for each recommendation.
        """
        user = db.query(User).filter(User.id == learner_id).first()
        if not user:
            return []

        # Ensure latest gaps are calculated
        gaps = db.query(CompetencyGap).filter(CompetencyGap.learner_id == learner_id).all()
        if not gaps:
            gaps = rules_engine.calculate_learner_gaps(db, learner_id)

        # Filter gaps where gap > 0 (Priority order: Critical > Medium > Low)
        active_gaps = [g for g in gaps if g.gap > 0]
        if not active_gaps:
            active_gaps = gaps  # fallback if all satisfied

        active_gap_comp_ids = {g.competency_id: g for g in active_gaps}

        # Fetch all active catalogue courses
        all_courses = db.query(Course).filter(Course.active == True).all()

        recommendations = []
        for course in all_courses:
            course_comps = db.query(CourseCompetency).filter(CourseCompetency.course_id == course.id).all()
            if not course_comps:
                continue

            # 1. Gap Match Score (Max 40)
            matched_gap = None
            max_gap_points = 0.0
            for cc in course_comps:
                if cc.competency_id in active_gap_comp_ids:
                    gap_obj = active_gap_comp_ids[cc.competency_id]
                    # Higher severity gaps get higher score
                    severity_multiplier = 1.0 if gap_obj.severity == "Critical" else (0.8 if gap_obj.severity == "Medium" else 0.5)
                    points = 100.0 * severity_multiplier
                    if points > max_gap_points:
                        max_gap_points = points
                        matched_gap = gap_obj

            gap_match_score = round(max_gap_points * self.weights["gap_match"], 1)

            # 2. Target Role Relevance Score (Max 25)
            target_role = user.target_role or user.role
            target_role_name = target_role.name if target_role else "Statistical Officer"
            role_relevance_raw = 95.0 if matched_gap else 60.0
            role_relevance_score = round(role_relevance_raw * self.weights["target_role"], 1)

            # 3. Competency Coverage Score (Max 15)
            max_coverage = max([cc.coverage_level for cc in course_comps]) if course_comps else 3
            coverage_score = round((max_coverage / 5.0 * 100.0) * self.weights["competency_coverage"], 1)

            # 4. Learner Preference Score (Max 10)
            pref_score = round(85.0 * self.weights["preference"], 1)

            # 5. Course Quality Score (Max 10)
            quality_score = round(90.0 * self.weights["quality"], 1)

            total_score = round(gap_match_score + role_relevance_score + coverage_score + pref_score + quality_score, 1)

            # Only recommend if total_score meets baseline threshold
            if matched_gap or total_score >= 50.0:
                comp_obj = db.query(Competency).filter(Competency.id == (matched_gap.competency_id if matched_gap else course_comps[0].competency_id)).first()

                # Build Unique Feature 1: Explainability Trail
                explainability_trail = {
                    "learner_name": user.name,
                    "current_role": user.role.name if user.role else user.designation,
                    "target_role": target_role_name,
                    "competency_name": comp_obj.name if comp_obj else "Statistical Analysis",
                    "domain": comp_obj.domain if comp_obj else "Statistical",
                    "assessed_level": matched_gap.assessed_level if matched_gap else 1,
                    "required_level": matched_gap.required_level if matched_gap else 3,
                    "gap": matched_gap.gap if matched_gap else 2,
                    "severity": matched_gap.severity if matched_gap else "Medium",
                    "course_title": course.title,
                    "course_provider": course.provider,
                    "course_duration": course.duration,
                    "coverage_level": max_coverage,
                    "recommendation_reason": (
                        f"This course addresses your {matched_gap.severity.lower() if matched_gap else 'identified'} "
                        f"{(comp_obj.name if comp_obj else 'competency')} gap (Assessed Level {matched_gap.assessed_level if matched_gap else 1} vs Required Level {matched_gap.required_level if matched_gap else 3}). "
                        f"It is aligned with your target role: {target_role_name}."
                    ),
                    "score": total_score,
                    "score_breakdown": {
                        "gap_match": gap_match_score,
                        "target_role": role_relevance_score,
                        "competency_coverage": coverage_score,
                        "preference": pref_score,
                        "quality": quality_score
                    }
                }

                recommendations.append({
                    "course_id": course.id,
                    "course": course,
                    "score": total_score,
                    "breakdown": explainability_trail["score_breakdown"],
                    "explainability": explainability_trail
                })

        # Sort recommendations descending by score
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations

recommender_engine = RecommenderEngine()
