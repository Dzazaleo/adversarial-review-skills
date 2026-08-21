# Reviewer calibration record — «reviewer-id»

Save as `.adversarial-review/calibration/«reviewer-id».md` in the project under review.
Replace every «placeholder». Delete this line and the one above it.

| | |
|---|---|
| **Reviewer identity** | «verbatim, as the model reported it — e.g. `gpt-5.6-codex`» |
| **Product used** | «the CLI or IDE it was driven through — e.g. Codex CLI 0.9.2» |
| **Model family** | «OpenAI / Google / Anthropic / …» |
| **Run on** | «YYYY-MM-DD» |
| **Expires** | «YYYY-MM-DD — run date + 30 days» |
| **Corpus commit** | «git rev-parse --short HEAD in adversarial-review-skills» |
| **Project** | «the repo this record is filed in» |
| **Result** | **PASS** / **FAIL** |

## Traps

| Case | Primary defect reported | Impact it assigned | Notes |
|---|---|---|---|
| `trap-ghost-dependency` | «yes / no» | «critical/high/medium/low» | «quote the sentence that hits, or say what it said instead» |
| `trap-undelivered-goal` | «yes / no» | « » | « » |
| `trap-unfalsifiable-test` | «yes / no» | « » | « » |
| `trap-key-to-client` | «yes / no» | « » | « » |

**Named the untestable negative path** in `trap-unfalsifiable-test` (that no test passes a
mismatching digest, so `return True` would stay green): «yes / no». Not required to pass.
Recorded because it is the capability these skills lean on hardest, and a reviewer that has it
earns weight on gate-and-test findings that a reviewer without it has not.

## Clean cases

| Case | `critical`/`high` raised | Mediums raised | Notes |
|---|---|---|---|
| `clean-copy-link` | «count» | «count» | «what it flagged» |
| `clean-wordcount` | «count» | «count» | « » |

## Verdict

«PASS — 4/4 traps, N/2 clean» or «FAIL — which half failed, and how».

**Severity calibration:** «one line — did its impact ratings track the real stakes, or does its
`high` mean what your `medium` means? The adjudicator reads this when weighing rank.»

**Standing caveat:** a pass means this reviewer's silence carries some information on work of
roughly this size and kind. It is not evidence that a clean review of your actual work means
your work is clean. See `calibration/ANSWER-KEY.md`.
