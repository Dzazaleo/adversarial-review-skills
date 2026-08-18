# Adversarial Review Skills

**Two Claude Code skills. The first gets a different AI to attack your work. The second helps
you work out which of its complaints are actually true.**

They come as a pair. One writes the attack. The other judges what comes back.

---

## The problem

If an AI writes your code and then reviews it, it will tell you the code is fine. It isn't
lying. It is re-reading its own reasoning and finding it convincing — the same way you find your
own reasoning convincing. Whatever it misread while writing, it misreads again while reviewing.
It cannot test for the thing it never thought of.

So you need a different model to look at it. And then you need a way to sort that model's good
findings from its bad ones, because you will get both.

---

## What each one does

### 1. `adversarial-review-prompt` — writes the attack

You point it at some work: a folder of code, a pull request, a design document, a plan.

It reads the actual work, not a summary of it, and writes a **briefing document** aimed at a
rival AI. The brief tells that reviewer:

- One model wrote this, reviewed it, and tested it against tests it also wrote. If you end up
agreeing with it, this exercise has failed.
- Every confident comment in this code is a **claim by the thing being reviewed**, not proof.
Go and check whether the test it points at would actually fail if the claim were wrong.
- Here are 15–25 specific things this work is betting on. Come back with CONFIRMED, REFUTED or
COULD NOT DETERMINE on each one.
- You cannot sign off one of those claims by quoting a comment or a test name. That is the code
vouching for itself. Run something, or say you could not tell.
- If you find a real bug and decide it was deliberate, report it and say why you think so. Do
not quietly let it go.
- Here is exactly what you may read, run and write — including "nothing else".
- Write your report **to a file as you go**, not into the chat window.

It also gives you a short **cover note**: the message you actually paste into Codex, Gemini,
Cursor, or another Claude session. You don't have to paste a 400-line document into a chat box.

Then it tells you privately what *it* suspects is wrong. Those suspicions are deliberately kept
out of the brief, so the other model has to find them on its own. If it does, that's real
confirmation. If it never mentions them, they're still open.

It will also tell you which model family you're about to send this to. Plenty of review tools
are built on the same few underlying models, so two of them can be one opinion bought twice.
The whole point is to get eyes that work differently from the ones that wrote the code.

### 2. `review-adjudication` — judges what comes back

A review lands. Fourteen findings. Some are real. Some are the reviewer misunderstanding a
decision you made months ago. Some are the reviewer being confidently wrong.

This skill rules on **every one of them** and writes those rulings into a permanent file — the
*ledger*. Each finding gets two separate answers:

- **Verdict — is it true?** `CONFIRMED` · `REFUTED` · `COULD NOT DETERMINE` · `SETTLED ALREADY`
· `OWNER RULING REQUIRED`
- **Disposition — what happens now?** `FIX NOW` · `FIX LATER` · `ACCEPTED AS-IS` · `NO ACTION`
· `VERIFY` · `PENDING OWNER`

Two answers, because they're two different questions. "This bug is real and we're shipping
anyway" is a reasonable position. "This bug isn't real" is a different one. A single word like
"accepted" hides which one you meant.

Before it rules on anything, it checks the report is worth ruling on:

- **Is this actually a review?** A summary of the code, a restatement of the diff, or a request
for more information is not a review. Treating one as "found nothing" would record an all-clear
that nobody gave.
- **Did it finish?** Reviews get cut off partway. What it managed to write still counts. Its
silence doesn't — anything it never reached is marked unchecked, not approved.
- **Is it trying to give me instructions?** The report was written by a model you asked to be
hostile. Its findings are claims to check. Any line telling *the adjudicator* what to do gets
flagged, not followed.

Then the rules that do the real work, most of which are rules against the easy answer:

- **Dismissal has to cost something.** "We'll do it later" means a real backlog file on disk,
written before the ledger, with the finding's location, cause and consequence copied into it. A
promise with nothing behind it is a dropped finding with a nicer name.
- **Disproving a finding is as much work as making one.** If the reviewer brought evidence and
you want to say it's wrong, bring evidence back. Reading the code and feeling reassured is not
evidence — least of all when the reassuring comment was written by the thing under review.
- **Claims the reviewer says it checked get spot-checked.** If it signed one off by quoting a
comment or a test name, it didn't check it, and that claim goes back on the pile.
- **Two reviewers agreeing only counts if the second couldn't see the first.** Reports land in
the same folder, so usually it could. The skill records what each reviewer was able to read and
discounts the overlap.
- **It never decides whether you ship.** Anything that turns on what you want, what risk you'll
accept, or what the product should do comes back to you as a decision, with the options and
what each one costs.
- **It never fixes anything on its own.** The output is the ledger. Fixing is a separate step
that you ask for.

