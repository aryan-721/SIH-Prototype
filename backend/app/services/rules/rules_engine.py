from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import RoleCompetency, LearnerCompetency, CompetencyGap, User, Competency
from app.config import settings

class RulesEngine:
    def __init__(self, rule_version: str = None):
        self.rule_version = rule_version or settings.RULE_ENGINE_VERSION

    def classify_gap_severity(self, gap_value: int) -> str:
        """
        Deterministic gap classification:
        gap <= 0 -> Satisfied
        gap == 1 -> Low
        gap == 2 -> Medium
        gap >= 3 -> Critical
        """
        if gap_value <= 0:
            return "Satisfied"
        elif gap_value == 1:
            return "Low"
        elif gap_value == 2:
            return "Medium"
        else:
            return "Critical"

    def calculate_learner_gaps(self, db: Session, learner_id: int, target_role_id: int = None) -> List[CompetencyGap]:
        """
        Calculates gaps against current or target role requirement.
        Stores results deterministically with rule version audit trail.
        """
        user = db.query(User).filter(User.id == learner_id).first()
        if not user:
            return []

        # Determine role to evaluate against (target role takes priority if specified)
        eval_role_id = target_role_id or user.target_role_id or user.role_id

        # Get role requirements
        role_comps = db.query(RoleCompetency).filter(RoleCompetency.role_id == eval_role_id).all()
        
        # Get current learner competency assessments
        learner_comps = db.query(LearnerCompetency).filter(LearnerCompetency.learner_id == learner_id).all()
        assessed_map = {lc.competency_id: lc.assessed_level for lc in learner_comps}

        # Clear existing calculated gaps for this learner & role run
        db.query(CompetencyGap).filter(CompetencyGap.learner_id == learner_id).delete()

        computed_gaps = []
        for rc in role_comps:
            assessed = assessed_map.get(rc.competency_id, 0) # 0 if unassessed
            gap_value = max(0, rc.required_level - assessed)
            severity = self.classify_gap_severity(gap_value)

            gap_obj = CompetencyGap(
                learner_id=learner_id,
                competency_id=rc.competency_id,
                required_level=rc.required_level,
                assessed_level=assessed,
                gap=gap_value,
                severity=severity,
                rule_version=self.rule_version
            )
            db.add(gap_obj)
            computed_gaps.append(gap_obj)

        db.commit()
        return computed_gaps

rules_engine = RulesEngine()
