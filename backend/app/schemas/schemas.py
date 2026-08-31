from pydantic import BaseModel, EmailStr
from typing import List, Optional, Any, Dict
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    name: str
    email: str
    employee_id: str
    department: str
    designation: str
    experience_years: float = 0.0

class UserCreate(UserBase):
    role_id: int
    target_role_id: Optional[int] = None

class RoleBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    department: str
    version: str = "1.0"
    active: bool = True

    class Config:
        from_attributes = True

class UserOut(UserBase):
    id: int
    role_id: int
    target_role_id: Optional[int] = None
    role: Optional[RoleBase] = None
    target_role: Optional[RoleBase] = None

    class Config:
        from_attributes = True

# Competency Schemas
class CompetencyOut(BaseModel):
    id: int
    name: str
    domain: str
    description: Optional[str] = None
    levels: Optional[Any] = None
    active: bool = True

    class Config:
        from_attributes = True

# Gap Schema
class GapOut(BaseModel):
    id: int
    learner_id: int
    competency_id: int
    competency_name: str
    domain: str
    required_level: int
    assessed_level: int
    gap: int
    severity: str
    rule_version: str

    class Config:
        from_attributes = True

# Recommendation & Explainability Trail
class ScoreBreakdown(BaseModel):
    gap_match: float
    target_role: float
    competency_coverage: float
    preference: float
    quality: float

class ExplainabilityTrail(BaseModel):
    learner_name: str
    current_role: str
    target_role: Optional[str] = None
    competency_name: str
    domain: str
    assessed_level: int
    required_level: int
    gap: int
    severity: str
    course_title: str
    course_provider: str
    course_duration: str
    coverage_level: int
    recommendation_reason: str
    score: float
    score_breakdown: ScoreBreakdown

class RecommendationOut(BaseModel):
    id: int
    learner_id: int
    course_id: int
    course_title: str
    provider: str
    duration: str
    difficulty: str
    score: float
    score_breakdown: ScoreBreakdown
    explainability: ExplainabilityTrail

# Career Navigator Schema
class PathStep(BaseModel):
    step_number: int
    course_id: int
    course_title: str
    provider: str
    duration: str
    competency_addressed: str
    reason: str
    prerequisites: Optional[str] = None

class CareerNavigatorOut(BaseModel):
    current_role: str
    target_role: str
    competency_readiness_pct: float
    satisfied_competencies: List[Dict[str, Any]]
    priority_gaps: List[Dict[str, Any]]
    missing_competencies: List[Dict[str, Any]]
    recommended_path: List[PathStep]

# Assistant Schema
class ChatRequest(BaseModel):
    learner_id: int
    message: str

class GroundedCitation(BaseModel):
    title: str
    clause_or_source: str
    content_snippet: str

class ChatResponse(BaseModel):
    answer: str
    citations: List[GroundedCitation]
    grounded: bool = True
    mode: str = "Claude API"

# Quiz Schemas
class QuizQuestionOut(BaseModel):
    id: int
    assessment_document_id: int
    question: str
    options: List[str]
    correct_answer: int
    explanation: str
    difficulty: str
    competency_name: Optional[str] = "General Statistics"
    reviewed: bool
    published: bool

class QuizGenerateResponse(BaseModel):
    document_id: int
    filename: str
    total_generated: int
    questions: List[QuizQuestionOut]

# Admin Schemas
class WorkforceHeatmapItem(BaseModel):
    role_name: str
    department: str
    statistical_avg_gap: float
    technical_avg_gap: float
    governance_avg_gap: float
    behavioural_avg_gap: float
    data_avg_gap: float
    leadership_avg_gap: float

class AdminAnalyticsOut(BaseModel):
    total_officials: int
    critical_skill_gaps: int
    courses_enrolled: int
    completion_rate_pct: float
    top_skill_gaps: List[Dict[str, Any]]
    course_demand: List[Dict[str, Any]]
    heatmap: List[WorkforceHeatmapItem]
