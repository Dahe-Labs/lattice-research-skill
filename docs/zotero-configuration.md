# Zotero Configuration for Lattice

This page explains the Zotero setup expected by Lattice Research Skill. Lattice uses Zotero as the local literature hub for DOI records, PDF attachments, indexed full text, and project-specific evidence checks.

The goal is simple: make sure Codex can see the same papers, PDFs, and indexed text that you can see in Zotero, without treating metadata or abstracts as full-text evidence.

## What This Setup Enables

After configuration, Lattice can:

- search matching Zotero items by DOI, title, author-year, project terms, or collection;
- distinguish metadata-only records from records with PDFs or indexed full text;
- use Zotero PDF/indexed text status when deciding whether a paper still needs manual PDF handling;
- pass reliable full-text evidence from `lattice-find-papers` to `lattice-gaps`.

Lattice still does not bypass paywalls, scrape inaccessible PDFs, or read files that are not locally available to Zotero or the project folder.

## Required Setup

1. Install Zotero Desktop.
2. Keep Zotero Desktop open while using Lattice.
3. Enable Zotero's local API:
   - Open Zotero settings/preferences.
   - Go to the Advanced pane.
   - Enable the option that allows other applications on this computer to communicate with Zotero.
4. Make sure the relevant papers are in Zotero.
5. Attach PDFs when available.
6. Let Zotero index the PDFs before expecting full-text search to work.

The local API normally listens at:

```text
http://localhost:23119/api/
```

## Verify Local API Access

With Zotero open, run:

```bash
curl -i "http://localhost:23119/api/users/0/items?limit=1"
```

Expected result:

- `200 OK`: Zotero is reachable and returned local library data.
- `403 Forbidden`: the local API preference is probably disabled.
- `Connection refused` or timeout: Zotero is closed, blocked, or not listening on the expected port.
- `404 Not Found`: the local server is reachable, but the endpoint or API path is wrong.

For Lattice, a successful local API probe is useful, but it is still only the access layer. A paper becomes strong evidence only when the needed PDF, table, figure, supplement, method section, or raw-data source is actually available and readable.

## Configure PDF and Full-Text Indexing

Open Zotero settings/preferences and check the Search pane.

Recommended configuration:

- Keep full-text indexing enabled.
- Avoid setting the maximum indexed characters per file to `0`, because that disables full-text indexing.
- If a PDF was OCRed or replaced, use Zotero's reindex option for that attachment.
- Check Zotero's index statistics to see whether files are indexed, partially indexed, or unindexed.

Important limitation:

- Zotero indexed text can help locate relevant passages, but it may omit figure/table structure, captions, formatting, equations, and supplementary files.
- Lattice treats indexed full text as partial evidence unless the underlying PDF or supplement is also readable.

## Configure Sync and PDF Availability

If you use Zotero across multiple computers, check the Sync pane.

Recommended configuration:

- Enable data syncing if you want item metadata, notes, and full-text content synced across devices.
- Enable file syncing if you want PDFs to download through Zotero storage or WebDAV.
- Choose "download files at sync time" when you want Lattice to find PDFs locally without manual opening.
- If you choose "download files as needed", open the target PDF in Zotero once before running a full-text Lattice workflow.

Lattice works best when PDFs are actually present on the same machine where Codex is running.

## Recommended Lattice Collection Pattern

For project work, use a dedicated Zotero collection so Lattice does not need to scan the whole library.

Suggested pattern:

```text
Codex Mother Library
Codex Mother Library / YYYY-MM-DD
Codex Mother Library / YYYY-MM-DD - Project Name
```

`lattice-find-papers` should import or match screened DOI records during the Find Papers stage. `lattice-gaps` should later read the project folder, request-PDF folder, manifests, and matching Zotero records without repeating DOI import.

## Evidence Levels Used by Lattice

Use these levels when diagnosing why a paper was or was not accepted as evidence:

| Level | Meaning |
|---|---|
| `L0_metadata_only` | Zotero item exists, but no abstract/full text/PDF is available. |
| `L1_abstract_only` | Abstract or metadata is available, but no full-text evidence. |
| `L2_indexed_text` | Zotero indexed text or HTML text exists, but figures/tables/supplements may be missing. |
| `L2_full_text` | Main PDF or full-text article is readable. |
| `L3_figures_tables` | Figures, tables, captions, or embedded numerical evidence are readable. |
| `L4_supplementary` | Supplementary methods/data are available. |
| `L5_raw_data_code` | Raw data, code, or machine-readable datasets are available. |

Strong data, experiment, and method gaps usually require `L2_full_text` or higher. Claims involving exact numbers, parameter drift, experimental procedure, or interface modeling assumptions often require `L3` or `L4`.

## Common Problems

### Zotero is running, but Codex cannot connect

Check:

- Zotero is open on the same machine.
- The local API preference is enabled.
- The URL starts with `http://localhost:23119/api/`.
- No firewall, VPN, or security tool is blocking local connections.

### Zotero item exists, but Lattice still requests the PDF

This is expected when Zotero has only metadata, an abstract, or indexed text without the PDF/supplement needed for the task. Lattice should keep the item in `request_PDF/doi_list.md` until the missing evidence is resolved.

### Indexed text exists, but figures or tables are missing

Zotero full-text indexing is useful for search, but it does not guarantee reliable extraction of tables, figures, equations, captions, or supplementary files. For numerical or experimental claims, attach the original PDF and supplements.

### A paper was imported by DOI, but no PDF appeared

DOI import creates or matches the bibliographic record. It does not guarantee PDF availability. Some items still require manual download, institutional access, open-access lookup, or user-supplied files.

## Fallback When Zotero Is Unavailable

If Zotero cannot be reached:

1. Continue generating the request-PDF list.
2. Export relevant records from Zotero as BibTeX, RIS, CSL JSON, or CSV if possible.
3. Put manually downloaded PDFs into the project's `request_PDF/` folder.
4. Run `lattice-gaps` only after the needed full-text files are present.

Online metadata sources such as Crossref can help locate papers, but they should not be treated as full-text evidence for exact values or experimental procedures.

## Sources Consulted

This tutorial was written for Lattice and paraphrases the setup implications of the following sources:

- Zotero Web API documentation: local API base path, authentication behavior, local API differences, and status-code behavior.  
  <https://www.zotero.org/support/dev/web_api/v3/basics>
- Zotero Search preferences documentation: PDF/EPUB/HTML full-text indexing, index statistics, and reindexing behavior.  
  <https://www.zotero.org/support/preferences/search>
- Zotero Sync preferences documentation: data sync, full-text content sync, attachment file syncing, and download timing.  
  <https://www.zotero.org/support/preferences/sync>
- Zotero developer announcement for the desktop local HTTP API: enabling local communication and the `localhost:23119` usage pattern.  
  <https://groups.google.com/g/zotero-dev/c/ElvHhIFAXrY/m/fA7SKKwsAgAJ>
- Third-party Zotero MCP server documentation, used only as a reference point for MCP-style local Zotero access patterns.  
  <https://mcpservers.org/servers/kujenga/zotero-mcp>
