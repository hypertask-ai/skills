# hypertask-skills

Skills that teach an AI session to use a Hypertask board. They cover the board only: tickets, comments, columns, search and agent identity. Each one is a `SKILL.md` that drives the [`hypertask` CLI](https://github.com/hypertask-ai/cli).

## Install

Claude Code:

```
/plugin marketplace add hypertask-ai/skills
/plugin install hypertask@hypertask-skills
```

Other agents: copy a folder from `skills/` into the agent's skills directory.

## Skills

| Skill | Use it to |
|---|---|
| [hypertask-tickets](skills/hypertask-tickets/SKILL.md) | Read, create and update tickets without losing the description. |
| [hypertask-comments](skills/hypertask-comments/SKILL.md) | Write comments people read, and ask questions they answer. |
| [hypertask-columns](skills/hypertask-columns/SKILL.md) | Move tickets, claim them, set labels and columns safely. |
| [hypertask-find](skills/hypertask-find/SKILL.md) | Search every state, filter, pick the next ticket, save views. |
| [hypertask-agent](skills/hypertask-agent/SKILL.md) | Run a long-lived session under its own agent identity. |

Writing style, code review and general workflow skills are not here. Install [pstack](https://github.com/cursor/plugins/tree/main/pstack) for those.

## Evals

`evals/evals.json` holds five cases, one per mistake a board skill must prevent. `python3 evals/check.py` checks that each case still has its rule in the skill it names. Run it before you open a pull request.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for bug reports, ideas, and our contribution policy.
