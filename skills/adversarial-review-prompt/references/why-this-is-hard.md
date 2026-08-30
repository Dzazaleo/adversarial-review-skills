# Why writing the brief is hard — the failure modes, and which rule resists each

Background for `SKILL.md`, and **subordinate to it and to `prompt-template.md` — where they
differ, this file is the stale one.** It carries the reasoning and the case histories; the
obligations are in the skill, and the emitted wording is the template's.

## why this is hard

The failure mode is not a badly-formatted prompt. It is a prompt that produces confirmation.
A reviewer given "please review this code" will re-derive what the author already claimed,
agree, and return a polite summary of the author's own beliefs. That output is worthless and
worse than nothing, because it launders self-review as independent review.

Everything in this skill exists to defeat that. Three levers do most of the work:

1. **Name the *condition*, not the contents.** You cannot list the blind spots — if you could
   see them they would not be blind, and finding them is the reviewer's entire job. What you
   can state, because it is a fact about the process rather than about the work, is how the work
   was authored and reviewed — and then **only what that particular pairing actually buys.**
   Whether a difference in architecture is among the things it buys depends on both identities,
   which is why the emitted wording is not written here: take it from `prompt-template.md`'s four
   branches, which are the authority. Never imply you know what was missed. Where you genuinely
   do suspect something, that is a *known* unknown — it is held out of the prompt entirely, and
   out of the cover note and the hand-off too. It is not routed anywhere: the residual-doubts
   protocol that used to carry it is retired, below.
2. **Demote the author's assertions to claims.** Every confident comment, test name, and
   "verified/measured/guaranteed" note is a testable assertion by the party under review,
   never evidence. This single reframing produces more findings than any checklist.
3. **Hand over a target list, not a codebase.** You cannot point at the blind spot, but you
   can point at what is carrying weight. An enumerated list of load-bearing claims — each of
   which must come back CONFIRMED / REFUTED / COULD NOT DETERMINE — puts the reviewer's
   different eyes where an unseen defect would be expensive, instead of scattered thin across
   the whole tree by a generic "audit this."

## identity guessing

**A habit is not an answer.** What this project used last time, what its history suggests,
  what is installed on the machine, what the surrounding documentation was written around, and
  what most users of this skill run are all inference. Each produces a confident wrong answer
  exactly as readily as a right one, and none of them is evidence about the session the user is
  actually about to open.

  **What a wrong guess costs, precisely.** The calibration lookup below is keyed on the
  reviewer's identity. Name the wrong model and the lookup returns a different model's record —
  very possibly a `PASS` — and the hand-off then reports *this* reviewer as calibrated when it
  has never been tested on anything. That is a false all-clear at the one point this whole
  scheme exists to protect, and nothing downstream catches it: the ledger faithfully records
  what the lookup returned, and a record that was read for the wrong reviewer looks identical to
  one read for the right one. Note the asymmetry and let it decide you. A **missing** record is
  a normal state that costs one honest sentence at hand-off. A **wrong** record is an error no
  later step can see. One question removes the second risk entirely.

## calibration lookup — light reads two fields, `[deep]` does the rest

**Light tier reads the result and the expiry and reports one line.** Everything below — digest
recomputation, the closed list of mismatch traps, arbitrating a project-local record against a
home one — is the `[deep]` tier. It is here because when it is run it must be run exactly this
way, not because it is owed on every brief.

