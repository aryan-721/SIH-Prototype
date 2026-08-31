from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base, SessionLocal
from app.api.endpoints import router as api_router, mock_router
from app.seed import seed_db
from app.models.models import User

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="MoSPI / NSSTA / iGOT Karmayogi AI-Enabled Skill Intelligence & Personalized Learning Platform",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes
app.include_router(api_router, prefix="/api")
app.include_router(mock_router)

@app.on_event("startup")
def startup_event():
    # Auto-seed database if empty
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        if user_count == 0:
            seed_db()
    finally:
        db.close()

@app.get("/")
def root():
    return {
        "status": "online",
        "platform": settings.PROJECT_NAME,
        "ecosystem": settings.TARGET_ECOSYSTEM,
        "demo_mode": settings.DEMO_MODE,
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
