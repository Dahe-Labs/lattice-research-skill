# Lattice Research Skill

Lattice Research Skill is a portable Agent Skills package for AI research agents such as Cursor, Claude, VS Code/GitHub Copilot, and other tools that support `SKILL.md`-based skills. It is designed for full-text literature work rather than abstract-only screening.

The core pain point is that a paper's abstract and conclusion often do not expose the concrete numerical values, experimental procedures, boundary conditions, figures, tables, or supplementary details needed for serious research-gap analysis. Lattice connects the research workflow to Zotero and local PDF evidence so users can reason from full text, not from summaries.

## Core Idea

Lattice helps organize scientific literature into structured evidence trees:

- `data tree`: numerical values, parameters, variables, observed objects, outcomes, and evidence levels.
- `experiment tree`: material preparation, test conditions, protocols, controlled variables, missing variables, and reproducibility blockers.
- `method tree`: measurement methods, modeling assumptions, finite-element parameters, calibration choices, visibility limits, and validation status.

These structures make the research-assistance chain explicit:

```text
Zotero + PDFs + supplements + an Agent Skills-compatible AI agent
  -> data / experiment / method extraction
  -> comparability and evidence-level audit
  -> candidate Research Gap
  -> Anti-Gap verification
  -> narrowed, evidence-bound research opportunity
```

## Skills Included

| Skill | Purpose |
|---|---|
| `lattice-research-skill` | Router for the Lattice workflow. |
| `lattice-find-papers` | Searches literature, screens candidates, imports selected DOI records into Zotero, checks full-text availability, and prepares `request_PDF/doi_list.md`. |
| `lattice-gaps` | Reads `request_PDF`, Zotero PDFs/indexed full text, and Find Papers manifests; defaults to compact gap discovery; supports optional evidence trees and verify-only Anti-Gap checks. |
| `lattice-wording` | Wording review skill. This is still accumulating rules and examples. |
| `lattice-honesty` | Evidence-bound honesty and overclaim audit. This and related skills are still being optimized. |

## Anti-Gap Status

`Lattice Anti-Gap` is intentionally not included as a separate active skill in this release.

Anti-Gap is now embedded inside `lattice-gaps`. Users can skip the gap-discovery stage and directly run reverse verification:

```text
Use lattice-gaps verify-only mode to check whether this proposed gap is real.
```

This avoids maintaining two separate gap-verification paths.

## Zotero-Based Workflow

Lattice assumes a Zotero-centered workflow:

1. `lattice-find-papers` retrieves and screens papers.
2. Screened DOI records are imported or matched in Zotero when possible.
3. Zotero PDF / indexed full-text status is recorded in `zotero_import_manifest.csv`.
4. Missing PDFs or supplements are written to `request_PDF/doi_list.md`.
5. `lattice-gaps` consumes the resulting PDFs, Zotero records, and manifests.

Important evidence rule:

> DOI metadata, abstracts, and web snippets can locate papers or refute broad claims, but they are not full-text evidence for numerical values or experimental procedures.

Default output rule:

> Lattice Gaps uses compact gap discovery by default. Full data trees, problem trees, method trees, and long evidence tables are generated only when the user explicitly asks for full evidence mapping.

## Zotero Setup Guide

Detailed Zotero configuration instructions are maintained separately here:

[Zotero Configuration for Lattice](docs/zotero-configuration.md)

The main page intentionally keeps only this entry point so the setup guide can be updated independently.

## Installation

Clone this repository and copy the skills into the skill directory used by your AI agent:

```bash
git clone https://github.com/Stephendahe/lattice-research-skill.git
cd lattice-research-skill
```

Common install targets:

```bash
# Cursor global skills
mkdir -p ~/.cursor/skills
cp -R skills/lattice-* ~/.cursor/skills/

# Claude global skills
mkdir -p ~/.claude/skills
cp -R skills/lattice-* ~/.claude/skills/
```

For project-local installs, copy the same `skills/lattice-*` folders into the project skill directory supported by your agent.

If your agent does not support automatic skill discovery, use [AGENTS.md](AGENTS.md) as the repository-level entry point.

See the full multi-agent installation guide:

[Agent Installation Guide](docs/agent-installation.md)

## Requirements

- An AI agent with Agent Skills / `SKILL.md` support, or an agent that can read this repository as project instructions.
- Zotero Desktop for the Zotero-backed workflow.
- A working Zotero local API / connector setup if you want DOI import, Zotero search, attachment lookup, or indexed full-text reading.
- Local PDFs or user-supplied full texts for strong data/method/experiment conclusions.

## Current Development Status

- `Lattice Wording`: continuously accumulating wording rules.
- `Lattice Honesty`: actively being optimized for evidence-bound scientific writing.
- `Lattice Gaps`: active core module for data, experiment, method, parameter-drift, and Anti-Gap workflows.
- `Lattice Anti-Gap`: deprecated as an independent skill; use `Lattice Gaps` verify-only mode.

## Evidence Boundaries

Lattice does not bypass paywalls and does not claim to read inaccessible PDFs. When full text, figures, tables, or supplementary materials are missing, the correct output is a request or evidence blocker, not a fake conclusion.

No copyrighted PDFs are included in this repository.
