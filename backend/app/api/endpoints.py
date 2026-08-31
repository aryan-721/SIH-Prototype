from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app.models.models import User, Role, Competency, Course, CompetencyGap, AssessmentDocument, QuizQuestion, Enrolment
from app.schemas.schemas import (
    UserOut, RoleBase, GapOut, RecommendationOut, CareerNavigatorOut,
    ChatRequest, ChatResponse, QuizGenerateResponse, AdminAnalyticsOut
)
from app.services.rules.rules_engine import rules_engine
from app.services.recommendations.recommender_engine import recommender_engine
from app.services.recommendations.career_navigator import career_navigator_service
from app.services.assistant.assistant_service import assistant_service
from app.services.assessment.quiz_generator import quiz_generator_service
from app.services.analytics.analytics_service import analytics_service
from app.services.guardrails.guardrails import guardrails_service

router = APIRouter()

# 1. Auth & Demo User
@router.get("/auth/demo-user")
def get_demo_user(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == "Ananya Sharma").first()
    if not user:
        user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="No users found in database")
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "employee_id": user.employee_id,
        "designation": user.designation,
        "department": user.department,
        "role_id": user.role_id,
        "role_name": user.role.name if user.role else "Statistical Officer",
        "target_role_id": user.target_role_id,
        "target_role_name": user.target_role.name if user.target_role else "Senior Statistical Officer"
    }

@router.get("/auth/users")
def get_auth_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "employee_id": u.employee_id,
        "designation": u.designation,
        "department": u.department,
        "role_name": u.role.name if u.role else "Statistical Officer"
    } for u in users]

@router.post("/auth/login")
def login_user(payload: Dict[str, Any], db: Session = Depends(get_db)):
    identifier = payload.get("identifier", "").strip()
    role_type = payload.get("role_type", "learner") # learner or admin

    user = None
    if identifier:
        user = db.query(User).filter(
            (User.email.ilike(identifier)) | (User.employee_id.ilike(identifier))
        ).first()

    if not user:
        # Default to Ananya Sharma for learner, or first admin user
        user = db.query(User).filter(User.name == "Ananya Sharma").first() or db.query(User).first()

    return {
        "status": "Authenticated",
        "token": "demo-jwt-token-mospi-nssta-2024",
        "role_type": role_type,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "employee_id": user.employee_id,
            "designation": user.designation,
            "department": user.department,
            "role_id": user.role_id,
            "role_name": user.role.name if user.role else "Statistical Officer",
            "target_role_id": user.target_role_id,
            "target_role_name": user.target_role.name if user.target_role else "Senior Statistical Officer"
        }
    }

