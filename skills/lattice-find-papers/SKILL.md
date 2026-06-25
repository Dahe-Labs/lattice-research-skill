---
name: lattice-find-papers
description: Use when the user wants to search papers, audit literature coverage, deduplicate and screen papers, import DOI-selected papers into Zotero, check full-text availability, generate runs/run_id/request_PDF/doi_list.md, or prepare compact evidence handoff for gap discovery.
---

# Lattice Find Papers

## Purpose

Lattice Find Papers owns the pipeline from a research topic to a clean Zotero/request-PDF handoff. Its main deliverables are:

```text
runs/<run_id>/request_PDF/doi_list.md
runs/<run_id>/find_papers_outputs/tables/zotero_import_manifest.csv
```

The user downloads missing PDFs into that same `request_PDF/` folder. Lattice Gaps later reads `request_PDF/` and the relevant Zotero collection/readable attachments as its evidence set.

Mechanism maps, data tables, variable relations, experiment audit tables, and logs are optional side products. Do not generate or show them by default unless they directly unblock a requested gap check or the user asks for full evidence mapping. Keep them out of the run root.

## Run Layout

Create or reuse this structure:

```text
runs/<run_id>/
  run_manifest.json
  resume_state.json
  request_PDF/
    doi_list.md
    *.pdf
  find_papers_outputs/
    request_queue/
    logs/
    tables/
      zotero_import_manifest.csv
    outputs/
    inputs/
    intermediate_tables/
```

Only `request_PDF/` stays at the run root. Put every other Lattice Find Papers output under `find_papers_outputs/`.

## Workflow

1. Lock the topic.
   - Identify research object, core phenomenon, material/system, mechanisms, variables, methods, and date/field boundaries.
   - Ask only if missing boundaries would change search strategy.

2. Plan and run retrieval.
   - Use multiple source blocks when available: OpenAlex, Crossref, Semantic Scholar, Google Scholar or equivalent academic search, publisher pages, domain databases, review papers, user seed papers, backward/forward citations, and adjacent terminology.
   - Split queries by object, mechanism, variable, method, parameter, controversy, and benchmark.

3. Build and audit the candidate pool.
   - Deduplicate by DOI, normalized title, author-year, and source URL.
   - Screen title/abstract only for relevance; do not make data, methods, or mechanism conclusions from abstracts.
   - Write only the minimal tables needed for deduplication, full-text status, Request PDF generation, and later gap discovery.

4. Import selected DOI records into Zotero.
   - Read `references/ZOTERO_IMPORT_PROTOCOL.md`.
   - Import only screened, relevant records: `include_core`, `include_variable`, `include_method`, `include_parameter`, and `need_full_text`.
   - Use `Lattice 母文献库` as the parent collection when collection control is available.
   - Use date naming by default: `YYYY-MM-DD`; use `YYYY-MM-DD - project_name` for cross-project or project-specific batches.
   - Write `find_papers_outputs/tables/zotero_import_manifest.csv`.
   - If Zotero write/import is blocked, record the blocker and continue to Request PDF generation.

5. Check full-text availability.
   - Check Zotero after DOI import to identify imported items with attached PDFs, metadata-only items, and manual-download items.
   - Then check online full text, local PDF folders, local supplement folders, and manual source lists as needed.
   - Do not scan a full Zotero/library-wide corpus unless the user explicitly asks.

6. Generate Request PDF output.
   - Write `find_papers_outputs/request_queue/full_text_requests.csv`.
   - Write `find_papers_outputs/outputs/request_literature_list.md`.
   - Write the user-facing download file at `request_PDF/doi_list.md`.
   - `doi_list.md` must contain a DOI list and a Web Links list. Keep it clean and suitable for downloading PDFs.

7. Generate optional side products only when requested.
   - If the user asks for full evidence mapping, produce mechanism maps, variable relations, experiment audit, normalization blockers, and final reports under `find_papers_outputs/`.
   - In the default compact workflow, only record blockers that affect Request PDF or later Lattice Gaps review.

8. Save resume state.
   - Keep `resume_state.json` at the run root.
   - Record missing PDFs, blocked phases, and next resume phase.

## Scripts

Use these scripts when appropriate:

- `scripts/init_run.py`: create the run layout.
- `scripts/build_full_text_request_queue.py`: build Request CSV/MD and root `request_PDF/doi_list.md`.
- `scripts/match_uploaded_full_text.py`: match user-provided PDFs after download.
- `scripts/render_final_outputs.py`: render side-product summary under `find_papers_outputs/outputs/`.
- `scripts/resume_run.py`: inspect or update resume state.

## Evidence Rules

- No full text, no deep data or mechanism conclusion.
- No Methods, no experiment audit.
- No figures/tables/SI, no quantitative extraction.
- Missing full text means generate Request PDF, not a fake conclusion.
- DOI import into Zotero is a literature-management and full-text-acquisition aid; it is not evidence that full text was read.
- Do not call a broad phrase a research gap; leave gap discovery to `lattice-gaps`.

## Output To User

Default visible output:

1. run id and `request_PDF/` path;
2. Zotero import collection/target and manifest path;
3. number of requested PDFs;
4. optional note only if side products were explicitly generated;
5. next action: download PDFs into `request_PDF/` or resolve `manual_pdf_required` items in Zotero.

Do not show long retrieval logs or table dumps unless the user asks.
