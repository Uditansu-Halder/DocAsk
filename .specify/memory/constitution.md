# DocAsk Constitution

Purpose: This document codifies the engineering, data, and governance principles for the DocAsk project — an opinionated, auditable document-retrieval and answer-generation service focused on accurate provenance, privacy, and reproducible results.

## Core Principles

### I. User-First Accuracy
All answers must prioritize correctness and transparent provenance. Every user-facing result should include source citations, a short provenance summary, and a confidence indicator when applicable.

### II. Provenance & Citations (Non-negotiable)
All returned claims that rely on external documents must include: (a) source identifier (URL, document id), (b) quoted excerpt or passage reference, and (c) retrieval score or rank. Suppress hallucinated or unverified assertions.

### III. Privacy & Data Minimization
Treat user data and ingested documents as sensitive by default. Avoid storing PII unless explicitly permitted; when stored, encrypt at rest and document retention policies. Allow data deletion and export on request.

### IV. Test-First Development
New features require tests before implementation: unit tests for logic, integration tests for retrieval & ranking, and dataset/regression tests for model-related behavior. CI must enforce test coverage and block merging on failing gates.

### V. Modularity & Reproducibility
Design components (ingestion, chunking, embedding, retrieval, ranking, answer synthesis) as well-defined, independently testable modules with versioned interfaces. Configs and pipelines must be reproducible from declared manifests.

### VI. Observability & Traceability
Emit structured logs, traces, and metrics for ingestion, retrieval latency, and answer generation. Logs must include correlation IDs to trace a user request end-to-end and to reproduce results when needed.

### VII. Simplicity & Minimalism
Prefer simple, auditable approaches over complex heuristics. Document trade-offs and avoid premature optimization; YAGNI applies to components that increase operational complexity without clear value.

## Data & Security Requirements

- PII Handling: Identify, redact, or encrypt PII according to the project's privacy policy. Tests must include PII-detection checks for ingestion pipelines.
- Access Control: Enforce least-privilege access for storage and model endpoints. Secrets must be stored in a secrets manager; never commit credentials.
- Dataset Provenance: Record the source, ingestion date, and transform steps for every dataset used for retrieval.

## Development Workflow

- Branching: Use feature branches and descriptive PR titles. Link PRs to issue descriptions and include reproducible reproduction steps for behavior changes.
- Reviews: At least one reviewer must verify tests, citations, and privacy implications for changes affecting ingestion, storage, or answer generation.
- CI: Runs linting, unit tests, integration tests, and a lightweight end-to-end retrieval test that validates citations and deterministic outputs for fixed inputs.

## Testing & Quality Gates

- Unit tests: cover logic in `chunking.py`, `retrieval.py`, and `citations.py`.
- Integration tests: validate end-to-end ingestion → retrieval → citation flow using representative sample documents in `backend/tests/`.
- Regression datasets: store a small canonical test corpus and expected outputs for critical flows; treat significant diffs as review blockers.

## Versioning & Breaking Changes

- Use semantic versioning for public-facing APIs and for retrieval/index formats. Document migration steps for breaking changes and provide tooling to upgrade indexes or datasets.

## Governance

Amendments to this constitution require a documented PR describing the change, a migration/rollback plan (if applicable), and approval from at least two core maintainers. The constitution is the default source of truth for engineering decisions; exceptions must be documented in the PR and linked to an approved issue.

**Version**: 1.0.0 | **Ratified**: 2026-08-08 | **Last Amended**: 2026-08-08
