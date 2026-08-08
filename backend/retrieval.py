import re


# Common words that don't help much with retrieval
STOP_WORDS = {
    "the",
    "a",
    "an",
    "is",
    "are",
    "was",
    "were",
    "what",
    "which",
    "who",
    "when",
    "where",
    "why",
    "how",
    "does",
    "do",
    "did",
    "can",
    "could",
    "would",
    "should",
    "and",
    "or",
    "of",
    "to",
    "in",
    "on",
    "for",
    "with",
    "from",
    "about",
    "this",
    "that",
    "these",
    "those",
    "it",
    "its",
    "be",
    "been",
    "being",
}


def tokenize(text: str) -> list[str]:
    """
    Extract words using regular expressions.
    """

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )

    return [
        word
        for word in words
        if word not in STOP_WORDS
        and len(word) > 2
    ]


def calculate_score(
    question: str,
    chunk_text: str
) -> int:

    question_words = tokenize(question)
    chunk_words = tokenize(chunk_text)

    if not question_words or not chunk_words:
        return 0

    chunk_word_set = set(chunk_words)

    score = 0

    for word in question_words:

        if word in chunk_word_set:

            # Basic keyword match
            score += 1

            # Extra weight for repeated occurrences
            occurrences = chunk_words.count(word)

            if occurrences > 1:
                score += min(occurrences - 1, 3)

    # Exact phrase bonus
    question_clean = " ".join(
        tokenize(question)
    ).lower()

    chunk_clean = chunk_text.lower()

    if question_clean and question_clean in chunk_clean:
        score += 5

    return score


def retrieve_chunks(
    question: str,
    chunks: list[dict],
    top_k: int = 5
) -> list[dict]:

    results = []

    for chunk in chunks:

        score = calculate_score(
            question,
            chunk["text"]
        )

        if score > 0:

            result = chunk.copy()

            result["score"] = score

            results.append(result)

    # Highest score first
    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]