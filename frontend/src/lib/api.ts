const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {})
    },
    ...options
  });

  if (!res.ok) {
    throw new Error(`API Error ${res.status}: ${res.statusText}`);
  }

  return res.json();
}

export const api = {
  getDemoUser: () => fetchApi<any>("/auth/demo-user"),
  getLearnerGaps: (learnerId: number, targetRoleId?: number) =>
    fetchApi<any[]>(`/learners/${learnerId}/gaps${targetRoleId ? `?target_role_id=${targetRoleId}` : ''}`),
  getRecommendations: (learnerId: number) => fetchApi<any[]>(`/recommendations/${learnerId}`),
  getCareerNavigator: (learnerId: number, targetRoleId?: number) =>
    fetchApi<any>(`/career-navigator/${learnerId}${targetRoleId ? `?target_role_id=${targetRoleId}` : ''}`),
  getRoles: () => fetchApi<any[]>("/roles"),
  getCourses: () => fetchApi<any[]>("/courses"),
  chatAssistant: (learnerId: number, message: string) =>
    fetchApi<any>("/assistant/chat", {
      method: "POST",
      body: JSON.stringify({ learner_id: learnerId, message })
    }),
  generateQuiz: (docId: number) =>
    fetchApi<any>(`/assessments/${docId}/generate`, { method: "POST" }),
  getQuizQuestions: (docId: number) => fetchApi<any[]>(`/assessments/${docId}/questions`),
  publishQuiz: (docId: number) => fetchApi<any>(`/assessments/${docId}/publish`, { method: "POST" }),
  getAdminAnalytics: () => fetchApi<any>("/admin/analytics")
};
