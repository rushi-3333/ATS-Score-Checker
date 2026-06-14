import os
import json
import re
import time
import uuid
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from prompts import (
    ATS_KNOWLEDGE_BASE,
    ATS_ANALYSIS_PROMPT,
    RETRIEVAL_QUERIES,
)

load_dotenv(Path(__file__).parent / ".env")

VECTORSTORE_PATH = Path(__file__).parent / "vectorstore"
UPLOADS_PATH = Path(__file__).parent / "uploads"
COLLECTION_NAME = "resume_chunks"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-001")
LLM_MODEL = os.getenv("GEMINI_LLM_MODEL", "gemini-2.5-flash-lite")


class RAGPipeline:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError(
                "GOOGLE_API_KEY is missing. Copy .env.example to .env and add your Gemini API key."
            )

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL,
            google_api_key=api_key,
        )
        self.llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            google_api_key=api_key,
            temperature=0.2,
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)
        self.qdrant = QdrantClient(path=str(VECTORSTORE_PATH))
        self._ats_vector = self.embeddings.embed_query(ATS_KNOWLEDGE_BASE)

    def extract_text_from_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())
        full_text = "\n\n".join(pages).strip()
        if not full_text:
            raise ValueError("Could not extract text from PDF. The file may be scanned/image-based.")
        return full_text

    def chunk_text(self, text: str) -> list[str]:
        return self.text_splitter.split_text(text)

    def _ensure_collection(self, vector_size: int, session_id: str):
        collection = f"{COLLECTION_NAME}_{session_id}"
        if not self.qdrant.collection_exists(collection):
            self.qdrant.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
        return collection

    def embed_and_store(self, chunks: list[str], session_id: str) -> str:
        vectors = self.embeddings.embed_documents(chunks)
        if not vectors:
            raise ValueError("Failed to generate embeddings.")

        vector_size = len(vectors[0])
        collection = self._ensure_collection(vector_size, session_id)

        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": chunk, "index": idx},
            )
            for idx, (chunk, vector) in enumerate(zip(chunks, vectors))
        ]

        self.qdrant.upsert(collection_name=collection, points=points)
        return collection

    def embed_query(self, query: str) -> list[float]:
        return self.embeddings.embed_query(query)

    def cosine_similarity(self, vec_a: list[float], vec_b: list[float]) -> float:
        a = np.array(vec_a, dtype=np.float64)
        b = np.array(vec_b, dtype=np.float64)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def retrieve(self, collection: str, query: str, top_k: int = 3) -> list[dict]:
        query_vector = self.embed_query(query)
        results = self.qdrant.query_points(
            collection_name=collection,
            query=query_vector,
            limit=top_k,
        )
        return [
            {
                "text": point.payload["text"],
                "score": point.score,
            }
            for point in results.points
        ]

    def compute_ats_similarity_scores(self, resume_text: str) -> dict[str, float]:
        resume_vector = self.embed_query(resume_text[:8000])
        overall = self.cosine_similarity(resume_vector, self._ats_vector)

        category_queries = {
            "format": "resume format sections headers standard layout",
            "keywords": "skills keywords certifications technical tools",
            "experience": "work experience achievements metrics action verbs",
            "contact_education": "contact email phone education degree institution",
        }

        query_vectors = self.embeddings.embed_documents(list(category_queries.values()))
        scores = {"overall_ats_alignment": round(overall * 100, 2)}
        for (name, _), query_vector in zip(category_queries.items(), query_vectors):
            scores[name] = round(self.cosine_similarity(resume_vector, query_vector) * 100, 2)

        return scores

    def build_retrieved_context(self, collection: str) -> tuple[str, list[dict]]:
        all_results = []
        seen_texts = set()

        for query in RETRIEVAL_QUERIES:
            hits = self.retrieve(collection, query, top_k=2)
            for hit in hits:
                if hit["text"] not in seen_texts:
                    seen_texts.add(hit["text"])
                    all_results.append(hit)

        all_results.sort(key=lambda x: x["score"], reverse=True)
        top_results = all_results[:8]
        context = "\n\n---\n\n".join(
            f"[Relevance: {r['score']:.3f}]\n{r['text']}" for r in top_results
        )
        return context, top_results

    def analyze_with_llm(
        self,
        resume_text: str,
        retrieved_context: str,
        similarity_scores: dict[str, float],
    ) -> dict:
        prompt = ATS_ANALYSIS_PROMPT.format(
            ats_knowledge=ATS_KNOWLEDGE_BASE,
            retrieved_context=retrieved_context or "No chunks retrieved.",
            resume_text=resume_text[:8000],
            similarity_scores=json.dumps(similarity_scores, indent=2),
        )

        content = self._invoke_llm_with_retry(prompt)
        return self._parse_json_response(content)

    def _invoke_llm_with_retry(self, prompt: str, max_retries: int = 3) -> str:
        last_error = None
        for attempt in range(max_retries):
            try:
                response = self.llm.invoke(prompt)
                return response.content if hasattr(response, "content") else str(response)
            except Exception as exc:
                last_error = exc
                error_text = str(exc)
                if "429" not in error_text and "quota" not in error_text.lower():
                    raise
                if attempt < max_retries - 1:
                    time.sleep(35 * (attempt + 1))
                    continue
                raise ValueError(
                    "Gemini API quota exceeded. Wait 1–2 minutes and try again. "
                    "Free tier limits apply — avoid uploading repeatedly in quick succession."
                ) from exc
        raise last_error

    def _parse_json_response(self, content: str) -> dict:
        content = content.strip()
        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\n?", "", content)
            content = re.sub(r"\n?```$", "", content)

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                return json.loads(match.group())
            raise ValueError("LLM did not return valid JSON. Try again.")

    def run_pipeline(self, file_path: str) -> dict:
        session_id = str(uuid.uuid4())[:8]
        resume_text = self.extract_text_from_pdf(file_path)
        chunks = self.chunk_text(resume_text)
        collection = self.embed_and_store(chunks, session_id)
        similarity_scores = self.compute_ats_similarity_scores(resume_text)
        retrieved_context, retrieval_hits = self.build_retrieved_context(collection)
        analysis = self.analyze_with_llm(resume_text, retrieved_context, similarity_scores)

        return {
            "session_id": session_id,
            "chunks_processed": len(chunks),
            "similarity_scores": similarity_scores,
            "retrieval_count": len(retrieval_hits),
            **analysis,
        }
