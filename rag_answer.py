# =========================================================
# JARVIS V4.5 - RAG ANSWER GENERATION
# =========================================================

from google import genai
from config import GEMINI_API_KEY

from rag_store import search_knowledge


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# JARVIS V4.10 - RAG ANSWER WITH SOURCES
# =========================================================

def answer_with_rag(
    question,
    top_k=3
):

    results = search_knowledge(
        question,
        top_k=top_k
    )

    if not results:

        return None


    # -----------------------------------------------------
    # Build context + source information
    # -----------------------------------------------------

    context_parts = []
    sources = []

    for number, result in enumerate(
        results,
        start=1
    ):

        source = result["metadata"].get(
            "source",
            "unknown"
        )

        context_parts.append(
            f"[Context {number}]\n"
            f"Source: {source}\n"
            f"{result['text']}"
        )

        if source not in sources:

            sources.append(
                source
            )


    context = "\n\n".join(
        context_parts
    )


    # -----------------------------------------------------
    # RAG prompt
    # -----------------------------------------------------

    prompt = f"""
You are JARVIS, a personal AI assistant.

Answer the user's question using ONLY the
provided context.

Rules:

- Be concise.
- Be clear.
- Do not invent facts.
- Do not use outside knowledge.
- If the context does not contain enough
  information, say that the knowledge base
  does not contain the answer.
- Do not mention internal retrieval scores.

CONTEXT:
{context}

USER QUESTION:
{question}
"""


    # -----------------------------------------------------
    # Generate answer
    # -----------------------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        answer = response.text or None

        if not answer:

            return None


        # -------------------------------------------------
        # Add source section
        # -------------------------------------------------

        source_lines = []

        for source in sources:

            source_lines.append(
                f"- {source}"
            )

        source_text = "\n".join(
            source_lines
        )

        return (
            f"{answer}\n\n"
            f"Sources:\n"
            f"{source_text}"
        )


    except Exception as error:

        print(
            f"RAG AI ERROR: {error}"
        )

        return None