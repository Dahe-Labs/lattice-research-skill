# Lattice Research Skill Agent Entry

This repository contains portable Agent Skills for Zotero-backed full-text literature analysis and research-gap discovery.

If your agent supports `SKILL.md`, install the folders under `skills/` into the agent's skill directory. See:

- `docs/agent-installation.md`
- `docs/zotero-configuration.md`

If your agent does not support automatic skill discovery, read the router first:

- `skills/lattice-research-skill/SKILL.md`

Then follow the relevant child skill:

- `skills/lattice-find-papers/SKILL.md` for literature search, DOI import planning, full-text availability checks, and Request PDF generation.
- `skills/lattice-gaps/SKILL.md` for compact gap discovery, optional data/experiment/method trees, and verify-only Anti-Gap checks.
- `skills/lattice-wording/SKILL.md` for academic wording review.
- `skills/lattice-honesty/SKILL.md` for evidence-bound honesty and overclaim audits.

Core evidence rule: abstracts, conclusions, DOI metadata, and snippets can locate or screen papers, but they are not full-text evidence for numerical values, experimental procedures, figures, tables, or supplementary methods.
