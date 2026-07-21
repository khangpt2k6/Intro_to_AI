# Security and contribution guardrails

This is a course project. Two rules are enforced automatically so a pull
request cannot quietly compromise the repo or the team.

## 1. No AI-agent instruction files

Files that instruct an AI coding agent (Claude, Cursor, Copilot, aider, etc.)
are a prompt-injection vector: a contributor could smuggle in hidden
instructions that a teammate's AI assistant would then follow. They are
**not allowed in this repository**.

Blocked paths (case-insensitive, any directory):

- `.claude/`, `CLAUDE.md`
- `AGENTS.md`, `GEMINI.md`
- `.cursorrules`, `.cursor/`, `.windsurfrules`, `.aider*`
- `.mcp.json`
- `.github/copilot-instructions.md`

These are ignored by `.gitignore` and, if one is added in a PR anyway, the
**Guard** workflow (`.github/workflows/guard.yml`) fails the check.

## 2. No course-provided project brief

`CAI4002 Group Project Description & Team.pdf` is course material and must not
live in the repo. It is git-ignored and blocked by the Guard workflow.

## Making the Guard mandatory

To make these truly unmergeable, protect `main` in
**Settings -> Branches -> Add branch ruleset** and mark the `Guard` and `CI`
checks as required. Until then, do not merge a PR whose `Guard` check is red.

## Reviewing a PR

Before merging any PR, confirm both the `CI` and `Guard` checks are green. If
`Guard` is red, the PR is adding a forbidden file - remove it (or close the
PR) rather than overriding the check.
