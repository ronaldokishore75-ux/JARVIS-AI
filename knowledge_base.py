# =========================================================
# JARVIS V4.11 - MULTI-DOCUMENT KNOWLEDGE BASE
# =========================================================

import os

from document_ingest import ingest_file


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".py",
    ".json",
}


# =========================================================
# INGEST DIRECTORY
# =========================================================

def ingest_directory(
    directory,
    recursive=True,
    chunk_size=500,
    overlap=100
):

    if not os.path.exists(directory):

        raise FileNotFoundError(
            f"Directory not found: {directory}"
        )

    if not os.path.isdir(directory):

        raise ValueError(
            f"Not a directory: {directory}"
        )

    total_files = 0
    total_chunks = 0

    # -----------------------------------------------------
    # Find files
    # -----------------------------------------------------

    if recursive:

        walker = os.walk(directory)

    else:

        walker = [
            (
                directory,
                [],
                os.listdir(directory)
            )
        ]

    for root, _, files in walker:

        for filename in files:

            extension = os.path.splitext(
                filename
            )[1].lower()

            if extension not in SUPPORTED_EXTENSIONS:
                continue

            file_path = os.path.join(
                root,
                filename
            )

            try:

                chunks = ingest_file(
                    file_path,
                    chunk_size=chunk_size,
                    overlap=overlap
                )

                total_files += 1
                total_chunks += chunks

            except Exception as error:

                print(
                    f"V4.11 INGEST ERROR: "
                    f"{file_path}"
                )

                print(
                    error
                )

    return {
        "files": total_files,
        "chunks": total_chunks,
    }