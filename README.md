# Adversarial Review Skills

**Two Claude Code skills that get a *different* AI to attack your work, and then help you
decide which of its complaints are actually true.**

They are a pair. The first one writes the attack. The second one judges what comes back.

---

## The problem they solve

If you let an AI write your code and then ask that same AI to review it, it will tell you the
code is good. Not because it is lying — because it is re-reading its own reasoning and finding
it convincing, the same way you find your own reasoning convincing. It carries the same
misreadings into the review that it had while writing. It never tests the thing it never
thought of.

---

## What each one does

### 1. `adversarial-review-prompt` — writes the attack

You point it at some work: a folder of code, a pull request, a design document, a plan.

It reads the actual thing — not a summary of it — then writes a **briefing document** aimed at
a rival AI. The brief tells that reviewer, in plain terms:

- Everything here was written, reviewed and tested by *one* model. Agreement is a failed result.
- Every confident comment in this code is a **claim by the party under review**, not evidence.
  Go check whether the test it cites would actually fail if the claim were false.
- Here are 15–25 specific things this work is betting on. Come back with CONFIRMED, REFUTED,
  or COULD NOT DETERMINE on each one.
- Here is what you may read, run, and write — exactly, including "nothing else."
- Write your report **to a file as you go**, not in the chat window.

It also hands you a short **cover note** — the actual message you paste into Codex, Gemini,
Cursor, or another Claude session. You don't have to paste a 400-line document into a chat box.

Then it tells you privately what *it* suspects is wrong — deliberately kept out of the brief,
so the other model has to find those things on its own. If it does, that's real corroboration.
If it never mentions them, they're still open.

### 2. `review-adjudication` — judges what comes back

A review lands. It has fourteen findings. Some are real, some are the reviewer misunderstanding
a decision you made months ago, and some are the reviewer being confidently wrong.

This skill rules on **every single one**, and writes those rulings into a permanent file — the
*ledger*. Each finding gets two separate answers:

- **Verdict — is it true?** `CONFIRMED` · `REFUTED` · `COULD NOT DETERMINE` · `SETTLED ALREADY`
  · `OWNER RULING REQUIRED`
- **Disposition — what happens now?** `FIX NOW` · `FIX LATER` · `ACCEPTED AS-IS` · `NO ACTION`
  · `VERIFY` · `PENDING OWNER`

Two questions, because they are genuinely different. "This bug is real and we are shipping
anyway" is a legitimate position; "this bug is not real" is a different one; and a single word
like "accepted" hides which of the two you meant.

The rules that make it work are mostly rules against the *easy* answer:

- **Dismissal has to cost something.** "We'll do it later" requires an actual backlog file, on
  disk, before the ledger is written — with the finding's location, mechanism and consequence
  copied into it. A bare promise is a drop wearing a deferral label.
- **Disproving a finding is as hard as making one.** If the reviewer produced evidence and you
  want to say it's wrong, you produce evidence too. Reading the code and feeling reassured is
  not evidence — especially when the reassuring comment was written by the thing under review.
- **It never decides whether to ship.** Questions that turn on what you want, what risk you'll
  take, or what the product should do get handed back to you as a decision, with options and
  costs.
- **It never fixes anything on its own.** The output is the ledger. Fixing is a separate,
  deliberate act afterwards.

And the two skills close a loop: the ledger from one round becomes the "ground already walked"
section of the next brief, so the next reviewer doesn't waste its run re-finding what you
already ruled on.

---

## Install

Copy the two skill folders into your Claude Code skills directory:

```bash
git clone <this-repo> adversarial-review-skills
cp -r adversarial-review-skills/skills/adversarial-review-prompt  ~/.claude/skills/
cp -r adversarial-review-skills/skills/review-adjudication        ~/.claude/skills/
```

For a single project instead of everywhere, use `.claude/skills/` inside that project.

Restart Claude Code. Both skills are model-invoked — you don't need to remember a command, you
just describe what you want:

> "Get an independent review of the payment module from Codex."

> "The Codex review came back — work through it and tell me what's real."

Or invoke them by name: `/adversarial-review-prompt`, `/review-adjudication`.

## A typical run

1. **You:** "I want an outside review of `src/importer/` before I ship it."
2. Claude reads the code, writes `NN-EXTERNAL-REVIEW-PROMPT.md` and a cover note, and lists its
   own private suspicions for you to hold onto.
3. **You** paste the cover note into Codex / Gemini / Cursor / another Claude session.
4. That model reads the brief, does the audit, and writes `NN-EXTERNAL-REVIEW.md` to disk.
5. **You:** "The review's in — adjudicate it."
6. Claude re-verifies each finding by actually running things, and writes
   `NN-REVIEW-ADJUDICATION.md`: every finding ruled, a fix queue, and the questions that are
   yours to answer.
7. **You** answer those questions and say go. Fixing happens then, against the ledger.

## See it actually working

The [`examples/`](examples/) folder holds real output — the skills pointed at *themselves*.
Two different models (OpenAI's Codex and Claude Fable 5) were sent to audit the skills, found
real defects in them, and those defects were adjudicated and fixed using the very skill under
review. Nothing there is illustrative or made up; it is the raw artifacts, with local file
paths and one private project name rewritten.

Start with [`examples/audit-of-review-adjudication/REVIEW-ADJUDICATION.md`](examples/audit-of-review-adjudication/REVIEW-ADJUDICATION.md)
— 14 findings in, 14 rows out, including two findings that fired against the ledger *while it
was being written*.

## For the technically curious

[`HOW-IT-WORKS.md`](HOW-IT-WORKS.md) explains the design: why each rule is there, which failure
it was written against, and which of them were added only after a review caught them missing.

## Requirements

Claude Code, and access to at least one other AI that can read files in your repo — Codex CLI,
Gemini CLI, Cursor, or simply a second Claude Code session that hasn't seen the work. A
browser-only chat can be used too, with slightly more manual copying; the skill detects that
case and adjusts the hand-off.

## License

[CC0 1.0](LICENSE) — public domain. Take them, change them, ship them, no attribution needed.
