# Adversarial Review Skills

**Two Claude Code skills that work as a pair. One sends a rival AI to attack your work.
The other sorts the true complaints from the false ones.**

---

## Why they exist

If an AI writes your code and then reviews it, it will tell you the code is fine. It isn't
lying — it re-reads its own reasoning and finds it convincing, the same way you find yours
convincing. Whatever it missed while writing, it misses again while reviewing.

The fix is two steps: get a **different** model to look at the work, and then check what that
model says — because it will hand you a mix of real bugs, misunderstandings, and confident
nonsense, and you need to know which is which before acting on any of it.

One skill per step.

---

## Skill 1: `adversarial-review-prompt` — writes the attack

Point it at anything: a folder of code, a pull request, a plan, a design document. It produces
two files:

- **A briefing for the rival reviewer.** It reads your actual work — not a summary — and lists
  15–25 specific things the work is betting on, each one a claim the reviewer must go and test.
  It tells the reviewer the ground rules: prove findings by running things, don't trust the
  code's own comments as evidence, don't report style opinions, write the report to a file as
  you go, and here is exactly what you may read, run, and change (usually: nothing but the
  report file).
- **A short cover note.** The message you actually paste into Codex, Gemini, Cursor, or a fresh
  Claude session. You never paste the long brief into a chat box by hand.

Everything it suspects is wrong goes *into* the brief, as a sharp question the reviewer is pointed
at. There is no private list on the side. That used to exist — a chat-only message you were told to
save — and it was retired because on all four occasions anyone checked, the "private" suspicions
were already in the brief anyway. What replaced it costs nothing: the adjudicator assumes agreement
with the brief is the brief talking to itself, and re-proves those findings from scratch.

## Skill 2: `review-adjudication` — judges what comes back

The review lands with, say, fourteen findings. This skill rules on every single one and writes
the rulings into a permanent file called the **ledger**. Each finding gets two separate answers:

- **Is it true?** Confirmed, refuted, couldn't tell, already decided long ago, or a judgement
  call that belongs to you.
- **What happens now?** Fix it now, fix it later, accept it and ship anyway, or nothing.

Two answers, because "this bug is real but we're shipping anyway" and "this bug isn't real"
are very different positions, and one word like "accepted" hides which you meant.

The rules that do the real work are rules against taking the easy way out:

- **Nothing gets dropped.** Fourteen findings in means fourteen rulings out — including the
  ones the reviewer admitted it couldn't check.
- **"Later" has to cost something.** Deferring a finding means a real backlog file on disk,
  with the details copied in, before the ledger may say "later". A promise with nothing behind
  it is just a dropped finding with a nicer name.
- **Disproving takes as much evidence as proving.** To call a finding wrong, the skill has to
  run something and show the output — feeling reassured after re-reading the code doesn't count.
- **It checks the claim, not the sales pitch.** Each finding is stripped down to what it
  actually asserts before being tested, so a well-written false finding doesn't win and a
  badly-written true one doesn't lose.
- **Your past decisions are protected.** An outside reviewer can't see the choices you settled
  months ago, so it will reopen them. The skill screens those out — with a citation, so the
  screening itself can't become a way to dodge real findings.
- **It never decides for you.** Anything that turns on taste, risk, or what the product should
  do comes back to you as a plain question with the options and their costs. And it never
  fixes anything until you say go.

The two skills feed each other: this round's ledger tells the next round's reviewer what's
already been covered, so you never pay twice for the same finding.

---

## The process, start to finish

1. **You:** "Before we build this, I want an outside review." Claude writes the brief and the
   cover note. Everything it suspects goes into the brief, sharp — there is no separate list of
   hunches to keep, and nothing is held back to be scored later.
2. **You paste the cover note** into a different model — Codex, Gemini, Cursor, or a fresh
   Claude session that has never seen the work. Different company beats different product:
   many review tools run on the same few underlying models.
3. **The reviewer** reads the brief, does the audit, and writes its report to a file.
4. **You, in a fresh session:** "The review is in — adjudicate it." Claude re-tests every
   finding itself and writes the ledger: every finding ruled, a fix queue, and the short list of
   questions only you can answer. *(Fresh session, because the one that wrote the work has a
   stake in the findings being wrong.)*
5. **You answer the questions and say go.** Fixes happen then, against the ledger, and each
   ledger row is updated as its fix lands.

### When to use it

Not on every commit — that would grind development down. The high-value moments are few:
a plan before you build it, anything expensive to change later (a published API, a data
format, a security boundary), and once before shipping a milestone. One round at those points
buys most of the protection.

**Two rounds on a target, then stop.** After the second, whatever is still open goes on your
backlog and you close the thing. A third round takes you asking for one; left to itself the loop
does not end, and a review protocol nobody can afford to run is one that stops being run.

**Both skills run light by default.** Add `--deep` when it is genuinely worth it — a one-way door,
a high-severity finding you and the reviewer disagree about — and it turns on the heavier
machinery: corpus-digest checks, blind second opinions, echo tallies. The default path is: write
the brief, get the report, verify each finding, fix the blockers, backlog the rest.

---

