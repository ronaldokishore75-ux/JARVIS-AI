# =========================================================
# JARVIS V4.3 - LOCAL VECTOR STORE
# =========================================================
import hashlib
import json
import math
import os


# =========================================================
# VECTOR STORE
# =========================================================

class VectorStore:


    # =====================================================
    # DOCUMENT HASH
    # =====================================================

    @staticmethod
    def document_hash(text):
        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()


    def contains_hash(self, content_hash):

        return any(
            document.get("content_hash")
            == content_hash
            for document in self.documents
        )

    def __init__(self, file_path="vector_store.json"):

        self.file_path = os.path.join(
            os.path.dirname(__file__),
            file_path
        )

        self.documents = []

        self.load()


    # =====================================================
    # ADD DOCUMENT
    # =====================================================
    # =====================================================
    # ADD DOCUMENT
    # =====================================================

    def add(
        self,
        text,
        embedding,
        metadata=None
    ):

        if not text:
            raise ValueError(
                "Document text cannot be empty."
            )

        if not embedding:
            raise ValueError(
                "Embedding cannot be empty."
            )

        content_hash = self.document_hash(
            text
        )

        if self.contains_hash(
            content_hash
        ):

            return False

        self.documents.append(
            {
                "text": text,
                "embedding": list(embedding),
                "metadata": metadata or {},
                "content_hash": content_hash,
            }
        )

        return True

    # =====================================================
    # COSINE SIMILARITY
    # =====================================================

    @staticmethod
    def cosine_similarity(
        vector_a,
        vector_b
    ):

        if len(vector_a) != len(vector_b):

            raise ValueError(
                "Vectors must have the same dimensions."
            )

        dot_product = sum(
            a * b
            for a, b in zip(
                vector_a,
                vector_b
            )
        )

        magnitude_a = math.sqrt(
            sum(
                a * a
                for a in vector_a
            )
        )

        magnitude_b = math.sqrt(
            sum(
                b * b
                for b in vector_b
            )
        )

        if magnitude_a == 0 or magnitude_b == 0:

            return 0.0

        return (
            dot_product
            / (magnitude_a * magnitude_b)
        )


    # =====================================================
    # SEARCH
    # =====================================================

    def search(
        self,
        query_embedding,
        top_k=3
    ):

        if not query_embedding:

            return []

        results = []

        for document in self.documents:

            score = self.cosine_similarity(
                query_embedding,
                document["embedding"]
            )

            results.append(
                {
                    "text": document["text"],
                    "metadata": document["metadata"],
                    "score": score,
                }
            )

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return results[:top_k]


    # =====================================================
    # SAVE
    # =====================================================

    def save(self):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.documents,
                file,
                ensure_ascii=False,
                indent=2
            )


    # =====================================================
    # LOAD
    # =====================================================

    def load(self):

        if not os.path.exists(
            self.file_path
        ):

            self.documents = []

            return

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                self.documents = json.load(
                    file
                )

        except (
            json.JSONDecodeError,
            OSError
        ):

            self.documents = []


# =========================================================
# SHARED VECTOR STORE
# =========================================================

vector_store = VectorStore()