- **Calibration** — whether this reviewer has ever been shown to find anything. Look for
  `.adversarial-review/calibration/<reviewer-id>.md` in **two locations, the project root first
  and `~/` second** — keyed on what the reviewer actually is (family, product and version,
  reasoning effort, and its own self-report where it gave one). The filename is always
  `<identity>-<effort>.md`, `<identity>` being the served model alias where the session gave one,
  else family plus product and version, else the family alone. **List both directories before
  concluding there is no record** — one product does not always describe itself the same way
  twice, and a record read as absent is the failure this scheme exists to avoid.

  **The home copy is the normal one, and the reason is that the measurement is not project-shaped.**
  The corpus is fixed, the six cases run in a scratch directory, and nothing the project under
  review supplied enters the result — so a pass earned while reviewing project A is evidence about
  the same reviewer in project B. What does not travel is reach: the corpus is six small Python,
  HTML and plan-document cases, and that bound is already stated in numbers by the workload gap
  rather than by hiding the record. A project-local record still wins where one exists, because
  pinning one is deliberate — a team-shared record, or a private replacement corpus. On
  **2026-08-23** a reviewer holding a filed `PASS` was reported to a second project as "none on
  file" purely because the lookup looked only where it stood. **Name at hand-off which of the two
  you read it from.** Read its result, its expiry, **and its corpus digest**: recompute the
  digest from the corpus and compare, because that is the only check that notices the instrument
  changing, and where you do not have the corpus, say staleness was unknowable rather than
  treating the record as current.

  **Precedence is by location, not by freshness.** A project-pinned record wins while it is older,
  thinner, or filed against a corpus that has since moved, and nothing in either consumer compares
  the two — so a stale pin shadows a better home copy silently. Open both where both exist, and say
  at hand-off if they disagree on anything but the result. On **2026-08-24** this repository was
  found carrying two pinned duplicates that had missed the round adding the `Scope` and `Corpus
  checkout` rows. They were deleted rather than refreshed: a pin is a standing commitment to
  maintain a second copy, and nothing here needed one.

  **A digest mismatch is not by itself evidence that the corpus moved.** The digest hashes
  working-tree bytes through a `shasum` whose own output format varies by platform, so three
  properties of the *machine* each produce a different answer from an unmoved tree:

  - **Collation.** The ordering step is the shell's, and `LC_ALL=C` pins it. Round 7 `A7-1`.
  - **Output mode.** `shasum`'s output *is* the inner stream, so the separator between digest and
    path is hashed along with it. It defaults to text (two spaces) on macOS and Linux and to binary
    (` *`) on Windows — `775e1cc8c43f` against `676b43331561` for one identical corpus. `-t` pins
    it, and is a no-op wherever text was already the default.
  - **Line endings.** A `core.autocrlf=true` clone — what the Git-for-Windows installer offers by
    default — checks out CRLF and hashes it: `b6dad9bf7e9c`. The corpus's root `.gitattributes`
    marks every path `-text`, pinning the checkout whatever the cloner's config says; a clone
    predating that file still needs `core.autocrlf=false`.

  **That list is closed, and having been written down in advance is the whole difference between
  checking it and adjusting a command until it matches** — the second is not a check, whatever it
  returns. Rule out those three, change nothing else, then record stale. On **2026-08-24** a Windows
  session read two valid, in-date records as stale on the output-mode trap alone and came one
  keystroke from re-running the corpus: forty minutes, and both records would have been replaced by
  ones carrying the same platform-dependent digest, which fixes nothing and expires on the next
  machine. Missing, expired,
  or `FAIL` is a normal state and never a reason to refuse: run the review anyway. It changes one
  thing, and you say it at hand-off (§9) — **an untested reviewer's findings still count, and
  its silence does not.** A clean report from it is inconclusive rather than an all-clear, its
  claims-examined-and-upheld list is not coverage, and nothing it "cleared" may be written into
  the next brief's §7. That asymmetry is not caution, it is the same rule as everywhere else
  here: a finding arrives with evidence attached and can be checked, whereas silence arrives with
  nothing and can only be trusted. The corpus and the 20-minute procedure live in the source
  repository, not in the installed skill, so point at the URL:
  https://github.com/Dzazaleo/adversarial-review-skills/tree/main/calibration
  Mention it once, do not campaign for it.


## residual doubts — retired, and the history that retired it

The skill used to close by forming the author's own residual doubts against the saved brief,
bucketing each `SEEDED` (the brief already asks it) or `UNSEEDED` (it does not), and handing the
user both lists in chat for the adjudicator to re-rule. That is gone. One sentence replaces it, in
SKILL.md §9: **author doubts are never corroboration, and the adjudicator treats reviewer
agreement with the brief as non-independent by default.**

The warrant is the protocol's own measured record. Four rounds, four leaks: 2026-08-10 (five
doubts of five were already in the brief), 2026-08-15 (four of four, reported as "deliberately
excluded"), 2026-08-17 (two of three — the author chose the queries, and for a doubt whose own
text quoted `unitScale && (rotation === 0 || isoBone)` the recorded search was
`packed`/`original`/`whitespace`/`strip`, while `isoBone` sat in claim 7), and 2026-08-23 (five of
five, **with the search run correctly** — the doubt's own strings, over the brief and the cover
note, whitespace flattened, and the leak reported accurately).

