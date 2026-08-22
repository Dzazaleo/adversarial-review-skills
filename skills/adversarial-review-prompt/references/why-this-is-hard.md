# Why writing the brief is hard — the failure modes, and which rule resists each

Background for `SKILL.md`. Nothing here is an instruction; every obligation it motivates is in
the skill itself. Kept out of the main file so those obligations sit above the compaction cut.

## why this is hard

The failure mode is not a badly-formatted prompt. It is a prompt that produces confirmation.
A reviewer given "please review this code" will re-derive what the author already claimed,
agree, and return a polite summary of the author's own beliefs. That output is worthless and
worse than nothing, because it launders self-review as independent review.

Everything in this skill exists to defeat that. Three levers do most of the work:

1. **Name the *condition*, not the contents.** You cannot list the blind spots — if you could
   see them they would not be blind, and finding them is the reviewer's entire job. What you
   can state, because it is a fact about the process rather than about the work, is that one
   model wrote this, reviewed it, and verified it against tests it also wrote; that a reviewer
   with a different architecture notices different things; and that agreement is therefore a
   failed outcome. Never imply you know what was missed. Where you genuinely do suspect
   something, that is a *known* unknown — it is held out of the prompt entirely and handed
   to the user for post-review comparison (§10), never written into the prompt.
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
  `.adversarial-review/calibration/<reviewer-id>.md` under the project root — keyed on what the
  reviewer actually is (family, product and version, reasoning effort, and its own self-report
  where it gave one). The filename is always `<identity>-<effort>.md`, `<identity>` being the
  served model alias where the session gave one, else family plus product and version, else the
  family alone. **List the directory before concluding there is no record** — one product does not
  always describe itself the same way twice, and a record read as absent is the failure this
  scheme exists to avoid. Read its result, its expiry, **and its corpus digest**: recompute the
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


## leaked doubts — the case histories

This has now happened three times: 2026-08-10 (five doubts of five were in the brief), 2026-08-15
(four of four, reported as "deliberately excluded"), 2026-08-17 (two of three) — the last of these
*after* a search of the saved brief was made mandatory, and duly performed. It failed because the
author chose the queries: for a doubt whose own text quoted `unitScale && (rotation === 0 ||
isoBone)`, the recorded search was `packed`/`original`/`whitespace`/`strip`, none of which the
brief contained, while `isoBone` sat in claim 7. The one collision the search did surface was then
ruled "generic" by hand.

So take this literally: **you cannot certify absence in a document you wrote.** Over those three
runs, every wrong label was a claim of absence, and not one claim of presence — "prompted by claim
N" — was wrong. Presence is provable by pointing at a line. Absence is a claim about all six
hundred of them, made by the person who wrote them. Point, and let the adjudicator rule.

Run the search with no discretion in it. The queries come **from the doubt's own text** — every
`file:line` it cites, every backticked identifier, every SHOUTED term — never from your sense of
what the doubt is really about. One per line in a scratch file, then:

```bash
while IFS= read -r q; do printf '\n--- %s\n' "$q"
  grep -nF -- "$q" path/to/NN-EXTERNAL-REVIEW-PROMPT.md path/to/NN-EXTERNAL-REVIEW-COVER-NOTE.md \
    || echo '  no line'
done < queries.txt
```

A line citation often sits inside a range on the brief's side — the doubt says `:154`, the claim
cites `:129-155` — so when a citation query misses, run the bare path as well and read what cites
it. Then name, per doubt, the brief items the hits land in — "claim 7 at `:301`", "one-way door 1
at `:173`" — from anywhere in the brief, not only the claims list: on 2026-08-17 half the leak was
in the one-way doors, which the then-current rule did not cover. Where the queries turn up
nothing, the words are **"no line found — unverified"**. Never "held back", "withheld", or
"excluded from the brief": they assert what you are not in a position to know, they are the
signature of all three failures, and the adjudicator greps the hand-off for them.
