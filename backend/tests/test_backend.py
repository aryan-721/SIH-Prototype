import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.models import User, Role, Competency, RoleCompetency, LearnerCompetency, Course, CourseCompetency
from app.services.rules.rules_engine import rules_engine
from app.services.recommendations.recommender_engine import recommender_engine
from app.services.guardrails.guardrails import guardrails_service

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    
    # Create test role & competencies
    role = Role(name="Statistical Officer", department="National Accounts", version="1.0")
    session.add(role)
    session.flush()

    comp_da = Competency(name="Data Analysis", domain="Technical", active=True)
    comp_st = Competency(name="Statistics", domain="Statistical", active=True)
    session.add_all([comp_da, comp_st])
    session.flush()

    # Role requirements: Data Analysis = level 3, Statistics = level 4
    session.add(RoleCompetency(role_id=role.id, competency_id=comp_da.id, required_level=3, priority="critical"))
    session.add(RoleCompetency(role_id=role.id, competency_id=comp_st.id, required_level=4, priority="high"))

    # Test user
    user = User(name="Test Official", email="test@mospi.gov.in", employee_id="TEST-001", role_id=role.id, department="Test Dept", designation="Statistical Officer")
    session.add(user)
    session.flush()

    # Assessed levels: Data Analysis = 1 (Gap = 2, Medium/Critical), Statistics = 4 (Gap = 0, Satisfied)
    session.add(LearnerCompetency(learner_id=user.id, competency_id=comp_da.id, assessed_level=1))
    session.add(LearnerCompetency(learner_id=user.id, competency_id=comp_st.id, assessed_level=4))

    # Course mapped to Data Analysis
    course = Course(external_id="TEST-COURSE-101", title="Advanced Data Analysis", provider="iGOT", active=True)
    session.add(course)
    session.flush()
    session.add(CourseCompetency(course_id=course.id, competency_id=comp_da.id, coverage_level=3))

    session.commit()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_rules_engine_gap_calculation(db):
    user = db.query(User).first()
    gaps = rules_engine.calculate_learner_gaps(db, user.id)
    assert len(gaps) == 2
    
    da_gap = next(g for g in gaps if g.competency.name == "Data Analysis")
    assert da_gap.gap == 2
    assert da_gap.severity == "Medium"
    assert da_gap.required_level == 3
    assert da_gap.assessed_level == 1

    st_gap = next(g for g in gaps if g.competency.name == "Statistics")
    assert st_gap.gap == 0
    assert st_gap.severity == "Satisfied"

def test_recommendation_scoring_and_explainability(db):
    user = db.query(User).first()
    recs = recommender_engine.generate_recommendations(db, user.id)
    assert len(recs) == 1
    
    top_rec = recs[0]
    assert top_rec["course"].title == "Advanced Data Analysis"
    assert top_rec["score"] > 70.0
    
    explain = top_rec["explainability"]
    assert explain["competency_name"] == "Data Analysis"
    assert explain["gap"] == 2
    assert "score_breakdown" in explain

def test_guardrails_validation(db):
    user = db.query(User).first()
    course = db.query(Course).first()
    rules_engine.calculate_learner_gaps(db, user.id)
    
    valid, msg = guardrails_service.validate_course_recommendation(db, user.id, course.id)
    assert valid is True
    assert msg == "Validated"
