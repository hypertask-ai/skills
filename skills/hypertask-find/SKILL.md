---
name: hypertask-find
description: Find Hypertask tickets and pick the next one with the hypertask CLI. Use when the user says "find the ticket about", "is there already a ticket", "what is assigned to me", "what is in column X", "what should I work on next", "save a view", or before filing any new ticket.
---

# Find tickets

## Search before you create

```bash
hypertask search "export button" --project 42
hypertask task list --project 42 --search "export"
```

Check **all three states**. Archive keeps a ticket. Deleted is the trash.

```bash
hypertask task list --project 42 --search "export" --status Normal
hypertask task list --project 42 --search "export" --status Archive
hypertask task list --project 42 --search "export" --status Deleted
```

A ticket moved to another board gets a new number. Search its title, not just the old number. Call a ticket gone only when the title search and `task get` both find nothing.

## Filter

```bash
hypertask task list --project 42 --section "In Progress" --assigned-to me
hypertask task list --project 42 --labels BUG --priority urgent,high --sort-by dueDate --sort-order asc
hypertask search "invoice" --filter updated_since=2026-10-01 --filter has_pr=true
hypertask task list --project 42 --fields title,url --limit 50
```

Page with `--limit` and `--cursor` (or `--offset`). Do not cut a list short with `head`. Ask for fewer rows.

## Pick the next ticket

```bash
hypertask task next --project 42             # highest priority, not leased
hypertask task next --project 42 --label BUG
```

Read the ticket and its comments before you take it. Skip it when someone claimed it recently, when it waits on a person, or when it sits in a decision column. Claim it (`hypertask-columns`) before you start.

## Related work

```bash
hypertask task related PROJ-123     # similar tickets by meaning
hypertask task relations PROJ-123   # explicit links
```

## Saved views

```bash
hypertask view list --project 42
hypertask view create --project 42 --title "My bugs" --label BUG --assignee <userId> --match ALL --visibility Private
hypertask view switch <viewId>
```

A `Public` view is shared with the whole board. Default to `Private`.
