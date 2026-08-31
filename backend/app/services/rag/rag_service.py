import math
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import FrameworkDocument, Competency, Role, Course

class RAGService:
    def _simple_text_embedding(self, text: str) -> List[float]:
        """
        Lightweight deterministic 64-dim pseudo embedding vector for local offline fast similarity matching.
        """
        words = text.lower().split()
        vec = [0.0] * 64
        for i, word in enumerate(words):
            hash_val = sum(ord(c) for c in word)
            vec[hash_val % 64] += 1.0
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        return sum(a * b for a, b in zip(vec1, vec2))

    def retrieve_context(self, db: Session, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves grounded evidence from framework documents, role guidelines, and competencies.
        """
        query_vec = self._simple_text_embedding(query)
        docs = db.query(FrameworkDocument).all()
        
        scored_docs = []
        for doc in docs:
            doc_vec = doc.embedding or self._simple_text_embedding(doc.content)
            score = self._cosine_similarity(query_vec, doc_vec)
            
            # Boost score if keywords match
            query_lower = query.lower()
            if any(k in doc.content.lower() for k in query_lower.split() if len(k) > 3):
                score += 0.3

            scored_docs.append({
                "document": doc,
                "score": score,
                "title": doc.title,
                "clause": doc.clause or doc.source,
                "content": doc.content
            })

        scored_docs.sort(key=lambda x: x["score"], reverse=True)
        return scored_docs[:top_k]

rag_service = RAGService()
