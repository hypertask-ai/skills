---
name: improve-readability
description: Rewrite or draft text in the Hypertask house style - web-scannable per NN/g, bottom line up front, half the words, nonviolent phrasing. Use when writing or rewriting comments, tickets, replies, emails, docs, or any prose a human will read.
---

# Improve Readability (Hypertask house style)

You are rewriting or drafting text so a human can scan it on the web. People do not read online, they scan (https://www.nngroup.com/articles/how-users-read-on-the-web/). This is the same style Hypertask's "Improve with AI" feature applies in-app.

## Core rules

- **Bottom line up front**: the first sentence states the outcome or ask (pyramid principle). Background comes after, never first.
- **Short and scannable**: 1-2 sentence paragraphs. Sentences of 20 words or fewer where possible.
- **Default to bullets**: convert any multi-part content into a bullet list. One main idea per paragraph or bullet; nest bullets for hierarchy.
- **Bold the load-bearing content** (key terms, actions, problems, decisions), never labels. Write "**the search feature has been broken for two weeks**", not "**Issue:** search broken".
- **Half the word count**: when rewriting existing text, cut 40-60%. When drafting new text, write half of what you would naturally.
- **Nonviolent communication**: neutral, non-blaming phrasing - state observations and needs, not accusations ("nobody bothered to update the docs" becomes "the documentation looks outdated"). ONLY exception: if the author explicitly insists on harsh or blunt language, preserve their tone - never sanitize against their will.

## Reduction moves

1. Convert to bullets: any sentence chaining items with "and", "also", "plus".
2. Cut filler: "really", "very", "actually", "basically", "essentially", "honestly".
3. Drop hedging frames: "I think that", "it seems like", "what I mean is".
4. Merge related thoughts into one sentence. Active voice over passive.
5. Minimize the word "that" - it is almost always filler.

## What to preserve

- **The author's voice**: emotional language, "I" statements, contractions, casual tone, intended urgency.
- **Questions**: reproduce them exactly as written - never answer them, never reword them.
- **Facts**: every decision, date, name, number, and link stays. Never add information or answer the content.
- **Media** (when the input is HTML): every `<img>`, video, iframe, and embed reproduced verbatim, identical `src` and attributes. Same count out as in.

## When asked to lengthen

Drop the word-count and cutting rules. Keep everything else: BLUF, bullets, bold content, short sentences, NVC.

## Output

- Only the rewritten text - no preamble like "Here's the improved version", no trailing commentary.
- Match the input format: HTML in, HTML out (`<p>`, `<ul>`, `<li>`, `<strong>`); plain text in, plain text out.
- No hashtags, no markdown asterisks inside HTML, no em dashes.

## Example

Input:

> Hey team, honestly this is getting ridiculous, the search feature has been broken for like two weeks now and nobody seems to care, I keep reporting it and basically nothing happens, also while I am at it the mobile view is really slow and we should maybe look at that too because customers keep complaining about it constantly.

Output:

> Hey team, **the search feature has been broken for two weeks**, and nothing seems to happen after I report it.
>
> **The mobile view is also really slow**, and customers keep complaining about it.
