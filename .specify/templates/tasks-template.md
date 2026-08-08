# Tasks: DocAsk - Document Question Answering

**Input**: Design documents from `/specs/001-docask/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`

**Tests**: No dedicated test tasks are included because tests were not explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable incremental implementation and independent validation.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize the DocAsk project and establish the frontend/backend structure.

* [ ] T001 Create the project structure according to `specs/001-docask/plan.md`
* [ ] T002 Initialize the Python backend environment and dependency configuration in `backend/requirements.txt`
* [ ] T003 [P] Create the FastAPI application entry point in `backend/src/main.py`
* [ ] T004 [P] Create backend package directories and initialization files under `backend/src/`
* [ ] T005 [P] Create frontend structure with `frontend/index.html`, `frontend/css/`, `frontend/js/`, and `frontend/assets/`
* [ ] T006 [P] Create the environment configuration template in `backend/.env.example`
* [ ] T007 Configure `.gitignore` to exclude virtual environments, environment files, uploaded documents, temporary files, caches, and generated artifacts
* [ ] T008 Configure Uvicorn startup and basic FastAPI application settings in `backend/src/main.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement the shared infrastructure required by all user stories.

**⚠️ CRITICAL**: User story implementation begins only after this phase is complete.

* [ ] T009 Create application configuration management in `backend/src/core/config.py`
* [ ] T010 [P] Create shared API response and request schemas in `backend/src/models/schemas.py`
* [ ] T011 [P] Implement application-wide error handling in `backend/src/main.py`
* [ ] T012 [P] Configure structured application logging in `backend/src/main.py`
* [ ] T013 Create document data model and processing-state representation in `backend/src/models/document.py`
* [ ] T014 Create document storage and lifecycle management service in `backend/src/services/document_service.py`
* [ ] T015 Create supported-file validation logic in `backend/src/services/document_service.py`
* [ ] T016 [P] Create API router structure in `backend/src/api/upload.py` and `backend/src/api/chat.py`
* [ ] T017 Create temporary upload and processing directories required by the application
* [ ] T018 Configure Gemini client initialization using environment-based credentials in `backend/src/services/ai_service.py`
* [ ] T019 Configure the frontend API communication layer in `frontend/js/api.js`
* [ ] T020 Create the basic DocAsk page structure and document-upload area in `frontend/index.html`
* [ ] T021 [P] Create initial frontend styling in `frontend/css/style.css`
* [ ] T022 [P] Create frontend application state and utility functions in `frontend/js/app.js`

**Checkpoint**: Foundation ready — file processing, retrieval, AI integration, and user stories can now be implemented.

---

## Phase 3: User Story 1 - Upload and Process a Document (Priority: P1) 🎯 MVP

**Goal**: Allow users to upload PDF, DOCX, TXT, PNG, JPG, and JPEG files and convert them into usable text for question answering.

**Independent Test**: Upload a valid document in each supported format and verify that the system validates it, extracts or recognizes its text, and reports successful processing. Upload an unsupported or unreadable file and verify that an appropriate error is returned.

### Implementation for User Story 1

* [ ] T023 [P] [US1] Implement PDF text extraction using `pypdf` in `backend/src/services/extraction_service.py`
* [ ] T024 [P] [US1] Implement DOCX text extraction using `python-docx` in `backend/src/services/extraction_service.py`
* [ ] T025 [P] [US1] Implement TXT file reading and text extraction in `backend/src/services/extraction_service.py`
* [ ] T026 [P] [US1] Implement image loading and preprocessing for PNG, JPG, and JPEG files in `backend/src/services/ocr_service.py`
* [ ] T027 [P] [US1] Implement OCR text recognition for PNG, JPG, and JPEG files in `backend/src/services/ocr_service.py`
* [ ] T028 [US1] Implement file-type-based extraction routing in `backend/src/services/document_service.py`
* [ ] T029 [US1] Implement extracted-text cleaning and normalization in `backend/src/services/extraction_service.py`
* [ ] T030 [US1] Detect empty or unusable extraction/OCR results in `backend/src/services/document_service.py`
* [ ] T031 [US1] Implement document processing status transitions in `backend/src/services/document_service.py`
* [ ] T032 [US1] Implement document upload endpoint in `backend/src/api/upload.py`
* [ ] T033 [US1] Connect the frontend upload form to the backend upload endpoint in `frontend/js/upload.js`
* [ ] T034 [US1] Display upload and processing states in `frontend/index.html` and `frontend/js/upload.js`
* [ ] T035 [US1] Display unsupported-file, extraction, OCR, and processing errors in `frontend/js/upload.js`
* [ ] T036 [US1] Preserve processed document metadata and extracted content for subsequent retrieval in `backend/src/services/document_service.py`
* [ ] T037 [US1] Verify the complete upload-to-text-processing flow for PDF, DOCX, TXT, PNG, JPG, and JPEG

**Checkpoint**: User Story 1 is complete when a supported document can be uploaded, processed, and prepared for question answering independently.

---

## Phase 4: User Story 2 - Ask Questions About the Document (Priority: P1)

**Goal**: Allow users to ask natural-language questions about a successfully processed document and receive answers grounded in its content.

**Independent Test**: Upload a document containing known information, ask questions whose answers are present and absent from the document, and verify that the system retrieves relevant content and responds appropriately.

### Implementation for User Story 2

* [ ] T038 [US2] Implement text chunking logic in `backend/src/services/chunking_service.py`
* [ ] T039 [US2] Associate generated chunks with their source document in `backend/src/services/chunking_service.py`
* [ ] T040 [US2] Integrate chunk generation into the document-processing pipeline in `backend/src/services/document_service.py`
* [ ] T041 [US2] Implement lightweight document-chunk retrieval in `backend/src/services/retrieval_service.py`
* [ ] T042 [US2] Implement question validation and normalization in `backend/src/services/retrieval_service.py`
* [ ] T043 [US2] Implement relevant-context selection from processed document chunks in `backend/src/services/retrieval_service.py`
* [ ] T044 [US2] Implement Gemini prompt construction using retrieved document context in `backend/src/services/ai_service.py`
* [ ] T045 [US2] Implement grounded answer generation using Gemini in `backend/src/services/ai_service.py`
* [ ] T046 [US2] Implement handling for questions where no relevant document content is found in `backend/src/services/retrieval_service.py`
* [ ] T047 [US2] Implement handling for questions whose requested information is absent from the document in `backend/src/services/ai_service.py`
* [ ] T048 [US2] Ensure Gemini receives only the appropriate document context associated with the active document in `backend/src/services/ai_service.py`
* [ ] T049 [US2] Implement question-answering API endpoint in `backend/src/api/chat.py`
* [ ] T050 [US2] Connect the frontend question input to the question-answering API in `frontend/js/chat.js`
* [ ] T051 [US2] Display generated answers in the frontend chat interface in `frontend/js/chat.js`
* [ ] T052 [US2] Display a loading state while retrieval and Gemini processing are in progress in `frontend/js/chat.js`
* [ ] T053 [US2] Handle empty, invalid, or unanswered questions in `frontend/js/chat.js`
* [ ] T054 [US2] Handle Gemini API failures and timeout responses in `backend/src/services/ai_service.py`
* [ ] T055 [US2] Verify the complete document-question-answering flow from uploaded document to grounded answer

**Checkpoint**: User Story 2 is complete when users can upload a document, ask questions about it, and receive grounded answers independently.

---

## Phase 5: User Story 3 - View and Handle Results (Priority: P2)

**Goal**: Provide a clear and understandable interface for answers, processing states, and failures.

**Independent Test**: Run successful and failed upload/question-answering scenarios and verify that the frontend clearly communicates each result without exposing internal implementation details.

### Implementation for User Story 3

* [ ] T056 [P] [US3] Implement reusable frontend status-message handling in `frontend/js/app.js`
* [ ] T057 [P] [US3] Implement upload progress and processing indicators in `frontend/js/upload.js`
* [ ] T058 [P] [US3] Implement question-answer loading indicators in `frontend/js/chat.js`
* [ ] T059 [US3] Implement user-friendly error message mapping for backend API errors in `frontend/js/api.js`
* [ ] T060 [US3] Display document processing status in the main interface in `frontend/index.html` and `frontend/js/upload.js`
* [ ] T061 [US3] Display clear document-processing failure messages in `frontend/js/upload.js`
* [ ] T062 [US3] Display clear question-answering failure messages in `frontend/js/chat.js`
* [ ] T063 [US3] Ensure backend errors do not expose API keys, credentials, stack traces, or internal configuration in `backend/src/main.py`
* [ ] T064 [US3] Ensure frontend does not expose Gemini credentials or backend secrets
* [ ] T065 [US3] Verify successful, failed, and incomplete workflows through the web interface

**Checkpoint**: All three user stories should now provide a complete and understandable DocAsk workflow.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improve reliability, maintainability, documentation, and deployment readiness across the complete application.

* [ ] T066 [P] Update `specs/001-docask/quickstart.md` with complete local setup and execution instructions
* [ ] T067 [P] Document supported file formats and processing behavior in `specs/001-docask/quickstart.md`
* [ ] T068 [P] Document backend API endpoints and request/response formats in `specs/001-docask/contracts/`
* [ ] T069 Review all environment variables and update `backend/.env.example`
* [ ] T070 Review uploaded-file validation and processing for security weaknesses
* [ ] T071 Review temporary-file handling and ensure temporary uploads are cleaned up appropriately
* [ ] T072 Review error handling across extraction, OCR, chunking, retrieval, and Gemini integration
* [ ] T073 Review logging to ensure secrets and sensitive document contents are not unnecessarily logged
* [ ] T074 [P] Refactor duplicated backend logic across `backend/src/services/`
* [ ] T075 [P] Refactor duplicated frontend logic across `frontend/js/`
* [ ] T076 Review frontend layout and responsive behavior in `frontend/css/style.css`
* [ ] T077 Verify all six supported formats: PDF, DOCX, TXT, PNG, JPG, and JPEG
* [ ] T078 Verify the complete workflow against the acceptance scenarios in `specs/001-docask/spec.md`
* [ ] T079 Run the quickstart procedure from a clean environment and resolve any setup issues
* [ ] T080 Confirm the MVP can be demonstrated without a vector database or additional infrastructure

---

## Dependencies & Execution Order

### Phase Dependencies

* **Setup (Phase 1)**: No dependencies — can start immediately.
* **Foundational (Phase 2)**: Depends on Phase 1 completion and blocks all user stories.
* **User Story 1 (Phase 3)**: Depends on Phase 2.
* **User Story 2 (Phase 4)**: Depends on the document-processing capability established by US1, particularly processed document content.
* **User Story 3 (Phase 5)**: Depends on the frontend/backend behavior established by US1 and US2.
* **Polish (Phase 6)**: Depends on completion of the desired user stories.

### User Story Dependencies

* **User Story 1 (P1)**: Starts after Foundational phase. Provides the document-processing foundation required by the application.
* **User Story 2 (P1)**: Starts after Foundational phase but practically depends on US1's document-processing pipeline being available.
* **User Story 3 (P2)**: Builds on the upload and question-answering workflows from US1 and US2.

Unlike independent CRUD-style stories, the DocAsk stories form a natural processing pipeline:

```text
US1: Upload & Process
          │
          ▼
