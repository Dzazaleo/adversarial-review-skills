# Reviewer calibration record — «reviewer-id»

Save as `.adversarial-review/calibration/«reviewer-id».md` in the project under review.
Replace every «placeholder». Delete this line and the one above it.

| | |
|---|---|
| **Model family** | «OpenAI / Google / Anthropic / …» |
| **Product and version** | «the CLI or IDE it was driven through, with its version — e.g. Codex CLI 0.9.2» |
| **Reasoning effort** | «the setting this calibration ran at — e.g. high / medium / default / not exposed» |
| **Reviewer self-report** | «verbatim, what the model said when asked what it is — e.g. `gpt-5.6-codex`, or `OpenAI Codex, GPT-5-based; exact served version not exposed to it`» |
| **Run on** | «YYYY-MM-DD» |
| **Expires** | «YYYY-MM-DD — run date + the window you chose. 30 days is the default, not a requirement; say which you used and why if it was not 30» |
| **Corpus digest** | «in adversarial-review-skills, run: `git ls-files -z calibration/cases calibration/CALIBRATION-PROMPT.md calibration/ANSWER-KEY.md \| sort -z \| xargs -0 shasum \| shasum \| cut -c1-12`» |
| **Workload** | «what the six cases actually were, in numbers — e.g. `6 cases, 14 files, ~400 lines total`. This is the size the pass was earned on, and the consumer states it beside the size of the work it is adjudicating» |
| **Project** | «the repo this record is filed in» |
| **Result** | **PASS** / **FAIL** |

The first four lines are the identity, and they are all four of it. A model that cannot name its own
served version is common and is not a failure — record what it did say, and the family, product
version and effort carry the key. **Effort is not decoration:** the same model at high and at low
reasoning effort is not the same reviewer, and a pass earned at one is not evidence about the other.

The digest covers **the instrument only**: the cases, the fixed brief, and the answer key. Not
`calibration/README.md` or this template, which are operator documentation the reviewer never sees
— a typo fix in either would otherwise expire every record on file for nothing.

**It enumerates tracked files, and that is the point of the command.** An earlier version walked
the directory with `find`, which hashed whatever happened to be sitting there — and every artefact
anyone's tooling dropped became part of the instrument. `.DS_Store` was pruned by name, then
pytest's `__pycache__/*.pyc` arrived through the same door, written by *following the calibration
procedure itself*. Worse, timestamp-mode `.pyc` embeds the source file's mtime, so the post-test
digest differed on every machine: one corpus, one commit, three different digests across three
checkouts. Every record silently expired the first time anyone ran the fixtures, and a valid
`PASS` read as stale. Enumerating tracked files ends the whole class — there is no artefact list
to maintain and no next artefact to be surprised by.

**What it costs, stated rather than discovered later:** a case edited but not committed does not
change the digest, and an entirely uncommitted private replacement corpus produces the digest of
whatever *is* tracked. Commit corpus edits before filing or trusting a record. Where a private
corpus is genuinely untracked, this command is the wrong instrument for it and the record should
say so on its face rather than carry a digest that describes something else.

## Traps

| Case | Primary defect reported | Impact it assigned | Notes |
|---|---|---|---|
| `trap-ghost-dependency` | «yes / no» | «critical/high/medium/low» | «quote the sentence that hits, or say what it said instead» |
| `trap-undelivered-goal` | «yes / no» | « » | « » |
| `trap-unfalsifiable-test` | «yes / no» | « » | « » |
| `trap-key-to-client` | «yes / no» | « » | « » |

**Which signal hit in `trap-unfalsifiable-test`** — the case has two primary defects and either one
scores it: «the truncated comparison / the untestable negative path / both / neither». Record which,
because they are not worth the same downstream. A reviewer that named the untestable negative path
(that no test ever passes a mismatching digest, so `return True` would stay green) has demonstrated
the capability these skills lean on hardest, and earns weight on gate-and-test findings that a
reviewer which only spotted the truncated comparison has not.

## Clean cases

| Case | `critical`/`high` raised | Mediums raised | Notes |
|---|---|---|---|
| `clean-copy-link` | «count» | «count» | «what it flagged» |
| `clean-wordcount` | «count» | «count» | « » |

## Verdict

«PASS — 4/4 traps, N/2 clean» or «FAIL — which half failed, and how».

**Severity calibration:** «one line — did its impact ratings track the real stakes, or does its
`high` mean what your `medium` means?» This is a note for whoever reads the record, and nothing
more. It never adjusts a finding's verdict or its rank: calibration governs the reviewer's silence,
never its speech, and a real defect is not worth less because the reviewer that found it rates
things a notch high.

**Standing caveat:** a pass means this reviewer's silence carries some information on work of
roughly this size and kind — the **Workload** row above says what that size actually was, in
numbers, so a later reader can compare it with the work being adjudicated rather than guess at
"roughly". It is not evidence that a clean review of your actual work means your work is clean.
See `calibration/ANSWER-KEY.md`.