The fourth round is the one that settles it, because nothing was wrong with the check. Doubts
mined from one reading of one body of work are structurally almost certain to be claims already in
the brief, and no search subtracts a leak the collection order guarantees. Forming them *after* the
brief was saved was the fix that round produced; the next round measured 5 of 5 anyway.

Against that, the credit at stake was small and could not be banked cheaply. An `UNSEEDED` doubt
became corroboration only once an adjudicator ran its *own* search and ruled it absent. The list
had no durable channel and could not be given one — a file is one `ls` away from a reviewer session
rooted more broadly than expected — so it lived in a chat window, and authoring and adjudicating
sessions here are routinely days apart, which made "unavailable" the ordinary outcome. Roughly
eighty lines of protocol across the two skills, for that.

**What survives does the same work and costs nothing extra.** The adjudicator probes every finding
against the brief and the cover note using the finding's own identifiers and rules the echoes from
primary sources. That was always the large channel: a pointed sub-question states the suspected
defect outright, so a reviewer agreeing with it has answered a question rather than found
anything. The doubts were the small one.

**Two rules keep their force, and neither is doubts-specific.** You cannot certify absence in a
document you wrote — across all four runs every wrong label was a claim of absence, and not one
claim of presence ("prompted by claim N") was ever wrong. And your suspicions still go nowhere near
the brief, the cover note, or the hand-off: they belong in §3's claims list, sharp, where the
reviewer is pointed at them openly instead of being credited with reaching them alone.

## several reviewers — what their agreement is worth

`review-adjudication` §5 rules that **two reviewers handed the same brief are not independent**.
That rule has lived only in the skill that measures the damage, never in the one that could prevent
it, and the asymmetry is itself the defect: by adjudication time the briefs are written and the runs
are spent, and all that is left to do is discount what came back.

The cost is not marginal. Asked for three reviewers, this skill did the natural thing and produced
three byte-identical briefs — the same 20 directed claims, the same four measured cases. In round 1,
**3 of 27 findings across those three reviewers were free of the brief's direction**; the other 24
were three models answering the same twenty questions, which is one piece of evidence wearing three
coats. §3 already measures the same effect on a single reviewer — 10 of 15, then 6 of 9 findings
were echoes of its own sub-questions — and handing that identical list to three reviewers multiplies
the cost without touching the cause.

So where more than one reviewer is commissioned, vary something real between them:

- **Split the scope.** Each gets a disjoint file set and the union is the audit. Cheapest to
  arrange, and it bounds each reviewer's silence to its own half instead of leaving it illusory
  across the whole.
- **Split the directed set.** One receives §3's claims list; another receives the same ground with
  the list withheld and only the template's §6b unseeded pass. Agreement between those two means
  something the first arrangement cannot buy.

**Varying nothing is a legitimate choice, and has to be a stated one.** Three answers to one set of
questions is a real consistency check: it catches a reviewer that misread the brief, and a claim
that is wrong in a way only some models see. What it is not is corroboration, on any finding. So say
which arrangement you used, and name in the hand-off **which reviewer received which** — the
adjudicator rules independence off that line and has no way to reconstruct it from two reports
sitting in one directory.

The file mechanics — one report path per reviewer, each cover note naming its own brief — are in
`cover-note-template.md`. They stop the second run destroying the first one's report. They do
nothing whatever for independence, and should not be mistaken for having handled it.

## reasoning effort — the field nothing ever captured

Effort is half the calibration key. The record filename is `<identity>-<effort>.md`, and both
`calibration/record-template.md` and `calibration/README.md` are emphatic about why: the same model
at high and at low reasoning effort is not the same reviewer, and a pass earned by the strong
configuration is not evidence about the weak one running under the same name.

Nothing captured it. Effort is a setting inside the reviewer's session, it appears in no report the
reviewer writes, and until **2026-08-24** no brief this skill produced carried the field either.
`review-adjudication` §1 names three sources for it — `$ARGUMENTS`, the brief the report answers, or
a prior round's ledger header — and **the second had never once existed**. The consequence was
silent and cumulative: two rounds were adjudicated as matching the record on family and product but
*unverified on the key's own effort field*, which weakens every lookup made against those ledgers
afterwards.

The fix is one question in §1 and one line in the brief's identity block. Where the reviewer does
not expose the setting — some do not — the answer is `not exposed`, recorded in those words. That
is a different and more useful claim than an empty field, which reads as nobody having asked.