US2: Ask Questions
          │
          ▼
US3: Display & Handle Results
```

Therefore, implementing US1 → US2 → US3 sequentially is the recommended approach for this project.

### Within Each User Story

* Shared models and infrastructure must exist before dependent services.
* Extraction/OCR must be available before chunking.
* Chunking must be available before retrieval.
* Retrieval must be available before grounded AI generation.
* Backend endpoints must be implemented before frontend API integration.
* Core implementation should be completed before final workflow validation.

### Parallel Opportunities

After Phase 2:

* PDF, DOCX, and TXT extraction can be developed in parallel.
* OCR preprocessing and OCR recognition can be developed in parallel with text-based extraction.
* Frontend upload UI can be developed in parallel with backend extraction services.
* Frontend chat UI can be developed in parallel with backend retrieval development.
* Documentation tasks in Phase 6 can be performed in parallel.
* Frontend refactoring and backend refactoring can be performed independently.

---

## Parallel Example: User Story 1

```text
Developer A:
T023 PDF extraction
T024 DOCX extraction
T025 TXT extraction

Developer B:
T026 Image preprocessing
T027 OCR recognition

Developer C:
T033 Frontend upload integration
T034 Upload/processing UI
T035 Error display
```

These tasks can proceed in parallel because they primarily operate on different files and components.

---

## Parallel Example: User Story 2

```text
Developer A:
T038 Chunking
T039 Chunk-document association

