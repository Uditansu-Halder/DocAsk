import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from citations import build_citation_payload


def test_build_citation_payload_uses_source_metadata():
    chunks = [
        {
            "chunk_id": "chunk_001",
            "text": "This is a relevant excerpt from the document.",#ok
            "score": 4,
            "source": {"type": "pdf", "location": "Page 2"},
        }
    ]

    citations = build_citation_payload(chunks)

    assert len(citations) == 1
    assert citations[0]["id"] == "chunk_001"
    assert citations[0]["type"] == "PDF"
    assert citations[0]["location"] == "Page 2"
    assert citations[0]["preview"].startswith("This is a relevant excerpt")