# 2. Learners & Competencies
@router.get("/learners/{learner_id}", response_model=UserOut)
def get_learner(learner_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == learner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Learner not found")
    return user

@router.get("/learners/{learner_id}/gaps")
def get_learner_gaps(learner_id: int, target_role_id: int = None, db: Session = Depends(get_db)):
    gaps = rules_engine.calculate_learner_gaps(db, learner_id, target_role_id)
    res = []
    for g in gaps:
        res.append({
            "id": g.id,
            "learner_id": g.learner_id,
            "competency_id": g.competency_id,
            "competency_name": g.competency.name if g.competency else "Unknown",
            "domain": g.competency.domain if g.competency else "General",
            "required_level": g.required_level,
            "assessed_level": g.assessed_level,
            "gap": g.gap,
            "severity": g.severity,
            "rule_version": g.rule_version
        })
    return res

# 3. Recommendations & Unique Feature 1: Explainability Trail
@router.get("/recommendations/{learner_id}")
def get_recommendations(learner_id: int, db: Session = Depends(get_db)):
    recs = recommender_engine.generate_recommendations(db, learner_id)
    out = []
    for r in recs:
        c = r["course"]
        out.append({
            "id": r["course_id"],
            "learner_id": learner_id,
            "course_id": c.id,
            "course_title": c.title,
            "provider": c.provider,
            "duration": c.duration,
            "difficulty": c.difficulty,
            "score": r["score"],
            "score_breakdown": r["breakdown"],
            "explainability": r["explainability"]
        })
    return out

# 4. Unique Feature 2: Career Navigator
@router.get("/career-navigator/{learner_id}")
def get_career_navigator(learner_id: int, target_role_id: int = None, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == learner_id).first()
    target_id = target_role_id or (user.target_role_id if user else 2) or 2
    return career_navigator_service.get_role_navigator_data(db, learner_id, target_id)

# 5. Roles & Courses
@router.get("/roles")
def get_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()

@router.get("/courses")
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

# 6. AI Assistant (RAG Powered)
@router.post("/assistant/chat")
def chat_assistant(req: ChatRequest, db: Session = Depends(get_db)):
    return assistant_service.answer_query(db, req.learner_id, req.message)

# 7. Assessment Generator & Quizzes
@router.post("/assessments/upload")
async def upload_assessment_doc(
    filename: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    content_bytes = await file.read()
    extracted_text = quiz_generator_service.extract_text_from_file(filename, content_bytes)
    
    doc = AssessmentDocument(
        filename=filename,
        extracted_text=extracted_text
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {"id": doc.id, "filename": doc.filename, "text_preview": extracted_text[:200]}

@router.post("/assessments/{doc_id}/generate")
def generate_quiz(doc_id: int, db: Session = Depends(get_db)):
    questions = quiz_generator_service.generate_quiz_questions(db, doc_id)
    out_q = []
    for q in questions:
        out_q.append({
            "id": q.id,
            "assessment_document_id": q.assessment_document_id,
            "question": q.question,
            "options": [q.option_a, q.option_b, q.option_c, q.option_d],
            "correct_answer": q.correct_answer,
            "explanation": q.explanation,
            "difficulty": q.difficulty,
            "competency_name": q.competency.name if q.competency else "Statistics",
            "reviewed": q.reviewed,
            "published": q.published
        })
    return {"document_id": doc_id, "questions": out_q}

@router.get("/assessments/{doc_id}/questions")
def get_quiz_questions(doc_id: int, db: Session = Depends(get_db)):
    questions = db.query(QuizQuestion).filter(QuizQuestion.assessment_document_id == doc_id).all()
    out_q = []
    for q in questions:
        out_q.append({
            "id": q.id,
            "assessment_document_id": q.assessment_document_id,
            "question": q.question,
            "options": [q.option_a, q.option_b, q.option_c, q.option_d],
            "correct_answer": q.correct_answer,
            "explanation": q.explanation,
            "difficulty": q.difficulty,
            "competency_name": q.competency.name if q.competency else "Statistics",
            "reviewed": q.reviewed,
            "published": q.published
        })
    return out_q

@router.post("/assessments/{doc_id}/publish")
def publish_quiz(doc_id: int, db: Session = Depends(get_db)):
    db.query(QuizQuestion).filter(QuizQuestion.assessment_document_id == doc_id).update({"published": True, "reviewed": True})
    db.commit()
    return {"status": "Quiz Published"}

# 8. Admin Analytics
@router.get("/admin/analytics")
def get_admin_analytics(db: Session = Depends(get_db)):
    return analytics_service.get_admin_analytics(db)

# 9. Mock iGOT Endpoints
mock_router = APIRouter(prefix="/mock-igot")

@mock_router.get("/courses")
def mock_igot_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return [{"id": c.id, "external_id": c.external_id, "title": c.title, "provider": c.provider, "duration": c.duration} for c in courses]

@mock_router.post("/enrolments")
def mock_igot_enroll(payload: Dict[str, Any], db: Session = Depends(get_db)):
    enrolment = Enrolment(learner_id=payload["user_id"], course_id=payload["course_id"], status="Enrolled")
    db.add(enrolment)
    db.commit()
    return {"status": "Enrolled", "enrolment_id": enrolment.id}
