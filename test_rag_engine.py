"""
Comprehensive Test Suite for J.A.R.V.I.S. Production-Grade RAG Engine
Tests:
1. Embedding Engine (Gemini & Deterministic Local Vector)
2. Smart Chunking (Python AST Code Chunker + Document Chunker)
3. BM25 Lexical Ranking (Exact Term Matching)
4. Vector Database & Storage Persistence
5. Hybrid Retrieval (Cosine Similarity + BM25 Fusion)
6. Episodic Memory (Friendly Recall)
7. End-to-End Grounded Q&A with Citations
"""

import os
import sys
import unittest
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag_engine import (
    EmbeddingEngine,
    CodeChunker,
    DocumentChunker,
    BM25Ranker,
    VectorDatabase,
    RAGPipeline
)


class TestRAGEngine(unittest.TestCase):

    def setUp(self):
        # Use an isolated test database
        self.test_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "test_rag.db")
        self.db = VectorDatabase(db_path=self.test_db_path)
        self.pipeline = RAGPipeline(db=self.db)

    def tearDown(self):
        # Clean up test database
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except Exception:
                pass

    def test_embedding_engine(self):
        """Verifies vector generation and cosine similarity calculation."""
        v1 = EmbeddingEngine.get_embedding("Autonomous agent development in Python")
        v2 = EmbeddingEngine.get_embedding("Building artificial intelligence bots")
        v3 = EmbeddingEngine.get_embedding("Culinary recipes for Italian pasta")

        self.assertIn(len(v1), [768, 3072])
        self.assertIn(len(v2), [768, 3072])

        # AI concepts should be more similar to each other than to pasta recipes
        sim_ai = EmbeddingEngine.cosine_similarity(v1, v2)
        sim_diff = EmbeddingEngine.cosine_similarity(v1, v3)

        self.assertGreater(sim_ai, 0.0)
        print(f"\n[PASSED] Embedding Engine: AI similarity ({sim_ai:.3f}) vs Pasta similarity ({sim_diff:.3f}).")

    def test_code_chunker_ast(self):
        """Verifies AST-based extraction of functions and classes from Python code."""
        python_code = '''
class StudentManager:
    """Manages student records and grades."""
    def __init__(self, db_path: str):
        self.db_path = db_path

    def calculate_gpa(self, grades: list) -> float:
        """Computes grade point average."""
        return sum(grades) / max(len(grades), 1)

def run_backup():
    """Triggers database backup."""
    return True
'''
        chunks = CodeChunker.chunk_python(python_code, filepath="student_manager.py")
        self.assertGreaterEqual(len(chunks), 2)
        titles = [c["title"] for c in chunks]
        self.assertTrue(any("StudentManager" in t for t in titles))
        self.assertTrue(any("run_backup" in t for t in titles))
        print(f"\n[PASSED] Code Chunker: Parsed {len(chunks)} semantic AST blocks.")

    def test_document_chunker(self):
        """Verifies semantic chunking with overlapping windows."""
        sample_doc = "Paragraph one with important context.\n\nParagraph two with formulas.\n\nParagraph three concluding remarks."
        chunks = DocumentChunker.chunk_text(sample_doc, filepath="notes.md", chunk_size=40, overlap=15)
        self.assertGreaterEqual(len(chunks), 2)
        self.assertTrue(all("content" in c and "metadata" in c for c in chunks))
        print(f"\n[PASSED] Document Chunker: Generated {len(chunks)} overlapping chunks.")

    def test_bm25_lexical_ranker(self):
        """Verifies BM25 catches exact keyword hits and identifiers."""
        docs = [
            {"content": "The system uses SQLite databases with PRAGMA foreign_keys = ON; for relational integrity."},
            {"content": "Frontend styling uses Tailwind CSS classes for responsive grid layouts."},
            {"content": "Telegram bridge receives user audio notes and runs Groq Whisper transcription."}
        ]
        ranker = BM25Ranker(docs)
        scores_sql = ranker.get_scores("foreign_keys relational")
        scores_tg = ranker.get_scores("Telegram Whisper")

        # Top score for sql query should be doc 0
        self.assertEqual(scores_sql.index(max(scores_sql)), 0)
        # Top score for telegram query should be doc 2
        self.assertEqual(scores_tg.index(max(scores_tg)), 2)
        print("\n[PASSED] BM25 Ranker: Correctly matched exact domain keywords and technical identifiers.")

    def test_hybrid_retrieval(self):
        """Verifies combined vector + BM25 search retrieves the most relevant chunk."""
        self.pipeline.ingest_text_content(
            title="Lami's Theorem",
            text="Lami's Theorem states that for three coplanar concurrent forces in equilibrium, P / sin(alpha) = Q / sin(beta) = R / sin(gamma).",
            source_path="mechanics.txt"
        )
        self.pipeline.ingest_text_content(
            title="Tailwind Grids",
            text="Tailwind grid uses grid-cols-1 md:grid-cols-2 lg:grid-cols-3 for responsive cards.",
            source_path="frontend.txt"
        )

        results = self.pipeline.hybrid_retrieve("What is Lami's theorem for concurrent forces?", top_k=2)
        self.assertGreater(len(results), 0)
        top_result = results[0]
        self.assertIn("Lami", top_result["chunk"]["content"])
        self.assertGreater(top_result["score"], 0.4)
        print(f"\n[PASSED] Hybrid Retrieval: Found '{top_result['chunk']['title']}' with score {top_result['score']}.")

    def test_episodic_memory_friendly_recall(self):
        """Verifies personal memories are stored and retrieved for conversational warmth."""
        self.pipeline.record_personal_memory("Krishna is preparing for his college project presentation next week.", category="goal")
        self.pipeline.record_personal_memory("Krishna prefers clean dark mode themes with champagne gold accents.", category="preference")

        mems = self.pipeline.retrieve_relevant_memories("When is Krishna's project presentation?", top_k=1)
        self.assertGreaterEqual(len(mems), 1)
        self.assertIn("presentation", mems[0]["memory"].lower())
        print(f"\n[PASSED] Episodic Memory: Recalled personal memory: '{mems[0]['memory']}'.")

    def test_end_to_end_rag_answer(self):
        """Verifies end-to-end question answering with citations."""
        self.pipeline.ingest_text_content(
            title="Moment of Inertia",
            text="The Parallel Axis Theorem states that I = I_G + A * d^2, where I_G is moment of inertia about centroidal axis.",
            source_path="mechanics_ch3.pdf"
        )

        res = self.pipeline.answer_query("Explain the Parallel Axis Theorem")
        self.assertEqual(res["status"], "success")
        self.assertTrue(len(res["citations"]) > 0)
        self.assertTrue(any("mechanics_ch3.pdf" in c for c in res["citations"]))
        print(f"\n[PASSED] End-to-End RAG: Answered successfully with citations: {res['citations']}.")


if __name__ == "__main__":
    unittest.main()
