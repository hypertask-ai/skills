---
name: hypertask-tickets
description: Read, create and update Hypertask tickets with the hypertask CLI. Use when the user says "file a ticket", "make a ticket for this", "update the ticket", "read ticket PREFIX-123", links a ticket URL, or asks to attach a file, link tickets, set a parent, priority, size or due date.
---

# Tickets with the `hypertask` CLI

Run `hypertask login` once. Add `--json` for machine output. Piped output is already plain and tab-separated.

## Read first

```bash
hypertask task get PROJ-123          # title, description, column, labels, assignees, PRs
hypertask comment list PROJ-123      # the discussion
hypertask task context PROJ-123      # one read-only pack for a session
hypertask task relations PROJ-123    # linked tickets
```

Read the whole ticket before you act on it. A ticket URL ends in `/detail/project-<boardId>/<number>`. The CLI takes the ref (`PROJ-123`), or the number with `--project <boardId>`.

## Create

```bash
hypertask project show --project 42      # prefix, columns, labels: read before you pick any
hypertask task create --project 42 --title "Export button does nothing on Safari" \
  --description-file body.html --labels "BUG" --priority high --section "Todo"
```

- The title states the outcome or the symptom in plain words. Not "Fix stuff".
- Descriptions and comments are **HTML**: wrap text in `<p>`, `<ul>`, `<strong>`. Add `--markdown` to send Markdown instead.
- Never embed images in the body. Add them with `--attach <path-or-url>` (repeatable).
- A good description has **Outcome**, **Done when** (a check anyone can run), **Steps** for a bug, and a link to the source.
- Search first (`hypertask-find`) so you do not file a duplicate.

## Update

```bash
hypertask task update PROJ-123 --title "..." --priority urgent --due 2026-11-01
hypertask task update PROJ-123 --description-file body.html   # replaces the whole description
hypertask task update PROJ-123 --pull-request https://github.com/org/repo/pull/9
hypertask task update PROJ-123 --estimate 4                   # 0 none, 2-6 = XS..XL
```

- `--description` replaces everything. Read the current text first and keep what you do not change. `hypertask task description-history` and `description-restore` undo a bad overwrite.
- `--labels` **replaces** the whole label set. Use `--add-labels` or `--remove-labels` to change one.
- `--assignee` replaces the whole list, so never use it to add yourself. Use `hypertask task assign PROJ-123 --assignee <id>`: it adds and repeats safely. Never remove a person you did not add.

## Structure

```bash
hypertask task update PROJ-123 --parent-task PROJ-100     # make it a subtask
hypertask task link PROJ-123 PROJ-124 --type <type>       # relate two tickets
hypertask task tree --ticket PROJ-100                     # parent and subtasks
```

One ticket, one outcome. Work bigger than the ticket becomes a new, linked ticket.

## Archive and delete

`hypertask task update PROJ-123 --status Archive` hides a ticket and keeps it. `Deleted` is the trash. Archive instead of deleting, and ask before any delete.
