import re


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def clean_text(text: str) -> str:
    """
    Clean text extracted from a document using regular expressions.
    """

    # Normalize Windows line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Replace tabs with spaces
    text = re.sub(r"\t+", " ", text)

    # Remove excessive spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # Keep paragraph breaks but remove excessive blank lines
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def split_into_sentences(text: str) -> list[str]:
    """
    Split text into sentences using regular expressions.
    """

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def create_chunks(text: str) -> list[dict]:
    """
    Create overlapping chunks using regex-based sentence splitting.
    """

    text = clean_text(text)

    if not text:
        return []

    sentences = split_into_sentences(text)

    chunks = []

    current_chunk = []
    current_length = 0

    chunk_number = 1

    for sentence in sentences:

        sentence_length = len(sentence)

        # If adding this sentence exceeds the chunk size,
        # save the current chunk first.
        if (
            current_chunk
            and current_length + sentence_length > CHUNK_SIZE
        ):

            chunk_text = " ".join(current_chunk).strip()

            chunks.append({
                "chunk_id": f"chunk_{chunk_number:03d}",
                "text": chunk_text
            })

            chunk_number += 1

            # Create overlap using the last few sentences
            overlap_text = ""
            overlap_sentences = []

            for previous_sentence in reversed(current_chunk):

                if len(overlap_text) >= CHUNK_OVERLAP:
                    break

                overlap_sentences.insert(
                    0,
                    previous_sentence
                )

                overlap_text = " ".join(
                    overlap_sentences
                )

            current_chunk = overlap_sentences
            current_length = len(overlap_text)

        current_chunk.append(sentence)
        current_length += sentence_length

    # Add final chunk
    if current_chunk:

        chunk_text = " ".join(current_chunk).strip()

        chunks.append({
            "chunk_id": f"chunk_{chunk_number:03d}",
            "text": chunk_text
        })

    return chunks