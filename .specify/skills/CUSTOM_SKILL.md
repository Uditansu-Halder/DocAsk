# DocAsk Document Processing Skill

## Purpose

Provide a consistent implementation approach for processing documents uploaded to DocAsk.

## Supported Formats

The skill supports:

* PDF
* DOCX
* TXT
* PNG
* JPG
* JPEG

## Processing Pipeline

Every uploaded document should follow this pipeline:

```text
File
 ↓
Validation
 ↓
Format Detection
 ↓
Text Extraction / OCR
 ↓
Text Cleaning
 ↓
Chunking
 ↓
Chunk Storage
 ↓
Retrieval
 ↓
AI Context
```

## Format Handling

### PDF

Use `pypdf` to extract text from PDF documents.

If extraction produces no usable text, report a processing failure rather than silently creating empty chunks.

### DOCX

Use `python-docx` to extract text from paragraphs and other relevant textual content.

### TXT

Read the file using an appropriate text encoding and normalize the resulting text.

### PNG / JPG / JPEG

Use an OCR pipeline to recognize text from images.

Image preprocessing may be applied when necessary to improve OCR quality.

If OCR produces no usable text, report that the document could not be processed.

## Text Cleaning

After extraction or OCR:

* Remove unnecessary whitespace.
* Normalize line breaks.
* Remove obviously empty sections.
* Preserve meaningful textual content.
* Avoid transformations that could change the meaning of the document.

## Chunking

Divide cleaned document text into manageable chunks.

Each chunk must remain associated with its source document.

Chunks should preserve enough surrounding context to make retrieval useful.

Avoid creating excessively small chunks that lose meaning.

Avoid unnecessarily large chunks that make retrieval inefficient.

## Retrieval

For the initial MVP:

* Do not require a vector database.
* Use a lightweight application-level retrieval approach.
* Retrieve the most relevant chunks for the user's question.
* Preserve the relationship between chunks and their source document.

If no sufficiently relevant information is found, the system should indicate that the answer is not available from the uploaded document.

## Gemini Context

Only relevant retrieved chunks should be provided as document context to Gemini.

The prompt should clearly distinguish:

```text
DOCUMENT CONTEXT
```

from:

```text
USER QUESTION
```

Gemini should be instructed to answer using the supplied document context.

If the context does not contain enough information to answer the question, the response should state that the information could not be found in the document.

## Error Handling

The processing pipeline must handle:

* Unsupported file types
* Corrupted files
* Empty documents
* Failed PDF extraction
* Failed DOCX extraction
* Invalid text encoding
* OCR failures
* Empty OCR results
* Chunking failures
* Retrieval failures
* Gemini API failures
* Missing API credentials

Errors should be converted into clear user-facing messages where appropriate.

Internal implementation details and API credentials must never be exposed to the frontend.

## Implementation Principles

* Keep extraction, OCR, cleaning, chunking, retrieval, and AI integration as separate services.
* Prefer deterministic processing where possible.
* Avoid unnecessary dependencies.
* Do not introduce a vector database unless the project requirements change.
* Keep the AI provider replaceable.
* Follow the project's constitution and feature specification.
