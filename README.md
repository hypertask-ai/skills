# Hypertask skills

Teach your AI agent to work a Hypertask board: read, create and move tickets, comment, search.

## Install

1. Install the CLI and log in:
   ```
   curl -fsSL https://raw.githubusercontent.com/hypertask-ai/cli/main/scripts/install.sh | sh && hypertask login
   ```
2. Add the skills. In Claude Code:
   ```
   /plugin marketplace add hypertask-ai/skills
   /plugin install hypertask@hypertask-skills
   ```
   Any other agent: `git clone --depth 1 https://github.com/hypertask-ai/skills && cp -r skills/skills/* <your agent's skills folder>`

## Try it

Ask your agent: *"Find ticket PROJ-1, move it to In Progress, and comment that you started."*

## Skills

| Skill | Use it to |
|---|---|
| `hypertask-tickets` | Read, create and update tickets |
| `hypertask-comments` | Comment and ask questions people answer |
| `hypertask-columns` | Move, claim, label |
| `hypertask-find` | Search, filter, pick the next ticket |
| `hypertask-agent` | Work under its own agent identity |

Bugs and ideas: [CONTRIBUTING.md](CONTRIBUTING.md). Evals: `python3 evals/check.py`.
