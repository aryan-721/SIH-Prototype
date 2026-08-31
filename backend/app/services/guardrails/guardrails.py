from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.models import Course, CourseCompetency, CompetencyGap

class GuardrailsService:
    def validate_course_recommendation(self, db: Session, learner_id: int, course_id: int) -> Tuple[bool, str]:
        """
        Deterministic Guardrail:
        1. Course exists and is active.
        2. Course is mapped to a competency.
        3. Recommendation is based on a REAL skill gap for the learner.
        """
        course = db.query(Course).filter(Course.id == course_id, Course.active == True).first()
        if not course:
            return False, "Course does not exist or is inactive."

        course_comps = db.query(CourseCompetency).filter(CourseCompetency.course_id == course_id).all()
        if not course_comps:
            return False, "Course is not mapped to any official competency."

        mapped_comp_ids = {cc.competency_id for cc in course_comps}
        
        # Check learner skill gaps
        learner_gaps = db.query(CompetencyGap).filter(
            CompetencyGap.learner_id == learner_id,
            CompetencyGap.gap > 0
        ).all()
        gap_comp_ids = {g.competency_id for g in learner_gaps}

        common_comp = mapped_comp_ids.intersection(gap_comp_ids)
        if not common_comp:
            return False, "Guardrail Violation: Course is not mapped to any verified competency gap of the learner."

        return True, "Validated"

    def validate_quiz_question(self, question_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validates generated MCQ JSON schema.
        """
        required_fields = ["question", "option_a", "option_b", "option_c", "option_d", "correct_answer", "explanation"]
        for field in required_fields:
            if field not in question_data:
                return False, f"Missing required field: {field}"

        if not isinstance(question_data["correct_answer"], int) or not (0 <= question_data["correct_answer"] <= 3):
            return False, "correct_answer must be an integer index between 0 and 3."

        if len(question_data["question"].strip()) < 10:
            return False, "Question text is too short."

        return True, "Validated"

guardrails_service = GuardrailsService()
