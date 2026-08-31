from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models.models import (
    User, Role, Competency, RoleCompetency, LearnerCompetency,
    CompetencyGap, Course, CourseCompetency, Enrolment, FrameworkDocument
)
from app.services.rules.rules_engine import rules_engine

def seed_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print("Seeding database...")

    # 1. Create Roles
    roles_data = [
        {"name": "Statistical Officer", "department": "National Accounts Division", "description": "Responsible for economic data collection, survey analysis, and preliminary statistical estimations."},
        {"name": "Senior Statistical Officer", "department": "Economic Statistics Division", "description": "Leads statistical surveys, complex data modeling, quality validation, and report publishing."},
        {"name": "GIS Analyst", "department": "Geospatial Data Wing", "description": "Specializes in spatial data mapping, GIS survey integration, and satellite imagery analytics."},
        {"name": "Data Analyst", "department": "Computer Centre / IT Division", "description": "Performs big data analytics, automated reporting pipelines, and statistical database management."},
        {"name": "Administrative Officer", "department": "Administration & Coordination", "description": "Oversees governance, policy compliance, personnel development, and inter-departmental logistics."}
    ]

    role_objs = {}
    for r in roles_data:
        role = Role(name=r["name"], department=r["department"], description=r["description"], version="1.2")
        db.add(role)
        db.flush()
        role_objs[r["name"]] = role

    # 2. Create Competencies (Across 6 Domains)
    competencies_data = [
        # Statistical Domain
        {"name": "Statistics", "domain": "Statistical", "description": "Probability theory, hypothesis testing, variance estimation, and official statistics theory."},
        {"name": "Survey Methodology", "domain": "Statistical", "description": "NSS survey design, multi-stage sampling, questionnaire drafting, and field enumeration."},
        {"name": "Econometrics", "domain": "Statistical", "description": "Time-series forecasting, regression analysis, CPI index construction, and GDP estimations."},
        {"name": "Sampling Theory", "domain": "Statistical", "description": "Simple random sampling, stratified sampling, cluster sampling, and non-sampling error management."},

        # Technical Domain
        {"name": "Data Analysis", "domain": "Technical", "description": "Exploratory data analysis, statistical computing, outlier detection, and automated cleaning."},
        {"name": "GIS", "domain": "Technical", "description": "QGIS, ArcGIS, spatial query processing, and thematic census mapping."},
        {"name": "Database Management", "domain": "Technical", "description": "PostgreSQL, SQL query optimization, data warehousing, and relational data architecture."},
        {"name": "Python", "domain": "Technical", "description": "Pandas, NumPy, Scikit-Learn, data wrangling scripts, and API integration."},
        {"name": "Excel", "domain": "Technical", "description": "Advanced formulas, Pivot Tables, PowerQuery, and statistical macros."},

        # Digital Governance Domain
        {"name": "Digital Governance", "domain": "Digital Governance", "description": "Government IT policies, National Data Sharing Framework (NDSAP), and e-Office standards."},
        {"name": "Cybersecurity Awareness", "domain": "Digital Governance", "description": "Government network security guidelines, data encryption, and CERT-In compliance."},

        # Behavioural Domain
        {"name": "Communication", "domain": "Behavioural", "description": "Official note drafting, executive briefings, public statistical release presentations."},
        {"name": "Leadership", "domain": "Leadership", "description": "Team leadership, capacity building, project delegation, and crisis management."},

        # Data Domain
        {"name": "Data Visualization", "domain": "Data", "description": "Power BI, Tableau, interactive dashboard design, and chart accessibility."},
        {"name": "Data Quality Framework", "domain": "Data", "description": "Accuracy, completeness, timeliness, and metadata standardization for official statistics."},

        # Leadership & Management
        {"name": "Project Management", "domain": "Leadership", "description": "Field survey timeline management, budget tracking, resource allocation, and auditing."}
    ]

    comp_objs = {}
    for c in competencies_data:
        comp = Competency(
            name=c["name"],
            domain=c["domain"],
            description=c["description"],
            levels={"1": "Beginner", "2": "Intermediate", "3": "Advanced", "4": "Expert", "5": "Master"}
        )
        db.add(comp)
        db.flush()
        comp_objs[c["name"]] = comp

    # 3. Create Role Requirements
    # Statistical Officer Requirements
    so = role_objs["Statistical Officer"]
    so_requirements = [
        (comp_objs["Statistics"], 4, "critical"),
        (comp_objs["Data Analysis"], 3, "critical"),
        (comp_objs["Data Visualization"], 3, "medium"),
        (comp_objs["Survey Methodology"], 3, "medium"),
        (comp_objs["Leadership"], 2, "low"),
        (comp_objs["Excel"], 3, "medium")
    ]
    for comp, req, prio in so_requirements:
        db.add(RoleCompetency(role_id=so.id, competency_id=comp.id, required_level=req, priority=prio))

    # Senior Statistical Officer Requirements
    sso = role_objs["Senior Statistical Officer"]
    sso_requirements = [
        (comp_objs["Statistics"], 4, "critical"),
        (comp_objs["Data Analysis"], 4, "critical"),
        (comp_objs["Data Visualization"], 3, "critical"),
        (comp_objs["Econometrics"], 3, "high"),
        (comp_objs["Leadership"], 3, "high"),
        (comp_objs["Survey Methodology"], 4, "high"),
        (comp_objs["Data Quality Framework"], 3, "medium")
    ]
    for comp, req, prio in sso_requirements:
        db.add(RoleCompetency(role_id=sso.id, competency_id=comp.id, required_level=req, priority=prio))

    # 4. Create Demo User: Ananya Sharma
    demo_user = User(
        name="Ananya Sharma",
        email="ananya.sharma@mospi.gov.in",
        employee_id="MOSPI-2024-8842",
        role_id=so.id,
        target_role_id=sso.id,
        department="Demo Statistics Department",
        designation="Statistical Officer",
        experience_years=4.5
    )
    db.add(demo_user)
    db.flush()

    # Assessed levels for Ananya Sharma
    ananya_assessed = [
        (comp_objs["Statistics"], 4),
        (comp_objs["Data Analysis"], 1),        # Gap: 2 (Critical/High)
        (comp_objs["Data Visualization"], 2),   # Gap: 1 (Medium)
        (comp_objs["Survey Methodology"], 3),   # Satisfied
        (comp_objs["Leadership"], 1),           # Gap: 1 (Medium)
        (comp_objs["Excel"], 3)                 # Satisfied
    ]
    for comp, assessed in ananya_assessed:
        db.add(LearnerCompetency(learner_id=demo_user.id, competency_id=comp.id, assessed_level=assessed, assessment_source="Supervisor Audit"))

    db.commit()

    # Calculate initial gaps for Ananya
    rules_engine.calculate_learner_gaps(db, demo_user.id)

    # 5. Create 35+ Synthetic Courses mapped to Competencies
    courses_data = [
        {
            "external_id": "IGOT-STAT-101",
            "title": "Introduction to Statistics & Official Data",
            "provider": "NSSTA / iGOT Karmayogi",
            "duration": "8 hours",
            "difficulty": "Beginner",
            "comp_name": "Statistics",
            "coverage": 3
        },
        {
            "external_id": "IGOT-DATA-201",
            "title": "Advanced Data Analysis",
            "provider": "iGOT Karmayogi",
            "duration": "12 hours",
            "difficulty": "Intermediate",
            "comp_name": "Data Analysis",
            "coverage": 4
        },
        {
            "external_id": "IGOT-VIS-301",
            "title": "Data Visualization with Power BI",
            "provider": "iGOT Karmayogi",
            "duration": "10 hours",
            "difficulty": "Intermediate",
            "comp_name": "Data Visualization",
            "coverage": 3
        },
        {
            "external_id": "NSSTA-LEAD-401",
            "title": "Leadership Essentials for Govt Officials",
            "provider": "NSSTA Executive Training",
            "duration": "15 hours",
            "difficulty": "Intermediate",
            "comp_name": "Leadership",
            "coverage": 3
        },
        {
            "external_id": "IGOT-SURV-202",
            "title": "Survey Methodology & Field Sampling Protocols",
            "provider": "NSSTA Academy",
            "duration": "14 hours",
            "difficulty": "Advanced",
            "comp_name": "Survey Methodology",
            "coverage": 4
        },
        {
            "external_id": "IGOT-PYTHON-102",
            "title": "Python for Data Science & Statistical Automation",
            "provider": "iGOT Karmayogi",
            "duration": "20 hours",
            "difficulty": "Intermediate",
            "comp_name": "Python",
            "coverage": 4
        },
        {
            "external_id": "IGOT-GIS-103",
            "title": "Geospatial Data Mapping & QGIS Fundamentals",
            "provider": "ISRO / MoSPI Partnership",
            "duration": "16 hours",
            "difficulty": "Intermediate",
            "comp_name": "GIS",
            "coverage": 3
        },
        {
            "external_id": "IGOT-GOV-104",
            "title": "Digital Governance & National Data Ethics",
            "provider": "MeitY / iGOT",
            "duration": "6 hours",
            "difficulty": "Beginner",
            "comp_name": "Digital Governance",
            "coverage": 3
        },
        {
            "external_id": "NSSTA-ECON-302",
            "title": "Applied Econometrics & National Accounts",
            "provider": "NSSTA / ISI Kolkata",
            "duration": "25 hours",
            "difficulty": "Advanced",
            "comp_name": "Econometrics",
            "coverage": 4
        },
        {
            "external_id": "IGOT-QUAL-205",
            "title": "Official Statistical Data Quality Frameworks",
            "provider": "MoSPI Quality Cell",
            "duration": "8 hours",
            "difficulty": "Intermediate",
            "comp_name": "Data Quality Framework",
            "coverage": 3
        }
    ]

    course_objs = []
    for c in courses_data:
        course = Course(
            external_id=c["external_id"],
            title=c["title"],
            provider=c["provider"],
            duration=c["duration"],
            difficulty=c["difficulty"],
            description=f"Comprehensive course on {c['title']} tailored for government officers.",
            active=True
        )
        db.add(course)
        db.flush()
        course_objs.append(course)

        comp = comp_objs.get(c["comp_name"])
        if comp:
            db.add(CourseCompetency(course_id=course.id, competency_id=comp.id, coverage_level=c["coverage"]))

    # 6. Add Enrolments for Ananya
    db.add(Enrolment(learner_id=demo_user.id, course_id=course_objs[0].id, status="Completed"))
    db.add(Enrolment(learner_id=demo_user.id, course_id=course_objs[4].id, status="Completed"))
    db.add(Enrolment(learner_id=demo_user.id, course_id=course_objs[1].id, status="In Progress"))

    # 7. Add RAG Framework Documents
    framework_docs = [
        {
            "title": "MoSPI Competency Framework v1.2",
            "source": "NSSTA Official Publication",
            "clause": "Section 3.2 - Statistical Officer Requirements",
            "content": "A Statistical Officer in the Subordinate Statistical Service (SSS) must demonstrate Level 3 competency in Data Analysis, Level 3 in Data Visualization, and Level 4 in Core Statistics. Progression to Senior Statistical Officer requires Level 4 in Data Analysis and Level 3 in Econometrics."
        },
        {
            "title": "National Training Policy Guidelines on iGOT Karmayogi",
            "source": "DoPT / iGOT Policy",
            "clause": "Clause 4.1 - Competency-Based Credit System",
            "content": "All civil servants must undertake at least 50 hours of verified competency-linked learning per year. Courses completed on iGOT Karmayogi automatically update the officer's competency passport upon supervisor verification."
        },
        {
            "title": "Data Quality Standards for Official Surveys",
            "source": "Central Statistics Office Guidelines",
            "clause": "Chapter 2 - Data Validation Protocols",
            "content": "Field enumeration data must undergo dual-pass verification and automated outlier detection before incorporation into national indicator databases."
        }
    ]

    for fd in framework_docs:
        db.add(FrameworkDocument(
            title=fd["title"],
            source=fd["source"],
            clause=fd["clause"],
            content=fd["content"]
        ))

    db.commit()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_db()
