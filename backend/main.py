from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

from chunking import create_chunks
from retrieval import retrieve_chunks

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

def extract_text_from_pdf(file_path: str) -> str:

    try:
        PdfReader = importlib.import_module("pypdf").PdfReader

    except ImportError:
        raise RuntimeError(
            "PDF support requires pypdf to be installed."
        )

    reader = PdfReader(file_path)

    text_parts = []

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text_parts.append(extracted)

    return "\n".join(text_parts)


# --------------------------------------------------
# DOCX extraction
# --------------------------------------------------

def extract_text_from_docx(file_path: str) -> str:

    try:
        Document = importlib.import_module("docx").Document

    except ImportError:
        raise RuntimeError(
            "DOCX support requires python-docx to be installed."
        )

    document = Document(file_path)

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)


# --------------------------------------------------
# Image OCR
# --------------------------------------------------

def extract_text_from_image(file_path: str) -> str:

    try:
        from PIL import Image
        import pytesseract

    except ImportError:
        raise RuntimeError(
            "Image OCR requires Pillow and pytesseract."
        )

    # Change this path if Tesseract is installed elsewhere
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    image = Image.open(file_path)

    return pytesseract.image_to_string(image)


# --------------------------------------------------
# TXT / MD extraction
# --------------------------------------------------

def extract_text_from_txt(file_path: str) -> str:

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# --------------------------------------------------
# General document extraction
# --------------------------------------------------

def extract_text_from_file(
    file_path: str,
    filename: str
) -> str:

    extension = Path(filename).suffix.lower()

    if extension == ".pdf":

        return extract_text_from_pdf(file_path)

    elif extension == ".docx":

        return extract_text_from_docx(file_path)

    elif extension in {".png", ".jpg", ".jpeg"}:

        return extract_text_from_image(file_path)

    elif extension in {".txt", ".md"}:

        return extract_text_from_txt(file_path)

    else:

        raise ValueError(
            "Unsupported file type. "
            "Please upload a PDF, image, DOCX, TXT or MD file."
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

    # Check filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    filename = file.filename
    extension = Path(filename).suffix.lower()

    # Check extension
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Please upload a PDF, image, DOCX, TXT or MD file."
            )
        )

    try:

        # ------------------------------------------
        # Read uploaded file
        # ------------------------------------------

        contents = await file.read()

        # ------------------------------------------
        # Create temporary file
        # ------------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            temp_file.write(contents)
            temp_file_path = temp_file.name

        try:

            # --------------------------------------
            # Extract text
            # --------------------------------------

            text = extract_text_from_file(
                temp_file_path,
                filename
            )

        finally:

            # --------------------------------------
            # Delete temporary file
            # --------------------------------------

            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        # ------------------------------------------
        # Check extracted text
        # ------------------------------------------

        if not text or not text.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text could be extracted "
                    "from this document."
                )
            )

        # ------------------------------------------
        # Create regex-based chunks
        # ------------------------------------------

        chunks = create_chunks(text)

        if not chunks:

            raise HTTPException(
                status_code=400,
                detail="Could not create chunks from this document."
            )

        # ------------------------------------------
        # Store document
        # ------------------------------------------

        document_text = text
        document_filename = filename
        document_chunks = chunks

        # ------------------------------------------
        # Return upload information
        # ------------------------------------------

        return {
            "message": "Document uploaded successfully.",
            "filename": filename,
            "characters": len(text),
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
            "sources": []
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
        # Build sources
        # --------------------------------------

        sources = []

        for chunk in relevant_chunks:

            sources.append({
                "chunk_id": chunk["chunk_id"],
                "score": chunk["score"],
                "preview": chunk["text"][:400]
            })

        # --------------------------------------
        # Return answer + sources
        # --------------------------------------

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:

        print("AI Error:", e)

        raise HTTPException(
            status_code=500,
            detail="Sorry, I couldn't generate an answer."
        )