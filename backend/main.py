from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import re

from chunking import create_chunks
from retrieval import retrieve_chunks
from citations import build_citation_payload

import importlib
import os
import tempfile
from pathlib import Path


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# FastAPI
# --------------------------------------------------

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Gemini
# --------------------------------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# --------------------------------------------------
# Global document storage
# --------------------------------------------------

document_text = ""
document_filename = ""
document_chunks = []


# --------------------------------------------------
# Allowed file types
# --------------------------------------------------

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".docx",
    ".txt",
    ".md"
}


# --------------------------------------------------
# Question model
# --------------------------------------------------

class Question(BaseModel):
    question: str


# --------------------------------------------------
# Root endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "DocAsk backend is running."
    }

# --------------------------------------------------
# PDF extraction
# --------------------------------------------------

def extract_text_from_pdf(file_path: str) -> list[dict]:

    try:
        PdfReader = importlib.import_module(
            "pypdf"
        ).PdfReader

    except ImportError:
        raise RuntimeError(
            "PDF support requires pypdf to be installed."
        )

    reader = PdfReader(file_path)

    documents = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        extracted = page.extract_text()

        if extracted and extracted.strip():

            documents.append({
                "text": extracted.strip(),

                "source": {
                    "type": "pdf",
                    "location": f"Page {page_number}"
                }
            })

    return documents


# --------------------------------------------------
# DOCX extraction
# --------------------------------------------------

def extract_text_from_docx(file_path: str) -> list[dict]:

    try:
        Document = importlib.import_module(
            "docx"
        ).Document

    except ImportError:
        raise RuntimeError(
            "DOCX support requires python-docx to be installed."
        )

    document = Document(file_path)

    documents = []

    for paragraph_number, paragraph in enumerate(
        document.paragraphs,
        start=1
    ):

        text = paragraph.text.strip()

        if text:

            documents.append({
                "text": text,

                "source": {
                    "type": "docx",
                    "location":
                        f"Paragraph {paragraph_number}"
                }
            })

    return documents


# --------------------------------------------------
# Image OCR
# --------------------------------------------------

def extract_text_from_image(file_path: str) -> list[dict]:

    try:
        from PIL import Image
        import pytesseract

    except ImportError:
        raise RuntimeError(
            "Image OCR requires Pillow and pytesseract."
        )

    # Change this path if Tesseract is installed elsewhere
    tesseract_path = (
        r"C:\Program Files\Tesseract-OCR"
        r"\tesseract.exe"
    )

    if os.path.exists(tesseract_path):

        pytesseract.pytesseract.tesseract_cmd = (
            tesseract_path
        )

    image = Image.open(file_path)

    text = pytesseract.image_to_string(image)

    if not text.strip():
        return []

    return [
        {
            "text": text.strip(),

            "source": {
                "type": "image",
                "location": "Image"
            }
        }
    ]

# --------------------------------------------------
# Image OCR
# --------------------------------------------------

def extract_text_from_txt(file_path: str) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    full_text = "".join(lines).strip()
    if not full_text:
        return []

    return [{
        "text": full_text,
        "source": {
            "type": "txt",
            "location": "Full Document"
        }
    }]

# --------------------------------------------------
# Markdown extraction
# --------------------------------------------------

def extract_text_from_md(file_path: str) -> list[dict]:

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()

    documents = []

    current_section = "Document"

    for line_number, line in enumerate(
        lines,
        start=1
    ):

        text = line.strip()

        if not text:
            continue

        # Detect Markdown headings
        heading_match = re.match(
            r"^#{1,6}\s+(.+)",
            text
        )

        if heading_match:

            current_section = (
                heading_match.group(1).strip()
            )

            continue

        documents.append({
            "text": text,

            "source": {
                "type": "md",
                "location":
                    f"Section: {current_section} "
                    f"(Line {line_number})"
            }
        })

    return documents

# --------------------------------------------------
# General document extraction
# --------------------------------------------------

