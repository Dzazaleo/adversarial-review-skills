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

## the doubts have no durable channel, and that is the ruling

The list is chat-only by design: a file is one `ls` away from a reviewer session rooted more broadly
than expected, and the entire value of an `UNSEEDED` doubt is that the reviewer could not have been
pointed at it. `review-adjudication` §1 then says the list "lives in a chat message you cannot read"
and asks the user for the hand-off.

That assumes the authoring and adjudicating sessions are close enough together that the window is
still open. Here they routinely are not — days apart is the normal case rather than the exception —
and until **2026-08-24** both skills acknowledged the fragility and offered no ruling, so each
session improvised one.

**The ruling is that there is no durable channel, and inventing one is not the session's to do.**
The window *is* the artifact. Say so at hand-off in plain words, and stop there: do not resolve the
fragility by writing the list to disk under a name you judge safe, by folding it into the brief, or
by arranging any other route the adjudicator could read without the user handing it over. The two
costs are not symmetric. Losing the window costs one round's corroboration scoring — already a
bounded loss, since a doubt becomes corroboration only once an adjudicator runs its *own* search and
rules it absent. Leaking it costs the corroboration itself, silently, and in the direction that looks
like success.

The adjudication half of the same ruling: **take the list from the original hand-off message or from
nowhere.** A doubts file found on disk and a copy folded into the brief were both reachable by the
reviewer; a list the authoring session reconstructs now is written after the report it is supposed to
be independent of. Any of those is recorded as **unavailable**, exactly as if it had been lost.
