# Implementation Plan: DocAsk

**Branch**: `001-docask` | **Date**: August 8, 2026 | **Spec**: `specs/001-docask/spec.md`

**Input**: Feature specification from `/specs/001-docask/spec.md`

## Summary

DocAsk is a web-based document question-answering application that allows users to upload supported documents and ask questions about their contents.

The application will support **PDF, DOCX, TXT, PNG, JPG, and JPEG** files. Text-based documents will have their contents extracted directly, while image documents will undergo OCR processing to obtain text.

The implementation will use a FastAPI backend with an HTML/CSS/JavaScript frontend. Uploaded documents will be processed through a pipeline of file validation, text extraction or OCR, text cleaning, chunking, retrieval, and AI-powered answer generation.

The initial MVP will use Gemini as the AI provider and will not require a vector database. Relevant document chunks will be retrieved using a lightweight application-level retrieval mechanism and supplied as context to the AI model. Answers must remain grounded in the uploaded document, and the system must clearly indicate when the requested information cannot be found.

## Technical Context

**Language/Version**: Python 3.11+ for backend; HTML5, CSS3, and modern JavaScript for frontend

**Primary Dependencies**: FastAPI, Uvicorn, pypdf, python-docx, Google GenAI SDK, python-multipart, Pillow, pytesseract, pytest

**Storage**: Local filesystem for uploaded documents and temporary processing data; no database required for the initial MVP

**Testing**: pytest for backend unit and integration tests; FastAPI testing utilities for API endpoint testing

**Target Platform**: Web application running on a Python-compatible server with a modern web browser as the client

**Project Type**: Web application

**Performance Goals**:

* Document upload should provide clear progress/status feedback.
* Text extraction and OCR should complete without unnecessary processing overhead.
* Typical question-answer requests should return within a reasonable interactive time, subject to document size and Gemini API latency.
* The application should remain responsive while documents are being processed.

**Constraints**:

* Supported file formats are PDF, DOCX, TXT, PNG, JPG, and JPEG.
* Image files require OCR before entering the text-processing pipeline.
* Gemini API credentials must be stored in environment variables and never committed to source control.
* The MVP shall not require a vector database.
* The frontend shall use HTML, CSS, and JavaScript without React or Tailwind CSS.
* The backend shall use FastAPI.
* Answers must be grounded in retrieved document content.
* The system must gracefully handle unsupported files, failed extraction, OCR failures, empty documents, missing information, and AI/API failures.

**Scale/Scope**:

* Initial MVP intended for small-scale usage and demonstration.
* Supports individual document upload and question-answering workflows.
* Supports six input formats: PDF, DOCX, TXT, PNG, JPG, and JPEG.
* No requirement for distributed processing, enterprise authentication, or large-scale database infrastructure in the initial version.

## Constitution Check

### Gate 1 — Document-First Architecture

**PASS**

The implementation is centered around the uploaded document. The processing pipeline will follow:

**Upload → File Validation → Text Extraction/OCR → Cleaning → Chunking → Retrieval → AI Context → Answer**

### Gate 2 — Grounded and Reliable Answers

**PASS**

The AI will receive relevant chunks retrieved from the uploaded document as context. If sufficient information cannot be found, the system will communicate that the answer is not available from the document instead of fabricating an answer.

### Gate 3 — Simple MVP Architecture

**PASS**

The initial implementation does not introduce a vector database or unnecessary infrastructure. Retrieval will use a lightweight application-level approach appropriate for the project's scope.

### Gate 4 — Frontend/Backend Separation

**PASS**

The frontend will use HTML/CSS/JavaScript while the backend will use FastAPI. Communication will occur through defined HTTP API endpoints.

### Gate 5 — Replaceable AI Integration

**PASS**

Gemini integration will be isolated within the backend AI service layer. API credentials will be loaded from environment variables, allowing the model provider to be replaced later without rewriting the document-processing pipeline.

### Gate 6 — Testability and Maintainability

**PASS**

File validation, document extraction, OCR, text cleaning, chunking, retrieval, AI integration, and API functionality will be separated into independently testable modules.

**Constitution Status: PASS — No violations identified.**

## Project Structure

### Documentation (this feature)

```text
specs/001-docask/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py
│   ├── api/
│   │   ├── upload.py
│   │   └── chat.py
│   ├── services/
│   │   ├── document_service.py
│   │   ├── extraction_service.py
│   │   ├── ocr_service.py
│   │   ├── chunking_service.py
│   │   ├── retrieval_service.py
│   │   └── ai_service.py
│   ├── models/
│   │   └── schemas.py
│   └── core/
│       └── config.py
│
└── tests/
    ├── unit/
    │   ├── test_file_validation.py
    │   ├── test_extraction.py
    │   ├── test_ocr.py
    │   ├── test_chunking.py
    │   └── test_retrieval.py
    ├── integration/
    │   ├── test_upload.py
    │   └── test_question_answering.py
    └── contract/
        └── test_api_contracts.py

frontend/
├── index.html
├── css/
│   └── style.css
├── js/
│   ├── upload.js
│   ├── chat.js
│   └── api.js
└── assets/
```

**Structure Decision**:

The **Web Application** structure is selected because DocAsk consists of a browser-based frontend and a Python FastAPI backend.

The backend separates file validation, document extraction, OCR, chunking, retrieval, and AI interaction into independent services. This allows each supported file format to use its appropriate extraction mechanism while producing a common text representation for the remainder of the pipeline.

The frontend remains lightweight and framework-free, using HTML, CSS, and JavaScript as defined by the project requirements.

The `tasks.md` file will be generated separately by `/speckit.tasks` and is intentionally not included as an output of `/speckit.plan`.

## Complexity Tracking

No constitution violations identified.

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --------- | ---------- | ------------------------------------ |
| None      | N/A        | N/A                                  |
