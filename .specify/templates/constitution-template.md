# DocAsk Constitution

## Core Principles

### 1. Document-First Architecture

DocAsk shall be designed primarily around user-provided documents. The system must allow users to upload supported documents, extract their text reliably, process the extracted content, and use that content as the primary knowledge source for answering user questions.

The document-processing pipeline shall remain modular so that extraction, cleaning, chunking, retrieval, and question answering can be developed and tested independently.

### 2. Grounded and Reliable Answers

The system shall prioritize answers that are grounded in the content of the uploaded document rather than unsupported model-generated information.

The AI should use retrieved document chunks as context when answering questions. When the required information cannot be found in the uploaded document, the system should clearly indicate that the answer is not available from the provided document instead of confidently inventing information.

### 3. Simple MVP Architecture

The initial version shall favor simplicity, maintainability, and ease of development over unnecessary infrastructure.

The MVP shall not require a vector database. Document chunks may initially be retrieved using a lightweight, application-level retrieval approach suitable for the project's scope.

Additional infrastructure should only be introduced when it provides a clear benefit to the project and is justified by the requirements.

### 4. Clear Separation of Frontend and Backend

DocAsk shall use a clear client-server architecture.

The frontend shall be implemented using HTML, CSS, and JavaScript without requiring React or Tailwind CSS. The backend shall be implemented using Python and FastAPI.

The backend shall expose well-defined API endpoints for document upload, document processing, retrieval, and question answering. Frontend and backend responsibilities shall remain clearly separated to allow team members to work independently.

### 5. AI Integration Through a Replaceable Interface

AI functionality shall be implemented through a modular interface so that the underlying language model can be changed without requiring major changes to the document-processing pipeline.

The project shall use Gemini as the primary AI service rather than NVIDIA's API because of the project's available API-credit constraints.

AI calls shall be isolated from core document-processing logic, and API credentials must be stored securely using environment variables rather than being hard-coded into source files.

## Development Standards

### Code Quality and Maintainability

Code shall be organized into logical modules with clear responsibilities. Functions should perform focused tasks and avoid unnecessary coupling.

Configuration, API credentials, document processing, retrieval, and AI interaction should be kept separate wherever practical.

The project should favor readable and understandable implementations over unnecessary complexity.

### Document Processing Pipeline

The document-processing flow shall follow a predictable sequence:

**Upload → Text Extraction → Text Cleaning → Chunking → Retrieval → AI Context → Answer**

Each stage should produce a clearly defined output that can be tested independently.

For PDF documents, text extraction shall use an appropriate Python PDF-processing library such as `pypdf`. The system should handle documents where text extraction fails or produces empty content gracefully.

### API and Error Handling

FastAPI endpoints shall return clear and consistent responses.

The backend shall validate uploaded files and user requests before processing them. Errors such as unsupported files, failed text extraction, empty documents, invalid questions, and AI-service failures should be handled gracefully and should not cause the application to crash.

### Team Collaboration

Development responsibilities shall remain separated according to the team's agreed roles.

The backend implementation shall focus on FastAPI, document processing, chunking, retrieval, and AI integration. The frontend implementation shall focus on the HTML/CSS/JavaScript interface and communication with the backend APIs.

Shared API contracts should be established before frontend and backend integration so that both sides can be developed independently.

## Project Scope

The first implementation shall focus on delivering a functional document-question-answering MVP rather than attempting to build a fully scalable enterprise document intelligence platform.

The MVP should support:

* Document upload
* PDF text extraction
* Text cleaning and preprocessing
* Text chunking
* Retrieval of relevant chunks
* AI-powered question answering using Gemini
* Answers grounded in uploaded document content
* Clear handling of questions whose answers are not present in the document
* A simple web-based frontend
* FastAPI-based backend APIs

Features such as vector databases, complex authentication systems, large-scale distributed processing, and other infrastructure-heavy additions shall not be required unless they become necessary for the project's defined requirements.

## Governance

All implementation decisions should follow this constitution unless a requirement in the project's specification explicitly requires otherwise.

Changes to the architecture, technology choices, or core principles should be discussed and agreed upon by the team before implementation.

The constitution serves as the project's guiding development standard. The project specification and approved requirements define what the system must do, while this constitution defines the principles and engineering standards by which it should be built.

When a conflict exists, explicit project requirements take precedence over implementation preferences, while deviations from these principles should be documented and justified.

**Version**: 1.0.0 | **Ratified**: August 8, 2026 | **Last Amended**: August 8, 2026