def extract_text_from_file(
    file_path: str,
    filename: str
) -> list[dict]:

    extension = Path(
        filename
    ).suffix.lower()

    if extension == ".pdf":

        return extract_text_from_pdf(
            file_path
        )

    elif extension == ".docx":

        return extract_text_from_docx(
            file_path
        )

    elif extension in {
        ".png",
        ".jpg",
        ".jpeg"
    }:

        return extract_text_from_image(
            file_path
        )

    elif extension == ".txt":

        return extract_text_from_txt(
            file_path
        )

    elif extension == ".md":

        return extract_text_from_md(
            file_path
        )

    else:

        raise ValueError(
            "Unsupported file type. "
            "Please upload a PDF, image, "
            "DOCX, TXT or MD file."
        )

# --------------------------------------------------
# Upload document
# --------------------------------------------------
@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    global document_text
    global document_filename
    global document_chunks

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    filename = file.filename
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Please upload a PDF, image, DOCX, TXT or MD file."
            )
        )

    try:
        contents = await file.read()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:
            temp_file.write(contents)
            temp_file_path = temp_file.name

        try:
            # 1. CHANGE: Save list of dicts to 'extracted_docs' instead of 'text'
            extracted_docs = extract_text_from_file(
                temp_file_path,
                filename
            )
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        # 2. CHANGE: Validate list existence rather than running .strip() on a list
        if not extracted_docs:
            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text could be extracted "
                    "from this document."
                )
            )

        # 3. CHANGE: Pass the extracted_docs list to create_chunks
        chunks = create_chunks(extracted_docs)
        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Could not create chunks from this document."
            )

        # 4. CHANGE: Join text strings into a single string for document_text & character count
        combined_text = "\n\n".join(doc["text"] for doc in extracted_docs if doc.get("text"))

        document_text = combined_text
        document_filename = filename
        document_chunks = chunks

        return {
            "message": "Document uploaded successfully.",
            "filename": filename,
            "characters": len(combined_text),
            "chunks": len(chunks)
        }

    except HTTPException:
        raise
    except Exception as e:
        print("Upload Error:", e)
        raise HTTPException(
            status_code=500,
            detail=f"Could not process document: {str(e)}"
        )


# --------------------------------------------------
# Ask question
# --------------------------------------------------

@app.post("/ask")
def ask_question(data: Question):

    global document_chunks

    # ------------------------------------------
    # Check if document exists
    # ------------------------------------------

    if not document_chunks:

        raise HTTPException(
            status_code=400,
            detail="Please upload a document first."
        )

    # ------------------------------------------
    # Validate question
    # ------------------------------------------

    question = data.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    # ------------------------------------------
    # Retrieve relevant chunks
    # ------------------------------------------

    relevant_chunks = retrieve_chunks(
        question,
        document_chunks,
        top_k=5
    )

    # ------------------------------------------
    # No relevant chunks found
    # ------------------------------------------

    if not relevant_chunks:

        return {
            "answer": (
                "I couldn't find relevant information "
                "in the uploaded document."
            ),
            "sources": [],
            "citations": []
        }

    # ------------------------------------------
    # Build document context
    # ------------------------------------------

    context_parts = []

    for chunk in relevant_chunks:

        context_parts.append(
            f"""
SOURCE: {chunk["chunk_id"]}

{chunk["text"]}
"""
        )

    context = "\n".join(context_parts)

    # ------------------------------------------
    # Gemini prompt
    # ------------------------------------------

    prompt = f"""
You are DocAsk, a document question-answering assistant.

Answer the user's question ONLY using the provided
document context.

Do not use outside knowledge.

Do not make up information.

If the answer cannot be found in the provided context,
say that the information was not found in the document.

Do not create or invent citations.

DOCUMENT CONTEXT:

{context}

QUESTION:

{question}
"""

    # ------------------------------------------
    # Generate answer with Gemini
    # ------------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        answer = response.text

        # --------------------------------------
        # Build sources and citations
        # --------------------------------------

        sources = []

        for chunk in relevant_chunks:

            sources.append({
                "chunk_id": chunk["chunk_id"],
                "score": chunk["score"],
                "preview": chunk["text"][:400]
            })

        citations = build_citation_payload(relevant_chunks)

        

        return {
            "answer": answer,
            "sources": sources,
            "citations": citations
        }

    except Exception as e:

        print("AI Error:", e)

        raise HTTPException(
            status_code=500,
            detail="Sorry, I couldn't generate an answer."
        )