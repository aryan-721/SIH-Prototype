from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    employee_id = Column(String, unique=True, index=True, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    department = Column(String, nullable=False)
    designation = Column(String, nullable=False)
    experience_years = Column(Float, default=0.0)
    target_role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    role = relationship("Role", foreign_keys=[role_id])
    target_role = relationship("Role", foreign_keys=[target_role_id])
    learner_competencies = relationship("LearnerCompetency", back_populates="user", cascade="all, delete-orphan")
    gaps = relationship("CompetencyGap", back_populates="user", cascade="all, delete-orphan")
    enrolments = relationship("Enrolment", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    department = Column(String, nullable=False)
    version = Column(String, default="1.0")
    active = Column(Boolean, default=True)

    role_competencies = relationship("RoleCompetency", back_populates="role", cascade="all, delete-orphan")


class Competency(Base):
    __tablename__ = "competencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    domain = Column(String, nullable=False)  # Statistical, Technical, Digital Governance, Behavioural, Data, Leadership
    description = Column(Text, nullable=True)
    levels = Column(JSON, nullable=True)  # Description of levels 1 to 5
    active = Column(Boolean, default=True)

    role_competencies = relationship("RoleCompetency", back_populates="competency")
    learner_competencies = relationship("LearnerCompetency", back_populates="competency")
    course_competencies = relationship("CourseCompetency", back_populates="competency")


class RoleCompetency(Base):
    __tablename__ = "role_competencies"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=False)
    required_level = Column(Integer, nullable=False)  # 1 to 5
    priority = Column(String, default="medium")  # critical, high, medium, low
    framework_version = Column(String, default="1.0")

    role = relationship("Role", back_populates="role_competencies")
    competency = relationship("Competency", back_populates="role_competencies")


class LearnerCompetency(Base):
    __tablename__ = "learner_competencies"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=False)
    assessed_level = Column(Integer, nullable=False)  # 1 to 5
    assessment_source = Column(String, default="Supervisor Assessment")
    verified = Column(Boolean, default=True)
    assessment_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="learner_competencies")
    competency = relationship("Competency", back_populates="learner_competencies")


class CompetencyGap(Base):
    __tablename__ = "competency_gaps"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=False)
    required_level = Column(Integer, nullable=False)
    assessed_level = Column(Integer, nullable=False)
    gap = Column(Integer, nullable=False)
    severity = Column(String, nullable=False)  # Satisfied, Low, Medium, Critical
    rule_version = Column(String, default="1.0")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="gaps")
    competency = relationship("Competency")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    provider = Column(String, default="iGOT Karmayogi / NSSTA")
    duration = Column(String, default="10 hours")
    difficulty = Column(String, default="Intermediate")
    active = Column(Boolean, default=True)
    source = Column(String, default="iGOT")
    url = Column(String, nullable=True)

    course_competencies = relationship("CourseCompetency", back_populates="course", cascade="all, delete-orphan")


class CourseCompetency(Base):
    __tablename__ = "course_competencies"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=False)
    coverage_level = Column(Integer, default=3)  # Max level covered (1-5)

    course = relationship("Course", back_populates="course_competencies")
    competency = relationship("Competency", back_populates="course_competencies")


class Enrolment(Base):
    __tablename__ = "enrolments"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    status = Column(String, default="Enrolled")  # Enrolled, In Progress, Completed
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="enrolments")
    course = relationship("Course")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    score = Column(Float, nullable=False)
    gap_match_score = Column(Float, default=0.0)
    role_relevance_score = Column(Float, default=0.0)
    competency_coverage_score = Column(Float, default=0.0)
    preference_score = Column(Float, default=0.0)
    quality_score = Column(Float, default=0.0)
    explanation = Column(JSON, nullable=True)  # Stores Explainability Trail payload
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="recommendations")
    course = relationship("Course")


class FrameworkDocument(Base):
    __tablename__ = "framework_documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    source = Column(String, default="MoSPI NSSTA Competency Framework")
    version = Column(String, default="1.2")
    clause = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    embedding = Column(JSON, nullable=True)  # Vector representation as JSON list


class AssessmentDocument(Base):
    __tablename__ = "assessment_documents"

    id = Column(Integer, primary_key=True, index=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    filename = Column(String, nullable=False)
    extracted_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_document_id = Column(Integer, ForeignKey("assessment_documents.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=True)
    question = Column(Text, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_answer = Column(Integer, nullable=False)  # 0, 1, 2, 3
    explanation = Column(Text, nullable=False)
    difficulty = Column(String, default="Medium")
    reviewed = Column(Boolean, default=False)
    published = Column(Boolean, default=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    action = Column(String, nullable=False)
    entity = Column(String, nullable=False)
    entity_id = Column(String, nullable=True)
    metadata_json = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
