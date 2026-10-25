---
name: hypertask-columns
description: Move Hypertask tickets between columns and manage columns, labels, assignees and blockers. Use when the user says "move the ticket", "put it in progress", "mark done", "assign it", "add a label", "create a column", "who is this waiting on", or when claiming or handing off a ticket.
---

# Columns, labels, owners

Columns differ on every board. **Read the real ones first.** Never guess names.

```bash
hypertask section list --project 42
hypertask project manifest 42       # ordered columns and the move rules
hypertask project playbook 42       # the board's own working rules and definition of done
```

If the board has a playbook, it outranks this skill.

## Move

```bash
hypertask task move PROJ-123 --section "In Progress"
hypertask task get PROJ-123          # read it back
```

Read the ticket back after every move. A cross-board move is `hypertask task move <numeric-id> --to <boardId> --to-section <id>`. The ticket gets a new number and the old link breaks.

Move as the work moves: into the working column when you start, into review or done only when that is true. Never move a ticket you did not touch.

## Claim and hand off

```bash
hypertask task assign PROJ-123 --self            # agent token: adds you, keeps people
hypertask task assign PROJ-123 --assignee 123    # add a person or agent
hypertask task waiting-on PROJ-123 --user 123    # blocked by this person
hypertask task waiting-on PROJ-123 --user none   # clear the block
hypertask task move-to-inbox PROJ-123 --user 123 # route into a member's inbox
```

A person and an agent usually share a ticket. Add yourself. Never remove or replace a person. `task update --assignee` replaces the whole list, so avoid it.

## Labels

```bash
hypertask labels list --project 42
hypertask labels create --project 42 --name "BUG" --color <hex>
hypertask task update PROJ-123 --add-labels "QA"      # keeps the others
hypertask task update PROJ-123 --remove-labels "QA"
```

`--labels` replaces the whole set. Use the add and remove forms.

## Columns

```bash
hypertask section create --project 42 --title "Review" --after <sectionId>
hypertask section rename --project 42 --section <sectionId> --title "In Review"
hypertask section reorder --project 42 --section "Review" --after "Todo"
hypertask section done --project 42 --section "Shipped"   # marks a column as finished work
```

Changing columns affects everyone on the board. Ask the board owner first. Deleting a column needs a yes.
