import re


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def clean_text(text: str) -> str:
    """
    Clean extracted text while preserving useful
    paragraph/line boundaries.
    """

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"\n[ \t]+", "\n", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def split_into_sentences(text: str) -> list[str]:
    """
    Regex-based sentence splitting.
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


def create_chunks(
    documents: list[dict]
) -> list[dict]:

    chunks = []

    chunk_number = 1

    current_sentences = []
    current_length = 0

    current_source = None

    for document in documents:

        text = clean_text(
            document["text"]
        )

        if not text:
            continue

        sentences = split_into_sentences(text)

        for sentence in sentences:

            sentence_length = len(sentence)

            # Start source metadata
            if current_source is None:
                current_source = document["source"]

            # If adding this sentence would
            # exceed the chunk size
            if (
                current_sentences
                and
                current_length + sentence_length
                > CHUNK_SIZE
            ):

                chunk_text = " ".join(
                    current_sentences
                ).strip()

                chunks.append({
                    "chunk_id":
                        f"chunk_{chunk_number:03d}",

                    "text":
                        chunk_text,

                    "source":
                        current_source
                })

                chunk_number += 1

                

                overlap_sentences = []
                overlap_length = 0

                for previous_sentence in reversed(
                    current_sentences
                ):

                    if (
                        overlap_length
                        >= CHUNK_OVERLAP
                    ):
                        break

                    overlap_sentences.insert(
                        0,
                        previous_sentence
                    )

                    overlap_length += len(
                        previous_sentence
                    )

                current_sentences = (
                    overlap_sentences
                )

                current_length = (
                    overlap_length
                )

                current_source = (
                    document["source"]
                )

            current_sentences.append(
                sentence
            )

            current_length += (
                sentence_length
            )

    

    if current_sentences:

        chunk_text = " ".join(
            current_sentences
        ).strip()

        chunks.append({
            "chunk_id":
                f"chunk_{chunk_number:03d}",

            "text":
                chunk_text,

            "source":
                current_source
        })

    return chunks