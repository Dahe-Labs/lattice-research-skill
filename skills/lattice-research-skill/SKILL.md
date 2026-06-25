---
name: lattice-research-skill
description: Router skill for Lattice research workflow. Use when the user asks for Lattice Research Skill, needs help choosing between finding papers, requesting PDFs, scanning full texts, finding research gaps, anti-gap verification, honesty review, or wording review. This skill routes to child skills and keeps shared evidence rules; it does not directly perform retrieval, PDF scanning, data extraction, or gap discovery.
---

# Lattice Research Skill

## Purpose

Lattice Research Skill is the router for Lattice research workflow. It should not run the research pipeline itself. It selects the right child skill, preserves shared evidence principles, and keeps the workflow modular.

## Route Table

| User intent | Use skill | Notes |
|---|---|---|
| Find papers, search literature, audit coverage, import selected DOI records into Zotero, create Request PDF list, prepare `request_PDF/doi_list.md` | `lattice-find-papers` | Owns compact Zotero/request-PDF handoff and `zotero_import_manifest.csv`; side-product tables are optional. |
| Analyze project evidence, discover research gaps, or directly verify proposed gaps | `lattice-gaps` | Defaults to compact gap discovery. Full data/problem/method trees are optional and only used when explicitly requested. |
| Check whether a research output is honest and evidence-bound | `lattice-honesty` | Use for unsupported claims, abstract-as-full-text, correlation-as-causation, and uncertainty marking. |
| Review proposal/manuscript wording or supervisor comments | `lattice-wording` | Use for Chinese/English academic wording and reusable wording-rule updates. |

## Shared Rules

1. Do not make full-text claims from abstracts.
2. Do not present a missing PDF or missing variable as a proven research gap.
3. Do not turn broad phrases such as "unified framework", "multi-factor coupling", "data normalization", or "platform/database" into gaps unless they survive verification.
4. Keep user-visible answers concise and Chinese by default.
5. Separate facts, inference, suggestions, uncertainty, and missing evidence.
6. Preserve the Lattice Find Papers handoff contract: `runs/<run_id>/request_PDF/` contains `doi_list.md` and user-downloaded PDFs; `find_papers_outputs/tables/zotero_import_manifest.csv` records Zotero import/readiness status. Lattice Gaps reads these artifacts and matching Zotero PDFs/full text; it does not manage Zotero imports.
7. Default to compact outputs: evidence boundary, high-value signals, up to three candidate gaps, Anti-Gap quick check, and 1-3 next actions.

## Default Routing

If the user asks to start from a research topic, use `lattice-find-papers`.

If the user already has PDFs in `request_PDF/`, Zotero project literature, or other project evidence and asks for gaps, use `lattice-gaps`.

If the user gives one or more candidate gaps and asks whether they are real, use `lattice-gaps` in verify-only mode.

If the user asks whether a report is overclaiming, use `lattice-honesty`.

If the user asks to polish or respond to comments, use `lattice-wording`.
