---
name: hypertask-comments
description: Write Hypertask ticket comments that people read and answer. Use when the user says "comment on the ticket", "ask a question on the ticket", "post the result", "reply to", "mention", "react", or when a session needs a decision from a person through the board instead of chat.
---

# Comments with the `hypertask` CLI

A comment is for a person. Chatter to yourself (plans, retries, test runs) does not belong there.

```bash
hypertask comment list PROJ-123
hypertask comment add PROJ-123 --text '<p><strong>Fixed.</strong> Export works on Safari 18.</p>'
hypertask comment add PROJ-123 --file note.html --attach shot.png
```

## Shape

- **Verdict first**, in bold: what happened or what you need. Details after.
- Short sentences, plain words, one idea each.
- Bodies are HTML (`<p>`, `<ul>`, `<strong>`). `--markdown` sends Markdown.
- Images go through `--attach`, never inline.
- When work continues, end with `Next:` and say the next step and who does it.

## Kinds

`--kind` marks a comment the board shows to people:

| Kind | Use |
|---|---|
| `question` | You are blocked on a decision only a person can make. |
| `qa` | A test verdict, or a state note before you wait on CI or a person. |
| `done` | The closing summary once the work is live. |

An agent comment without `--kind` may be filed as log chatter and notify nobody.

## Ask a question people answer

1. Start the text with `Question:`.
2. **@mention** the person with a real mention. Find them with `hypertask project members <boardId>`. Only a real mention reaches their inbox.
3. Ask one yes/no or one pick-from-options question. Give your recommendation and why.
4. Post it with `--kind question`, then stop. Do not repeat it while you wait.

An emoji reaction is an answer: a thumbs-up on your unedited question is a yes. Before you ask again, re-read with `hypertask comment list PROJ-123 --json` and check reactions and new comments.

## React, edit

```bash
hypertask comment react <comment-id> --emoji 👍
hypertask comment update <comment-id> --text 'new text'
```

Do not edit a comment someone already answered. Post a new one. Delete only your own mistakes.

## Drafts

`hypertask draft create PROJ-123 --comment --text '...'` saves a draft. `hypertask draft publish <draft-id>` posts it. Use a draft when a person should approve the words first.
