# =========================================================
# JARVIS V4.1 - EMBEDDINGS
# =========================================================

import os

from dotenv import load_dotenv
from google import genai


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

env_path = os.path.join(
    os.path.dirname(__file__),
    ".env"
)

load_dotenv(env_path)

api_key = os.getenv(
    "GEMINI_API_KEY"
)

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY was not found in .env"
    )


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=api_key
)


# =========================================================
# EMBEDDING MODEL
# =========================================================

EMBEDDING_MODEL = "gemini-embedding-001"


# =========================================================
# EMBED ONE TEXT
# =========================================================

def embed_text(text):

    if not text or not text.strip():

        raise ValueError(
            "Text cannot be empty."
        )

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    if not response.embeddings:

        raise RuntimeError(
            "No embedding was returned."
        )

    return response.embeddings[0].values


# =========================================================
# EMBED MULTIPLE TEXTS
# =========================================================

def embed_texts(texts):

    if not texts:

        return []

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts
    )

    return [
        embedding.values
        for embedding in response.embeddings
    ]