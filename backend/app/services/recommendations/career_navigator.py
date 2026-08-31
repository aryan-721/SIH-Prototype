from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.models import User, Role, RoleCompetency, LearnerCompetency, Competency, Course, CourseCompetency
from app.services.rules.rules_engine import rules_engine
from app.services.recommendations.recommender_engine import recommender_engine

class CareerNavigatorService:
    def get_role_navigator_data(self, db: Session, learner_id: int, target_role_id: int) -> Dict[str, Any]:
        user = db.query(User).filter(User.id == learner_id).first()
        target_role = db.query(Role).filter(Role.id == target_role_id).first()
        current_role = user.role if user else None

        if not user or not target_role:
            return {}

        # Fetch required competencies for target role
        target_role_comps = db.query(RoleCompetency).filter(RoleCompetency.role_id == target_role_id).all()
        
        # Fetch current learner competency levels
        learner_comps = db.query(LearnerCompetency).filter(LearnerCompetency.learner_id == learner_id).all()
        assessed_map = {lc.competency_id: lc.assessed_level for lc in learner_comps}

        satisfied = []
        needs_improvement = []
        missing = []
        total_req_points = 0
        total_assessed_points = 0

        for trc in target_role_comps:
            comp = db.query(Competency).filter(Competency.id == trc.competency_id).first()
            if not comp:
                continue

            assessed_level = assessed_map.get(trc.competency_id, 0)
            required_level = trc.required_level
            gap = max(0, required_level - assessed_level)
            severity = rules_engine.classify_gap_severity(gap)

            total_req_points += required_level
            total_assessed_points += min(assessed_level, required_level)

            comp_info = {
                "competency_id": comp.id,
                "competency_name": comp.name,
                "domain": comp.domain,
                "required_level": required_level,
                "current_level": assessed_level,
                "gap": gap,
                "severity": severity,
                "priority": trc.priority
            }

            if gap == 0:
                satisfied.append(comp_info)
            elif assessed_level > 0:
                needs_improvement.append(comp_info)
            else:
                missing.append(comp_info)

        # Calculate Competency Readiness Percentage
        readiness_pct = round((total_assessed_points / total_req_points * 100.0), 1) if total_req_points > 0 else 100.0

        # Sort priority gaps
        priority_gaps = sorted(needs_improvement + missing, key=lambda x: (x["gap"], 1 if x["priority"]=="critical" else 2), reverse=True)

        # Build Sequenced Learning Path
        all_recs = recommender_engine.generate_recommendations(db, learner_id)
        
        recommended_path = []
        step_num = 1
        for gap in priority_gaps:
            # Find best matching course for this gap
            matched_rec = None
            for rec in all_recs:
                if rec["explainability"]["competency_name"] == gap["competency_name"]:
                    matched_rec = rec
                    break
            
            if matched_rec:
                course = matched_rec["course"]
                recommended_path.append({
                    "step_number": step_num,
                    "course_id": course.id,
                    "course_title": course.title,
                    "provider": course.provider,
                    "duration": course.duration,
                    "competency_addressed": gap["competency_name"],
                    "reason": (
                        f"Step {step_num}: Addresses your {gap['severity'].lower()} gap in {gap['competency_name']} "
                        f"(Assessed Level {gap['current_level']} → Target Level {gap['required_level']}) required for {target_role.name}."
                    ),
                    "prerequisites": "Basic Statistical Foundations" if step_num > 1 else None
                })
                step_num += 1

        # Append final assessment step
        recommended_path.append({
            "step_number": step_num,
            "course_id": 999,
            "course_title": f"{target_role.name} Competency Assessment & Certification",
            "provider": "NSSTA / iGOT Karmayogi Evaluation",
            "duration": "2 hours",
            "competency_addressed": f"Comprehensive {target_role.name} Readiness",
            "reason": f"Final evaluation covering all required competencies for {target_role.name} alignment.",
            "prerequisites": "Completion of prior learning path steps"
        })

        return {
            "current_role": current_role.name if current_role else user.designation,
            "target_role": target_role.name,
            "competency_readiness_pct": readiness_pct,
            "satisfied_competencies": satisfied,
            "needs_improvement": needs_improvement,
            "missing_competencies": missing,
            "priority_gaps": priority_gaps,
            "recommended_path": recommended_path
        }

career_navigator_service = CareerNavigatorService()
