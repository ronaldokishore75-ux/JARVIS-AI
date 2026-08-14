# =========================================================
# JARVIS V4.8 - SMART DOCUMENT CHUNKER
# =========================================================

import re


def _split_sentences(text):
    """
    Split text into sentence-like units while preserving
    complete sentences.
    """

    parts = re.split(
        r'(?<=[.!?])\s+|\n{2,}',
        text.strip()
    )

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]


def _split_long_sentence(sentence, chunk_size):
    """
    If one sentence is larger than chunk_size, split it
    at word boundaries.
    """

    words = sentence.split()

    pieces = []
    current_words = []
    current_length = 0

    for word in words:

        extra = len(word)

        if current_words:
            extra += 1

        if (
            current_length + extra
            <= chunk_size
        ):

            current_words.append(word)
            current_length += extra

        else:

            if current_words:
                pieces.append(
                    " ".join(current_words)
                )

            current_words = [word]
            current_length = len(word)

    if current_words:
        pieces.append(
            " ".join(current_words)
        )

    return pieces


def chunk_text(
    text,
    chunk_size=500,
    overlap=100
):
    """
    Create chunks using sentence boundaries.

    Preference:
        paragraph/sentence boundary
        -> word boundary only when a single sentence
           is larger than chunk_size.

    Overlap is also sentence-aware.
    """

    if not text or not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0."
        )

    if overlap < 0:
        raise ValueError(
            "overlap cannot be negative."
        )

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size."
        )

    sentences = _split_sentences(text)

    if not sentences:
        return []

    # -----------------------------------------------------
    # Expand sentences that are individually too large
    # -----------------------------------------------------

    units = []

    for sentence in sentences:

        if len(sentence) <= chunk_size:

            units.append(sentence)

        else:

            units.extend(
                _split_long_sentence(
                    sentence,
                    chunk_size
                )
            )

    # -----------------------------------------------------
    # Build base chunks from complete units
    # -----------------------------------------------------

    base_chunks = []

    current_units = []
    current_length = 0

    for unit in units:

        extra = len(unit)

        if current_units:
            extra += 1

        if (
            current_units
            and current_length + extra > chunk_size
        ):

            base_chunks.append(
                " ".join(current_units)
            )

            current_units = []
            current_length = 0

        current_units.append(unit)

        if current_length:
            current_length += 1

        current_length += len(unit)

    if current_units:

        base_chunks.append(
            " ".join(current_units)
        )

    if not base_chunks:
        return []

    # -----------------------------------------------------
    # Sentence-aware overlap
    # -----------------------------------------------------

    if overlap == 0 or len(base_chunks) == 1:

        return base_chunks

    final_chunks = [base_chunks[0]]

    for index in range(1, len(base_chunks)):

        previous_chunk = base_chunks[index - 1]
        current_chunk = base_chunks[index]

        previous_units = _split_sentences(
            previous_chunk
        )

        overlap_units = []
        overlap_length = 0

        for unit in reversed(previous_units):

            extra = len(unit)

            if overlap_units:
                extra += 2

            if overlap_length + extra > overlap:
                break

            overlap_units.insert(
                0,
                unit
            )

            overlap_length += extra

        if overlap_units:

            combined = (
                " ".join(overlap_units)
                + " "
                + current_chunk
            )

        else:

            combined = current_chunk

        # Never exceed chunk_size due to overlap.
        if len(combined) <= chunk_size:

            final_chunks.append(
                combined
            )

        else:

            final_chunks.append(
                current_chunk
            )

    return final_chunks