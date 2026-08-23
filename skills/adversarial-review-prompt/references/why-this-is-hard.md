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
   do suspect something, that is a *known* unknown — it is held out of the prompt entirely and
   handed to the user for post-review comparison (§10), never written into the prompt.
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

## calibration lookup

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
  treating the record as current. Missing, expired,
  or `FAIL` is a normal state and never a reason to refuse: run the review anyway. It changes one
  thing, and you say it at hand-off (§10) — **an untested reviewer's findings still count, and
  its silence does not.** A clean report from it is inconclusive rather than an all-clear, its
  claims-examined-and-upheld list is not coverage, and nothing it "cleared" may be written into
  the next brief's §7. That asymmetry is not caution, it is the same rule as everywhere else
  here: a finding arrives with evidence attached and can be checked, whereas silence arrives with
  nothing and can only be trusted. The corpus and the 20-minute procedure live in the source
  repository, not in the installed skill, so point at the URL:
  https://github.com/Dzazaleo/adversarial-review-skills/tree/main/calibration
  Mention it once, do not campaign for it.


## leaked doubts — the case histories, and why the fix is the order

Four rounds, four leaks: 2026-08-10 (five doubts of five were in the brief), 2026-08-15 (four of
four, reported as "deliberately excluded"), 2026-08-17 (two of three), 2026-08-23 (five of five).

The third failed because the author chose the queries. A search of the saved brief had just been
made mandatory and was duly performed: for a doubt whose own text quoted `unitScale && (rotation
=== 0 || isoBone)`, the recorded search was `packed`/`original`/`whitespace`/`strip`, none of which
the brief contained, while `isoBone` sat in claim 7. The one collision it did surface was then
ruled "generic" by hand. The rule that followed — **queries come from the doubt's own text, never
from your sense of what it is about** — closed that hole, and the hole stayed closed.

**The fourth round is the one that changed the design.** On 2026-08-23 the search was run
correctly, with the doubt's own strings, over the brief *and* the cover note, and it reported the
leak accurately: all five. The adjudicator's tally on the same report read *1 free / 3 partial /
4 echo*, and the review's single genuinely independent discovery was also its best finding. Nothing
had gone wrong with the check. **What was wrong was upstream of it.** Doubts were being mined in
the same pass as the load-bearing claims, out of one reading of one body of work, so a doubt was
structurally almost certain to be a claim already in the brief. No search, however honest, can
subtract a leak that the collection order guarantees.

So the order changed: **the brief is saved first, and only then are the doubts formed — by
re-reading the saved file and asking what it turned out not to ask.** Overlap is now measured
against a fixed document rather than produced alongside it, and the two buckets carry different
weight rather than the whole list collapsing to "echo":

- `SEEDED` doubts are not corroboration and never can be. Their use is the reverse: the brief
  pointed at the seam, so a **calibrated** reviewer that stayed silent on it has told you
  something — about the doubt, or about that reviewer's reach.
- `UNSEEDED` doubts are the only corroboration-eligible ones, and even they are only a report
  until an adjudicator has run its own search.

And the older rule still holds, because it is what makes the buckets readable: **you cannot certify
absence in a document you wrote.** Across all four runs every wrong label was a claim of absence,
and not one claim of presence — "prompted by claim N" — was wrong. Presence is provable by pointing
at a line. Absence is a claim about all six hundred of them, made by the person who wrote them.
Point, and let the adjudicator rule.

## the search loop

Run it with no discretion in it. The queries come **from the doubt's own text** — every `file:line`
it cites, every backticked identifier, every SHOUTED term — never from your sense of what the doubt
is really about. One per line in a scratch file, then:

```bash
BRIEF=path/to/NN-EXTERNAL-REVIEW-PROMPT.md
NOTE=path/to/NN-EXTERNAL-REVIEW-COVER-NOTE.md
# Second pass on a whitespace-flattened copy: the brief's prose wraps, and a line-oriented
# grep has reported "no line found" for a phrase that was present, split across two lines.
cat "$BRIEF" "$NOTE" | tr '\n' ' ' | tr -s ' ' > "$TMPDIR/flat.txt"

while IFS= read -r q; do
  printf '\n--- %s\n' "$q"
  grep -nF -- "$q" "$BRIEF" "$NOTE" \
    || { grep -qF -- "$q" "$TMPDIR/flat.txt" \
         && echo '  WRAPPED HIT - present; the line grep missed it, locate it by hand' \
         || echo '  no line found - unverified'; }
done < queries.txt
```

A line citation often sits inside a range on the brief's side — the doubt says `:154`, the claim
cites `:129-155` — so when a citation query misses, run the bare path as well and read what cites
it. **Any hit at all makes the doubt `SEEDED`**, and you name where it landed: "claim 7 at `:301`",
"one-way door 1 at `:173`" — from anywhere in the brief, not only the claims list, because on
2026-08-17 half the leak sat in the one-way doors, which the then-current rule did not cover.

**Only a doubt with no hit in either pass is `UNSEEDED`, and the words for it are "no line found —
unverified".** Never "held back", "withheld", or "excluded from the brief": they assert what you
are not in a position to know, they are the signature of all four failures, and the adjudicator
greps the hand-off for them.
