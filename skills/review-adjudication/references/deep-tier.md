# The deep tier — what `--deep` adds

**Loaded only on a deep run.** `SKILL.md` carries the light protocol whole and stubs each of these
in place, so a light adjudication never pays for this file. The `D` numbers are the stub labels;
the `§` in each heading is the `SKILL.md` section the piece belongs to.

Nothing here is optional once the tier is deep, and nothing here is owed on a light run. The tier
itself is decided in `SKILL.md` §1: a one-way door, a disputed high-severity finding, or a
reviewer/author disagreement worth arbitrating.

---

## D1 · §1 — calibration: digest, precedence, workload

Recompute the corpus digest with the command the record names, arbitrate a project-local record
against a home one, and state the workload gap in numbers — each has a trap that has already cost a
session, all of them in [inputs-and-calibration.md](inputs-and-calibration.md).

## D2 · §2 — auxiliary blocks and ID namespaces

Give each auxiliary class its own ledger block and its own ID namespace (`P-`, `CNV-`, `D-`, `U-`
for a re-opened upheld claim, `A-` for your own findings, `C-` for corrections to an earlier
round), count them separately in the header, and sample the upheld list rather than scanning it.

That per-namespace breakout is also what §7's header counts expand to on a deep run: process, CNV,
prior-review disagreements, re-opened upheld claims, your own `A-N` findings, `C-N` corrections to
earlier rounds — each stated even when it is zero. A process or prompt defect gets its own block
here rather than a class-tagged row.

## D3 · §2 — extract a claim card with each row

Alongside the skeleton, write each finding's *claim* on its own, into the session scratchpad —
never beside the ledger, where a later reviewer would read it. A claim card is exactly five fields,
copied verbatim and nothing else:

> Location · Mechanism · Trigger · Consequence · the impact the reviewer assigned

What stays out of the card is the point of it: the reviewer's **reasoning**, its evidence, the
argument for its severity, its suggested fix, and every phrase carrying confidence ("clearly",
"this will certainly", "I verified"). Those are how it persuaded itself, and step 5 verifies the
claim rather than grading the argument. Where a field is genuinely absent from the report, the card
says `not stated` — a finding with no stated trigger is one nobody can reproduce yet. Where the
reviewer put its evidence or its severity case *inside* the Mechanism, copy the claim clause
verbatim and replace the argument with a pointer to the report line (`— argument at :131`); never
paraphrase, which silently edits what you are about to verify. Cut the cards while you are still
transcribing, before any ruling exists: a card cut later is a card cut by someone who has already
decided. It does not make you blind — you read the report in step 1 and cannot unread it — it gives
step 5 a target containing only the claim.
[verification-standard.md](verification-standard.md).

**What the card buys, exactly.** You read the report in step 1 and cannot unread it; the card does
not make you blind. It gives step 5 a target containing only the claim, so the check aims at the
mechanism rather than the case for it. Genuine blindness exists only in step 5's subagent, and even
there, not being *handed* the report is not being unable to read it.
[verification-standard.md](verification-standard.md).

**They are the one exception to §7's write boundary**, and they live in the session scratchpad,
never beside the ledger: a card sitting in the review directory is the next reviewer's reading
material, and it is the finding stripped of its evidence.

## D4 · §5 — verify against the claim card, and pre-register the expectation

Open the card, write down what you expect the check to show *before* you run it, run it, then
re-read the reviewer's argument for that finding and record on its own line whether it changes the
ruling and which way. Pre-registration works on you, in the moment, and only if you actually write
the expectation first — it is no proof to a later reader, since the ledger records an expectation
and an output but nothing establishing their order. It guards both directions: a well-argued false
finding earns a `CONFIRMED` it did not deserve, and one stated flatly or in poor English earns a
`REFUTED` on the same non-evidence. Both are rulings on the reviewer's prose — a fact about the
reviewer, not about the code. Re-read the argument afterwards either way: it is often where the
reproduction steps are, and a card whose `Trigger` says `not stated` may only be reproducible from
the prose around it.

## D5 · §5 — run the echo probe and tally it

For every finding, query the brief and the cover note with that finding's own identifiers, record
whether the brief had already said it, and put the tally in the ledger — how many findings were
echoes, how many partial, how many were free to surprise. That last number is what the report's
evidentiary weight actually rests on. Measured twice here: 10 of 15 findings were echoes of the
brief's own sub-questions, then 6 of 9.
[verification-standard.md](verification-standard.md).

## D6 · §5 — sample the upheld list

A claim the reviewer upheld is a ruling you inherit, not a line you copy. Sample rather than
transcribe, re-open what was cleared on the work's own say-so, and rank a reviewer that reached the
defect and argued it intentional **below** a plain miss — that leaves you the bug plus a written
case for keeping it. (Light tier does the cheap half of this in §2 and no more.)

## D7 · §5 — a second opinion that was not handed the report

Spawn a subagent, give it the claim card and the code the claim concerns, and ask it to establish
whether the mechanism holds — never to check your work, which only hands it your conclusion to
agree with. Spawn it with a tool allowlist excluding `Write`, `Edit` and `NotebookEdit`; a subagent
does not inherit this skill, and `Bash` is itself a write capability. Record two facts beside the
verdict: whether its tools were restricted, and whether it could have read the report — not being
*handed* it is not blindness, since the subagent is spawned into the directory it sits in, and
**never write "blind" for a check that was merely uninformed.** If you disagree with it, the
verdict is `COULD NOT DETERMINE`. [second-opinion.md](second-opinion.md).

## D8 · §7 — the per-write append proof

Take a pre-session copy before your first write and prove the completed prefix untouched after
every write, not once at the end: `head -n <the prior round's last line> <ledger> | diff - <the
pre-session copy>` must be silent.
