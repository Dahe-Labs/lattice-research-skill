# Agent Installation Guide

Lattice Research Skill is distributed as a portable Agent Skills package. Each skill is a folder with a `SKILL.md` file plus optional scripts, references, schemas, examples, and assets.

Use this page to install the same skill package in Cursor, Claude, VS Code/GitHub Copilot, or another AI agent that supports `SKILL.md`-based skills.

## Package Layout

```text
lattice-research-skill/
  skills/
    lattice-research-skill/
      SKILL.md
    lattice-find-papers/
      SKILL.md
      scripts/
      references/
      assets/
    lattice-gaps/
      SKILL.md
      scripts/
      references/
    lattice-wording/
      SKILL.md
    lattice-honesty/
      SKILL.md
```

The skill names intentionally use lowercase letters and hyphens so they match the Agent Skills convention and their parent folder names.

## Install from GitHub

```bash
git clone https://github.com/Stephendahe/lattice-research-skill.git
cd lattice-research-skill
```

Then copy `skills/lattice-*` into your agent's skill directory.

## Cursor

Global install:

```bash
mkdir -p ~/.cursor/skills
cp -R skills/lattice-* ~/.cursor/skills/
```

Project-local install:

```bash
mkdir -p .cursor/skills
cp -R skills/lattice-* .cursor/skills/
```

Restart Cursor or open a new Agent chat. Cursor should discover the skills from their `SKILL.md` descriptions. If a skill is not selected automatically, ask Cursor explicitly:

```text
Use lattice-research-skill for this task.
```

## Claude

Claude Code user-level install:

```bash
mkdir -p ~/.claude/skills
cp -R skills/lattice-* ~/.claude/skills/
```

Restart Claude Code or start a new session after copying the folders. For Claude.ai or API-based custom-skill workflows, upload or register the same skill folders according to Anthropic's custom-skill interface.

Manual trigger examples:

```text
Use lattice-find-papers to search and request PDFs for this topic.
Use lattice-gaps in verify-only mode for this proposed research gap.
```

## VS Code / GitHub Copilot

Project-local install:

```bash
mkdir -p .github/skills
cp -R skills/lattice-* .github/skills/
```

Then open a new chat or agent session. Skills can be loaded automatically from their descriptions or manually invoked if your client exposes them as slash commands.

## Other Agent Skills-Compatible Tools

For any agent that follows the Agent Skills pattern, copy the skill folders into the tool's configured skill directory:

```bash
mkdir -p <your-agent-skills-dir>
cp -R skills/lattice-* <your-agent-skills-dir>/
```

If the tool does not support automatic `SKILL.md` discovery, use the repository as reference material and explicitly ask the agent to read:

```text
skills/lattice-research-skill/SKILL.md
```

Then ask it to follow the relevant child skill:

```text
skills/lattice-find-papers/SKILL.md
skills/lattice-gaps/SKILL.md
skills/lattice-wording/SKILL.md
skills/lattice-honesty/SKILL.md
```

## Recommended Prompt Pattern

Start broad through the router:

```text
Use lattice-research-skill to choose the right workflow for this project.
```

Start directly when the task is already clear:

```text
Use lattice-find-papers to build a literature pool and request missing PDFs.
Use lattice-gaps to run compact gap discovery from my PDFs and Zotero records.
Use lattice-gaps full evidence mapping if I explicitly need data, experiment, and method trees.
Use lattice-gaps verify-only mode to test whether this proposed gap is real.
Use lattice-wording to review academic phrasing.
Use lattice-honesty to audit unsupported claims.
```

## Zotero Requirement

Lattice works best when Zotero Desktop is running on the same machine as the agent, with the local API available and relevant PDFs attached or indexed.

See:

[Zotero Configuration for Lattice](zotero-configuration.md)

## Sources Consulted

This guide follows the public Agent Skills directory pattern and client-specific skill-discovery guidance from:

- Agent Skills specification.
  <https://agentskills.io/specification>
- Anthropic Agent Skills documentation.
  <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview>
- Cursor Agent Skills documentation.
  <https://cursor.com/docs/skills>
- VS Code Agent Skills documentation.
  <https://code.visualstudio.com/docs/agent-customization/agent-skills>
