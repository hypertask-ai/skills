# hypertask-skills

Reusable AI skills for Hypertask writing and processes. Each skill is a self-contained `SKILL.md` (Claude Code / Agent SDK skill format) that also works pasted as a system prompt into any LLM.

## Skills

| Skill | Purpose |
|---|---|
| [improve-readability](skills/improve-readability/SKILL.md) | The Hypertask house writing style: NN/g web-scannable, bottom line up front, half the words, nonviolent phrasing. Mirrors the in-app "Improve with AI" prompt (`src/app/api/ai/_lib/editorAi.ts` in the hypertasks repo). |

## Usage

- **Claude Code**: copy or symlink a skill directory into `~/.claude/skills/` (or a project's `.claude/skills/`), then invoke it by name.
- **Any other CLI/process**: feed the SKILL.md body (below the frontmatter) as the system prompt, followed by the text to rewrite.

## Keeping in sync

The in-app source of truth is `HOUSE_OUTPUT_STYLE` + the `ImproveReadability` prompt in the hypertasks repo (`src/app/api/ai/_lib/editorAi.ts`, shipped in HTPR-4313). If that changes, update the skill here.
