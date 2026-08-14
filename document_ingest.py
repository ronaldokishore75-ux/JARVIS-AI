# =========================================================
# JARVIS V4.7 - DOCUMENT INGESTION
# =========================================================

import json
import os

from rag_store import add_document


# =========================================================
# SUPPORTED FILE TYPES
# =========================================================

SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".py",
    ".json",
}


# =========================================================
# READ FILE
# =========================================================

def read_document(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if not os.path.isfile(file_path):

        raise ValueError(
            f"Not a file: {file_path}"
        )

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension not in SUPPORTED_EXTENSIONS:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

    except UnicodeDecodeError as error:

        raise ValueError(
            f"Could not decode file as UTF-8: "
            f"{error}"
        )

    # -----------------------------------------------------
    # JSON gets normalized into readable text
    # -----------------------------------------------------

    if extension == ".json":

        try:

            data = json.loads(content)

            content = json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            )

        except json.JSONDecodeError:

            # Keep original text if JSON is malformed.
            pass

    return content


# =========================================================
# INGEST ONE FILE
# =========================================================

def ingest_file(
    file_path,
    chunk_size=500,
    overlap=100
):

    content = read_document(
        file_path
    )

    if not content.strip():

        return 0

    source = os.path.abspath(
        file_path
    )

    chunks_added = add_document(
        content,
        source=source,
        chunk_size=chunk_size,
        overlap=overlap
    )

    print(
        f"V4.7 INGESTED: {source}"
    )

    print(
        f"V4.7 CHUNKS: {chunks_added}"
    )

    return chunks_added