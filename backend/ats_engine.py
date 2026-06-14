from rag_pipeline import RAGPipeline


class ATSEngine:
    """Orchestrates resume upload analysis through the RAG pipeline."""

    def __init__(self):
        self.pipeline = RAGPipeline()

    def analyze_resume(self, file_path: str) -> dict:
        result = self.pipeline.run_pipeline(file_path)
        return self._normalize_result(result)

    def _normalize_result(self, result: dict) -> dict:
        categories = result.get("categories", {})
        normalized_categories = {}

        for key, value in categories.items():
            if isinstance(value, dict):
                normalized_categories[key] = {
                    "score": int(value.get("score", 0)),
                    "feedback": value.get("feedback", ""),
                }

        return {
            "overall_score": int(result.get("overall_score", 0)),
            "categories": normalized_categories,
            "strengths": result.get("strengths", []),
            "improvements": result.get("improvements", []),
            "summary": result.get("summary", ""),
            "similarity_scores": result.get("similarity_scores", {}),
            "metadata": {
                "session_id": result.get("session_id"),
                "chunks_processed": result.get("chunks_processed", 0),
                "retrieval_count": result.get("retrieval_count", 0),
            },
        }