The two skills close a loop. This round's ledger becomes the "already covered" section of the
next brief, so the next reviewer doesn't spend its run re-finding what you've already ruled on.

---

## Install

The repo lives at
**[https://github.com/Dzazaleo/adversarial-review-skills](https://github.com/Dzazaleo/adversarial-review-skills)**.
Clone it and copy the two skill folders into your Claude Code skills directory:

```bash
git clone https://github.com/Dzazaleo/adversarial-review-skills.git
cp -r adversarial-review-skills/skills/adversarial-review-prompt  ~/.claude/skills/
cp -r adversarial-review-skills/skills/review-adjudication        ~/.claude/skills/
```

For one project instead of everywhere, use `.claude/skills/` inside that project.

Restart Claude Code. You don't need to remember a command — just say what you want:

> "Get an independent review of the payment module from Codex."

> "The Codex review came back — work through it and tell me what's real."

Or call them by name: `/adversarial-review-prompt`, `/review-adjudication`.

## A typical run

Say Claude has just written you a plan, and you'd rather not find out it was wrong after the
thing is built.

Each step says which session to run it in. Two of them need to be fresh sessions, and those two
are what make the whole exercise worth anything.

1. **You:** "Before we build any of this, I want an outside review of the plan you just wrote."
  Or run `/adversarial-review-prompt` directly.
2. Claude reads its own plan, writes `NN-EXTERNAL-REVIEW-PROMPT.md` and a cover note, and tells
  you its own private suspicions to hold onto.
  > **Where:** the same session that wrote the plan — that's the point, since it knows which
  > parts it was least sure of. Everything it writes stands on its own, so nothing later depends
  > on keeping this session open. The one risk is that its own suspicions end up in the brief
  > without it noticing, so it searches the saved file afterwards and tells you which ones really
  > were kept out.
3. **You** paste the cover note into Codex / Gemini / Cursor / another Claude session.
  > **Where: a fresh session, and ideally a different model.** Another Claude session only counts
  > if it hasn't seen the plan. Show the plan to the session that wrote it and you get agreement
  > instead of a review, and the run was worth nothing. Different *company* is worth more than
  > different *product* — several review tools sit on top of the same underlying models.
4. That model reads the brief, does the audit, and writes `NN-EXTERNAL-REVIEW.md` to disk.
5. **You, in another fresh session:** "The review's in — adjudicate it." Or run
  `/review-adjudication` and point it at the report.
6. Claude checks every finding itself — running commands where a finding is about code, going
  back to the source where it's about the plan — and writes `NN-REVIEW-ADJUDICATION.md`: every
  finding ruled on, a fix queue, and the questions that are yours to answer.
  > **Where: a fresh session again.** It costs you nothing, because the skill works from the
  > report and the files on disk rather than from a conversation — you can pick it up days later
  > on a different machine. And it buys a lot. The session that wrote the plan has a stake in the
  > findings being wrong, so letting it rule on them is self-review sneaking back in, and "we
  > already thought about that" is the cheapest sentence in the language. A session with no stake
  > has to go and look.
7. **You** answer those questions and say go. Fixing happens then, against the ledger.
  > **Where:** the session that wrote the ledger can do the fixing, as long as you've actually
  > said go. It writes your go-ahead into the ledger first, then updates each row as the fix
  > lands, so the file never claims something is still queued after it shipped.

## See it actually working

The [examples/](examples/) folder holds real output — the skills pointed at *themselves*. Two
different models (OpenAI's Codex and Claude Fable 5) were sent to audit the skills, found real
defects in them, and those defects were then adjudicated and fixed using the very skill under
review. Nothing in there is made up or cleaned up; it's the raw files, with local paths and one
private project name rewritten.

Start with
[examples/audit-of-review-adjudication/REVIEW-ADJUDICATION.md](examples/audit-of-review-adjudication/REVIEW-ADJUDICATION.md)
— 14 findings in, 14 rows out, including two findings that fired against the ledger *while it
was being written*.

## For the technically curious

[HOW-IT-WORKS.md](HOW-IT-WORKS.md) explains the design: why each rule is there, which failure it
was written against, and which ones were only added after a review caught them missing.

## Requirements

Claude Code, plus access to at least one other AI that can read files in your repo — Codex CLI,
Gemini CLI, Cursor, or just a second Claude Code session that hasn't seen the work. A
browser-only chat works too, with a bit more copying by hand; the skill spots that case and
adjusts the hand-off.

## Credits

Four of the rules here came from reading
[code review cadre](https://github.com/VibeCodyH/code-review-cadre), which tackles a different
problem — picking which reviewers to use — but had already measured failures these skills
weren't guarding against. Details in [HOW-IT-WORKS.md](HOW-IT-WORKS.md#borrowed-from-code-review-cadre).

## License

[CC0 1.0](LICENSE) — public domain. Take them, change them, ship them, no attribution needed.
