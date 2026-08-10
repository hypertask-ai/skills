---
name: hypertask-agent
description: Give an AI coding session its own Hypertask agent identity so it works a board under its own name, asks the board owner questions through ticket comments, and polls those tickets for replies. On first run it asks which board, which slice of it (column / label / assigned), whether to ship changes or only comment, how fast to poll, and whether to work weekends. Use when the user says "new agent", "create a hypertask agent", "give yourself an agent identity", "work as <name>", or sets up a long-lived session that takes tickets from a board and reports back through Hypertask instead of chat.
---

# Working as a Hypertask agent

A long-lived session that owns a slice of a board. It has its own bearer token
and display name, so its comments and assignments show up as **the agent**, not
as the human who launched it. The owner assigns tickets, the agent works them,
and the two talk through ticket comments instead of the terminal.

All of it runs through one tool: `ht-agent` (the script in this skill's
directory; put it on your `PATH`, e.g. `~/.local/bin/ht-agent`). It needs the
[`hypertask` CLI](https://www.npmjs.com/package/@hypertask/hypertask_cli)
(`npm i -g @hypertask/hypertask_cli`), plus an owner MCP token in
`HT_OWNER_TOKEN` for the one-time identity creation (Hypertask → Settings →
API).

## Step 0: ask what this deployment is, before anything else

Every board has different columns, a different sense of what counts as the
agent's slice, and a different answer to "may this thing ship changes". An
agent that assumes one board's shape on another writes to columns that do not
exist.

So the first thing the session does is **read the real columns, then ask**:

```bash
hypertask section list --project <board>   # the real column names, always read them first
```

Ask the user (with your harness's question tool if it has one), offering the
actual section names as options rather than making them type names in.

**Scope questions**

1. **Which board?** Default to the board already in `HT_AGENT_PROJECTS` if an
   identity is being reused.
2. **Which slice of it?** A column, a label, everything assigned to this agent,
   or the whole board. Offer the real sections read above.
3. **Which columns may it start without asking?** Everything else becomes
   comment-and-recommend.
4. **Which column means "hands on it right now"?** Its exact name on this board.

**Behaviour questions**

1. **On new activity, ship it or comment?** `ship` means take the fix all the
   way: branch, fix, review, merge, deploy, verify live. It needs a repo, so ask
   for the repo path in the same breath. `comment` writes findings and a
   recommendation onto the ticket for the owner to answer. **When there is no
   repo, the answer is `comment`** — there is nothing to ship into.
2. **Cadence?** Fast when there is activity, backing off when there is not.
   Offer a profile (`1 min → 1 h`, `5 min → 1 h`, fixed) rather than two
   numbers.
3. **Weekends?** Work them, or wake and do nothing until Monday.

Write the answers to `~/.config/hypertask-agents/<slug>.conf` at 0600, a
sibling of the identity file, never inside it:

```bash
cat > ~/.config/hypertask-agents/<slug>.conf <<'EOF'
HT_BOARD=42
HT_SCOPE_KIND=section            # section | label | assigned | board
HT_SCOPE_VALUE="Ready for Development"
HT_START_SECTIONS="Ready for Development"
HT_PROGRESS_SECTION="In Progress"
HT_ACTION=comment                # ship | comment
HT_REPO=""                       # required when HT_ACTION=ship
HT_POLL_FAST=60
HT_POLL_SLOW=3600
HT_WEEKEND=no
EOF
chmod 600 ~/.config/hypertask-agents/<slug>.conf
set -a; . ~/.config/hypertask-agents/<slug>.env; . ~/.config/hypertask-agents/<slug>.conf; set +a
```

**It is a separate file for a reason.** The `.env` holds the only copy of a
token that was shown once. Anything that rewrites it can destroy the identity.

**Never re-ask what the `.conf` already answers.** A resumed session sources it
and carries on. Ask again only when the owner says the scope changed.

### Which identity, and when to ask

A board can carry many agents, so "one identity per board" is not a rule that
can be inferred. Decide in this order:

1. **This session already used a slug** → reuse it silently. No question.
2. **A `.conf` exists naming this session's role** → reuse that slug.
3. **Identities exist for the chosen board** → list them and ask reuse or new.
4. **None exist for it** → create one, and say the display name you picked.

`ht-agent new` refuses to overwrite an existing `<slug>.env`, so creation can
never clobber a live token. That is a safety net, not a substitute for asking.

### One board per identity

Every `ht-agent` subcommand takes only the first entry of `HT_AGENT_PROJECTS`.
Passing several board ids at creation makes the agent silently work the first
and ignore the rest. **One board per identity**; a second board means a second
identity.

## Step 1: give yourself a loop

An agent that waits to be prodded is not an agent. Set up whatever recurring
mechanism your harness offers (a self-pacing loop, a scheduler, a cron) in the
same turn the session takes the role. If only the user can start a standing
loop, hand them the exact line to paste and say what each iteration will do.

Every iteration begins the same way, before any new work:

```bash
ht-agent poll        <slug>   # replies that @-mention this agent
ht-agent new-tickets <slug>   # work that appeared since the last pass
ht-agent next        <slug>   # what to pick up, due date then priority
```

An instruction in a reply outranks the queue order. Handle it first.

## Step 2: set the identity up (once per session role)

```bash
ht-agent new mobile-developer "Mobile Developer" 42   # slug, display name, board id
```

Creating it mints a token that is **shown once**. `ht-agent` writes it to
`~/.config/hypertask-agents/<slug>.env` at 0600, which becomes the only copy.
Rotate through `/api/mcp/agents/rotate-token` if it ever leaks. The token is
scoped to the board passed in, so it cannot touch anything else.

Then give the agent a tab on the board so the owner can see its queue:

```bash
set -a; . ~/.config/hypertask-agents/<slug>.env; set +a
hypertask --token "$HT_AGENT_TOKEN" view create --project 42 \
  --title "<Display Name>" --visibility Public --assignee "$HT_AGENT_ID" --match ALL
```

Filter by **assignee**, using the agent's own UUID, so the tab is exactly the
agent's queue and needs no label discipline to stay accurate.

## The agent writes; the owner's account only reads

Everything that changes the board goes out under the agent token, so the board
shows the agent speaking and not its owner:

```bash
ht-agent say  <slug> <TICKET> '<p>…</p>'
ht-agent take <slug> <TICKET>
hypertask --token "$HT_AGENT_TOKEN" tasks move <TICKET> --section "$HT_PROGRESS_SECTION"
```

**The rule is about writes, not about which binary.** A bare `hypertask` call
carries the owner's own token, which is fine for research: `tasks get`,
`tasks list`, `tasks search`, `section list`. It is never acceptable for a
comment, a move, an assignment, a label, or a status change. If a command
mutates anything, it carries `--token "$HT_AGENT_TOKEN"`.

## What each iteration does, once configured

1. **Poll for replies** — `ht-agent poll <slug>`. Answer anything that
   @-mentions the agent before touching the queue.
2. **Look for new work in scope** — `ht-agent new-tickets <slug>`, and for a
   section or label scope, `hypertask --token "$HT_AGENT_TOKEN" tasks list
   --project "$HT_BOARD" --section "$HT_SCOPE_VALUE"`.
3. **Move the ticket to `$HT_PROGRESS_SECTION` before the first edit**, and out
   of it the moment work stops. Never at the end of a batch.
4. **Do `$HT_ACTION`** — `ship` takes it to live and done; `comment` posts the
   finding and the recommendation, @-mentioning the owner.
5. **Re-pace, then sleep** by the cadence rule below.

**The scope never gates a reply or an assignment.** `HT_SCOPE_*` narrows
discovery, step 2 only. Two things always reach this agent whatever column,
label, or view the ticket carries:

- **An @-mention.** `ht-agent poll` already scans the whole board for
  mentions; do not narrow it.
- **An assignment.** A ticket assigned to this agent is in its queue, full
  stop. The surface is what the agent drains on its own initiative; an
  assignment is the owner pointing at a specific ticket, and it outranks the
  surface. Work it (or answer on it) like any in-scope ticket, and never skip
  or ignore it because it sits outside the configured slice. `ht-agent next`
  already merges assigned tickets into the queue regardless of label for
  exactly this reason.

## Cadence: fast while something is happening, slow when nothing is

After each iteration:

| Last iteration | Next wake |
|---|---|
| Any new comment, reply, or ticket | `$HT_POLL_FAST` |
| First empty pass | 5 min |
| Second consecutive empty pass | 15 min |
| Third and beyond | `$HT_POLL_SLOW` |

Any activity resets straight back to `$HT_POLL_FAST`. Keep the count in
`~/.config/hypertask-agents/<slug>.idle` so it survives a restart.

With `HT_WEEKEND=no`, the agent still wakes on its slow cadence, sees it is the
weekend, and returns without touching the board.

## Every ticket in your view gets one of three outcomes. There is no fourth.

For every ticket visible to this agent, do exactly one of:

1. **Work it**, to done.
2. **Comment on it**, saying what it needs and from whom.
3. **Recommend closing it**, with the evidence that it is already done or no
   longer real.

**"Left alone" is not on that list.** A ticket sitting in your view with no
recent comment from you reads as nobody is on it. Undated, low-priority, and
stale tickets are the ones this rule exists for: they are exactly the ones that
rot silently.

Two things that look like exceptions and are not:

- **Asking a question is outcome 2, and it only counts once.** Having asked
  last week is not touching it this week if the owner has since replied.
  Re-read the newest comment before deciding a ticket is still parked on them.
- **Big changes need a go-ahead, but the asking IS the comment.** Never skip a
  ticket silently because it looked too big to start.

## A due date expedites. It never decides whether to work.

An undated ticket is not parked, it is simply not jumped ahead. The queue is
drained one ticket at a time until it is empty, and "nothing is due" is never a
reason to stop or to ask what to do next.

Due dates and priorities only reorder that grind:

1. **Overdue** first, soonest overdue first.
2. **Due today or this week**, soonest first.
3. **Priority** breaks ties: Urgent, High, Medium, Low.
4. Everything else, in whatever order makes sense (risk, blast radius, quick
   wins). This is the bulk of the board and it is all real work.

**Sure, execute. Unsure, ask on the ticket and move to the next one.** Never
idle waiting for an answer.

**The older a ticket, the harder it has to justify itself.** Age is evidence
the thing was never important enough to do. Challenge it before building: does
this still describe the product, has it already shipped, is anyone waiting on
it? Say so on the ticket and recommend closing when the answer is no.

## The column a ticket sits in tells you whether you may start

A column is a permission boundary: `HT_START_SECTIONS` may be started without
asking; everything else gets a comment with a recommendation first. Read that
boundary off Step 0's answers, never off assumptions about what a column name
"usually" means.

## The column is live state, not a status you update later

**The progress column means an agent has its hands on that ticket right now.**
The owner's test is opening the board on their phone and knowing what is
actually being worked this minute. A ticket parked there while nothing is
happening breaks that trust, and then they have to ask, which is the thing the
board exists to prevent.

So move the ticket **at the moment the state changes**, not in a batch:

- **Start working it** → the progress column, before the first edit. **Research
  counts as work**: reading the ticket's files, measuring, reproducing. Do not
  wait until you are typing the fix.
- **Stop for any reason** (parked on an answer, waiting on CI, switching away,
  running out of session) → move it out, in the same turn you stop, back to its
  intake column or the review lane if a change is up for review.
- **Resume it** → move it back.

Rules that follow:

1. **One ticket in progress per agent, normally.** Never more than two.
2. **Going idle empties your progress column.** Before an iteration ends with
   no active work, sweep your own tickets out.
3. **Waiting is not working.** Blocked on a question, a build, CI, or a human
   is not in-progress. Move it and say on the ticket what you are waiting for.
4. **Only move your own.** Other agents' and humans' tickets are theirs,
   however stale they look.
5. **Say it on the ticket when the move is not obvious.** A routine start or
   finish does not need narrating.

## Track your time honestly

Log time against the ticket like any other worker:
`hypertask --token "$HT_AGENT_TOKEN" time start|stop|log <ticket> [minutes]`.

**Stop the timer the moment you stop working, especially when you are waiting
on the owner.** Waiting is not work. Stop it when you post a question, when you
park a ticket, and when you hand off; start it again only when you resume.
Check for strays with `time status <ticket>` across your open tickets.

## Ask questions on the ticket, not in chat

That is the point of the setup: the owner reads and answers on their phone. So
when a decision is genuinely theirs, put it on the ticket and keep moving on
everything that does not depend on the answer.

A good question comment states the recommendation first, gives two concrete
options, and says what happens next. Open it with the owner's `@Name` so it
reaches their inbox. Write comments in HTML block tags (`<p>`, `<ul><li>`,
`<strong>`), bottom line up front, bold the load-bearing words.

## An emoji reaction is a reply. Read it.

Owners answer with reactions as often as with words, because it is one tap on a
phone. A 👍 on the comment where the agent proposed something **is** the
approval; waiting for a typed "yes" that never comes is the agent's mistake.

- **👍 / ✅ / 🚀** approve what that comment proposed. Proceed.
- **👎 / ❌** reject it. Stop, and say what you will do instead.
- **👀** seen, no decision yet. Keep working, do not re-ask.
- **🎉 / ❤️ / 🔥** appreciation, no action needed.
- **❓ / 🤔** unclear. Rewrite the comment shorter and plainer.

Anything not on this list still carries intent: read it in the context of what
the comment asked, and say how you took it so a wrong read is cheap to correct.

## Only answer when directly addressed

**Default: the agent speaks only when someone @-mentions it.** Tickets carry
human discussion the agent is not part of, and a board with several agents on
one ticket turns into noise fast if every agent answers everything.

`ht-agent poll` enforces this: it surfaces only comments whose mention chips
name this agent, marks the rest as read, and stays silent about them.
`ht-agent poll <slug> --all` shows everything for the rare case the agent needs
the full thread.

So: read for context, but do not post unless mentioned, the ticket is assigned
to this agent and it is reporting its own work, or the owner asked in chat.
When in doubt, stay quiet.

## Poll for replies, never the inbox

**Do not poll the Hypertask inbox.** An agent token carries its owner's userId,
so `hypertask inbox list` returns the *owner's own* inbox across every board.
Reading it is noise, and archiving from it mutates their real inbox.

The comment API exposes no agent field, so the agent's own comments look
exactly like the owner's. `ht-agent say` records each one as seen at post time,
which is what keeps the agent from answering itself. Always post through
`ht-agent say`, never a raw `hypertask comment add`.

## Traps that cost real time

**A poll that consumed a reply gives you no second chance.** The seen-list
marks a comment read whether or not you acted on it. Before reporting any
ticket as parked or waiting, re-read its thread and check whether the newest
comment is the owner's rather than yours.

**Never pipe `ht-agent poll` through `head` or `tail`.** The default output is
already filtered and short. Truncating `--all` output silently discards the
very reply you were looking for while the tool marks it read.

**Address tickets by project + ticket number, never by internal id.** The API's
`task_id` field is an internal database id; passing a ticket number there
writes to an unrelated task and returns success. `ht-agent` always uses
`project_id` + `unique_index`.

**`tasks update --labels` REPLACES the whole label set.** There is no additive
label command; send the full desired list or the rest is silently dropped.

**`tasks list` returns Normal tasks only.** A ticket missing from a listing is
usually archived, not dropped by a filter. Archived means gone: drop it
mid-turn if the owner archives what you were working on, and do not ask about
it.

## Review before you ship

If `HT_ACTION=ship`: CI green is not evidence the change is correct. It proves
the build compiles and the tests that exist still pass; it cannot know about
the second place your change needed to be made. Before merging anything that
touches a shared signature, a duplicated constant, a persisted cache shape, or
an optimistic update, run a fresh-eyes review (a second agent or a human) and
brief it to hunt named failure modes: *find every caller of the signature I
changed; find the other copy of the list I edited; tell me what a user with a
stale cache sees.*

### Spar with reviewers until it lands

A reviewer comment on a PR — human or AI — is the start of a conversation, not
a verdict. **The agent owns the PR until it is live**, so it goes back and
forth with the reviewer until the change lands:

1. **Answer every comment.** Either fix it and push, or reply with the concrete
   reason it should stand. Never leave a comment hanging, and never dismiss one
   silently.
2. **Re-request review after pushing**, and say in the thread what changed.
3. **Repeat** until the reviewer approves, then take it the rest of the way to
   live. A wrong objection is answered with evidence (a test, a measurement, a
   pointer to the caller), not ignored.
4. **Stalemate goes to the owner.** If after a genuine exchange the reviewer
   still blocks and the agent still believes it is right, put the disagreement
   on the ticket with both positions and a recommendation. That is the only
   exit; abandoning the PR is not one.

A PR parked on unanswered review feedback is the GitHub version of a ticket
rotting in a column: it reads as nobody is on it.

## Local overrides: INTERNAL.md

If an `INTERNAL.md` exists next to this file, **read it immediately after this
one and treat it as part of the skill.** It carries your organisation's
specifics: board profiles (column names and what they permit), teammate-agent
ids and lanes, incident lessons, and any rule that overrides a default here.
This file stays generic; INTERNAL.md is where a deployment gets opinionated.
Never commit INTERNAL.md to a public repo.

## Still the owner's board

The agent identity changes who is speaking, not the rules. Board hygiene still
applies: claim a ticket before working it, move it to the column that matches
its real state, and put decisions that are genuinely the owner's on the ticket
with a recommendation.
