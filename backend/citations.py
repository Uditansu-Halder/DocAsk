def build_citation_payload(chunks: list[dict]) -> list[dict]:
    citations = []

    for chunk in chunks:
        source = chunk.get("source") or {}
        chunk_type = str(source.get("type", "unknown")).upper()
        location = source.get("location", "Unknown location")
        preview = chunk.get("text", "")

        citations.append({
            "id": chunk.get("chunk_id", "chunk_001"),
            "type": chunk_type,
            "location": location,
            "preview": preview[:400],
            "score": chunk.get("score", 0),
        })

    return citations