Developer B:
T041 Retrieval
T042 Question validation
T043 Context selection

Developer C:
T050 Frontend question integration
T051 Answer display
T052 Loading state
```

Gemini integration tasks should begin once the retrieval/context contract is established.

---

## Implementation Strategy

### MVP First

The recommended MVP path is:

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational infrastructure.
3. Complete Phase 3: User Story 1.
4. **STOP and VALIDATE** document upload and processing.
5. Complete the minimum required parts of Phase 4: User Story 2.
6. **STOP and VALIDATE** document question answering.
7. Complete the essential parts of Phase 5: User Story 3.
8. **STOP and DEMO** the complete DocAsk workflow.

The minimum demonstrable MVP is:

```text
Upload document
      ↓
Validate file
      ↓
Extract text / OCR
      ↓
Clean text
      ↓
Chunk text
      ↓
Retrieve relevant chunks
      ↓
Send context to Gemini
      ↓
Generate grounded answer
      ↓
Display answer
```

### Incremental Delivery

1. **Foundation** → FastAPI + frontend skeleton.
2. **US1** → Six-format document upload and processing.
3. **US2** → Chunking + retrieval + Gemini question answering.
4. **US3** → Complete user-facing feedback and error handling.
5. **Polish** → Documentation, security review, cleanup, and final validation.

### Team Strategy

For the four-person team, the recommended split is:

**Backend Developer**

* Document validation
* PDF/DOCX/TXT extraction
* OCR
* Chunking
* Retrieval
* Gemini integration
* FastAPI endpoints

**Frontend Developers**

* Upload interface
* Processing states
* Chat/question interface
* Answer display
* Error states
* Responsive styling

**Integration/Support Developer**

* API contract coordination
* Frontend/backend integration
* Documentation
* End-to-end workflow verification
* Deployment/setup support

All team members should coordinate around the API contracts before integrating frontend and backend components.

---

## Notes

* `[P]` tasks can be performed in parallel when their dependencies are satisfied.
* `[US1]`, `[US2]`, and `[US3]` map tasks directly to the corresponding user stories in `spec.md`.
* Exact file paths are included for every implementation task.
* The initial implementation intentionally does **not** introduce a vector database.
* The six supported formats are **PDF, DOCX, TXT, PNG, JPG, and JPEG**.
* Image files require OCR before entering the common text-processing pipeline.
* Gemini is the AI provider for the initial implementation.
* The frontend uses HTML, CSS, and JavaScript.
* The backend uses Python and FastAPI.
* `tasks.md` should be treated as the execution checklist generated from the approved design documents.