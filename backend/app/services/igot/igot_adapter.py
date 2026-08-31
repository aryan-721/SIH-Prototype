from typing import List, Dict, Any, Optional
import httpx
from app.config import settings

class IGOTAdapter:
    def __init__(self):
        self.base_url = settings.MOCK_IGOT_BASE_URL

    def get_courses(self) -> List[Dict[str, Any]]:
        """
        Communicates through adapter interface to retrieve active courses.
        Can swap between Mock API and real iGOT Karmayogi API seamlessly.
        """
        try:
            with httpx.Client(timeout=5.0) as client:
                resp = client.get(f"{self.base_url}/courses")
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        return []

    def get_course_details(self, course_id: int) -> Optional[Dict[str, Any]]:
        try:
            with httpx.Client(timeout=5.0) as client:
                resp = client.get(f"{self.base_url}/courses/{course_id}")
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        return None

    def enroll_user(self, user_id: int, course_id: int) -> Dict[str, Any]:
        try:
            with httpx.Client(timeout=5.0) as client:
                resp = client.post(f"{self.base_url}/enrolments", json={"user_id": user_id, "course_id": course_id})
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        return {"status": "Enrolled (Offline Mode)", "user_id": user_id, "course_id": course_id}

igot_adapter = IGOTAdapter()