## Install

```bash
git clone https://github.com/Dzazaleo/adversarial-review-skills.git
cp -r adversarial-review-skills/skills/adversarial-review-prompt  ~/.claude/skills/
cp -r adversarial-review-skills/skills/review-adjudication        ~/.claude/skills/
```

For a single project instead of everywhere, copy into that project's `.claude/skills/` folder.

**Keep the clone** — the calibration cases below live in the repo, not inside the skills.

**Re-syncing after an edit.** The copy direction is always this repo → `~/.claude/skills/`, and the
install flattens the `skills/` prefix (`skills/review-adjudication/` becomes
`~/.claude/skills/review-adjudication/`). Copy with `rsync -a --delete skills/<skill>/
~/.claude/skills/<skill>/` so removed files go too, then check it landed with
`diff -rq skills/<skill> ~/.claude/skills/<skill>`. Never edit the installed copy directly — that
is the version you actually run, and `scripts/validate.py` warns when the two drift apart.

Restart Claude Code. Then just say what you want:

> "Get an independent review of the payment module from Codex."

> "The Codex review came back — work through it and tell me what's real."

Or call them by name: `/adversarial-review-prompt`, `/review-adjudication`.

---

## What they're allowed to touch

Both skills declare read-only tools (`Read`, `Grep`, `Glob`) and nothing more. Every file they
create — brief, cover note, ledger, backlog entry — goes through your normal Claude Code
permission prompts, not a skill-level grant.

But note what that means: `allowed-tools` *grants*, it doesn't *restrict*. If your own settings
auto-approve edits, these skills' writes go through without stopping for you. Their written
rules about what they touch are instructions to the model, not a fence. If you want a real
fence, build it in your own settings by denying the paths you care about:

```json
{
  "permissions": {
    "deny": ["Edit(src/**)", "Edit(scripts/**)", "Edit(**/*.py)"]
  }
}
```

Two things worth knowing: write the rules as `Edit(path)` — Claude Code doesn't consult
`Write(path)` rules for file checks — and don't try a blanket deny with narrow allows, because
deny always wins and the skills couldn't write their own reports. For a true "nothing outside
this folder" boundary, use [the sandbox](https://code.claude.com/docs/en/sandboxing).

One more caution that applies to all skills, not just these: `allowed-tools` in a checked-in
skill isn't gated by workspace trust. Read the frontmatter of skills you didn't write.

---

## Test your reviewer once (20 minutes)

When a review comes back clean, you can't tell whether the work is sound or the reviewer never
really looked — both produce the same empty report, and the empty one is worse than nothing,
because it gets recorded as "covered".

The [calibration/](calibration/) folder settles it: six small pieces of work — four with
defects deliberately planted, two genuinely clean — that you hand to a reviewer once per model,
not once per review. If it finds the planted bugs and doesn't invent bugs in the clean ones,
it has earned some trust.

The result goes in `~/.adversarial-review/calibration/`, so it follows the reviewer to every
project on your machine rather than being re-earned in each one — the twenty minutes really is
paid once. Both skills look there and in the current project, and a record you drop into a
project's own `.adversarial-review/calibration/` wins, for teams that want one checked in.

Neither skill refuses to run without this. An untested reviewer's *findings* still count fully
— a real bug is real regardless of who found it. What an untested reviewer can't do is clear
anything: its "I checked, it's fine" is recorded as unverified, not as coverage.

---

## See real output

The [examples/](examples/) folder holds the skills pointed at *themselves*: two different
models were sent to audit these skills, found real defects, and the defects were adjudicated
and fixed using the very skill under review. Real reports and real rulings — the only edits were
absolute paths and one private project's name.

Start with
[examples/audit-of-review-adjudication/REVIEW-ADJUDICATION.md](examples/audit-of-review-adjudication/REVIEW-ADJUDICATION.md)
— 14 findings in, 14 rulings out.

## How it all works under the hood

[HOW-IT-WORKS.md](HOW-IT-WORKS.md) explains every rule: why it exists, which failure it was
written against, and which ones were only added after an external review caught them missing.

## Requirements

Claude Code, plus at least one other AI that can read files in your repo — Codex CLI, Gemini
CLI, Cursor, or a second Claude Code session that hasn't seen the work. A browser-only chat
works too, with a little more copying by hand; the skills spot that case and adjust.

## Credits

Four of the rules here came from reading
[code review cadre](https://github.com/VibeCodyH/code-review-cadre), which tackles a different
problem — picking which reviewers to use — but had already measured failures these skills
weren't guarding against. The calibration corpus follows
[cross-model-review](https://github.com/med95Albert/cross-model-review) and
[validity-audit](https://github.com/klmtseng/validity-audit), which frame it as *has the
checker demonstrated that it can fail when it should?* Ruling on the claim before reading the
argument comes from [refute](https://github.com/Jmosier69/refute). Details, and what was
deliberately not taken: [HOW-IT-WORKS.md](HOW-IT-WORKS.md#borrowed-from-code-review-cadre).

## License

[CC0 1.0](LICENSE) — public domain. Take them, change them, ship them, no attribution needed.
