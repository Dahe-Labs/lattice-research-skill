# Installation

## Install All Lattice Skills

```bash
git clone https://github.com/Stephendahe/lattice-research-skill.git
cd lattice-research-skill
mkdir -p ~/.codex/skills
cp -R skills/lattice-* ~/.codex/skills/
```

Then restart Codex or open a new Codex session.

## Install A Subset

```bash
cp -R skills/lattice-research-skill ~/.codex/skills/
cp -R skills/lattice-find-papers ~/.codex/skills/
cp -R skills/lattice-gaps ~/.codex/skills/
```

`lattice-wording` and `lattice-honesty` can be installed separately if needed.

## Zotero Notes

For DOI import and local-library evidence checks, keep Zotero Desktop running and make sure the Zotero local API / connector is available to Codex.

If Zotero is unavailable, Lattice Find Papers can still prepare Request PDF lists, but Lattice Gaps should not treat abstracts or metadata as full-text evidence.

Detailed setup instructions are here:

[Zotero Configuration for Lattice](docs/zotero-configuration.md)
