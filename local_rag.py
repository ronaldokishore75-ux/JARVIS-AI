# =========================================================
# JARVIS V6.5 - LOCAL LLM + RAG
# =========================================================

from local_llm import ask_local
from rag_store import search_knowledge


# =========================================================
# ANSWER USING LOCAL LLM + RAG
# =========================================================

def answer_with_local_rag(
    question,
    top_k=1
):
    """
    Retrieve relevant knowledge from the V4 RAG system
    and use the local Ollama model to generate a
    concise, grounded answer.
    """

    # -----------------------------------------------------
    # Validate question
    # -----------------------------------------------------

    if not question or not question.strip():

        raise ValueError(
            "Question cannot be empty."
        )


    question = question.strip()


    # -----------------------------------------------------
    # Retrieve relevant knowledge
    # -----------------------------------------------------

    results = search_knowledge(
        question,
        top_k=top_k
    )


    # -----------------------------------------------------
    # No relevant knowledge
    # -----------------------------------------------------

    if not results:

        return None


    # -----------------------------------------------------
    # Build context
    # -----------------------------------------------------

    context_parts = []
    sources = []

    for number, result in enumerate(
        results,
        start=1
    ):

        text = result.get(
            "text",
            ""
        )

        metadata = result.get(
            "metadata",
            {}
        )

        source = metadata.get(
            "source",
            "unknown"
        )


        if not text:

            continue


        context_parts.append(
            f"[Context {number}]\n"
            f"{text}"
        )


        if source not in sources:

            sources.append(
                source
            )


    # -----------------------------------------------------
    # No usable context
    # -----------------------------------------------------

    if not context_parts:

        return None


    context = "\n\n".join(
        context_parts
    )


    # -----------------------------------------------------
    # Local RAG prompt
    # -----------------------------------------------------

    prompt = f"""
You are JARVIS, a personal AI assistant.

Answer the user's question in ONE or TWO sentences.

Use ONLY the context below.

Rules:
- Do not invent facts.
- Do not use outside knowledge.
- Do not explain your reasoning.
- Do not list steps.
- Do not repeat the question.
- Do not mention the context.
- Do not mention the source.
- Do not say you are Qwen.
- Answer directly as JARVIS.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""


    # -----------------------------------------------------
    # Ask local Ollama model
    # -----------------------------------------------------

    try:

        answer = ask_local(
            prompt
        )

    except Exception as error:

        print(
            f"V6.5 LOCAL RAG ERROR: {error}"
        )

        return None


    # -----------------------------------------------------
    # Validate answer
    # -----------------------------------------------------

    if not answer or not answer.strip():

        return None


    answer = answer.strip()


    # -----------------------------------------------------
    # Add sources
    # -----------------------------------------------------

    source_lines = []

    for source in sources:

        source_lines.append(
            f"- {source}"
        )


    source_text = "\n".join(
        source_lines
    )


    # -----------------------------------------------------
    # Final response
    # -----------------------------------------------------

    return (
        f"{answer}\n\n"
        f"Sources:\n"
        f"{source_text}"
    )