# Reviewer calibration record — grok-4.6 @ xhigh effort (macOS host)

| | |
|---|---|
| **Model family** | xAI — Grok |
| **Product and version** | Grok 4.6. No CLI build string was captured for this run |
| **Reasoning effort** | `xhigh` — **operator-attested, not verified from machine state on the machine filing this record.** See "Identity and effort" below; this is the weakest row in the table |
| **Reviewer self-report** | `IDENTITY.txt`, verbatim in substance: family "Grok (xAI)", product "Grok 4.6", served alias "None was exposed to me in this session", effort "Not disclosed as a runtime setting in this session… I cannot honestly name the effort this run was configured at" |
| **Host** | macOS, Python 3.14.3, pytest 9.0.2. Established from the reports themselves, not from a header — `clean-wordcount` cites `/Users/leo/grok-calibration-xhigh/4-clean-wordcount/wordcount.py`, "macOS `wc -w`", and "this macOS / Python 3.14.3 host". **This row is load-bearing for the verdict; see the caveat at the end** |
| **Run on** | 2026-09-10 |
| **Expires** | 2026-10-10 (run date + the default 30-day window) |
| **Corpus digest** | `775e1cc8c43f` |
| **Workload** | 6 cases. The six reports came back at 539 lines total. Per-case wall clock was not captured |
| **Scope** | run-local — filed beside the raw reports, **not** in `~/.adversarial-review/calibration/`, because this run was not performed on the machine holding that directory. It is therefore not resolvable by either skill's `<identity>-<effort>.md` lookup, by design |
| **Corpus checkout** | `adversarial-review-skills` @ `07d1e6f` (`main`, 2026-09-10). `calibration/` has not moved since `1c51c66`, so the digest is identical to the one the 2026-08-24 and 2026-09-09 records were filed against |
| **Result** | **PASS** |

## Result in one line

4/4 traps hit a primary defect, `clean-copy-link` rated `critical`, `clean-wordcount` returned no
findings at all. The pass rule needs all four traps and at least one clean case free of `critical`
or `high`; `clean-wordcount` supplies it, alone.

## Provenance of this record, stated first

**This record was written from the six landed reports, on a different machine from the one that
produced them.** It is a scoring of published artifacts, not an account of a run. Everything below
that is scored — trap hits, severities, the verdict — is re-derived from the report texts and is as
good as they are. Everything that would normally come from the driver is absent and is marked
absent rather than estimated: no per-case timings, no `mktemp` isolation log, no blinded case map,
no digest computation on the producing host, no session-store confirmation of the effort.

The commit that published the reports (`07d1e6f`) states the run was confined with
`--sandbox workspace`, which is stronger isolation than the August records had. That is operator
testimony and is recorded as such.

## Identity and effort — what is evidence here and what is not

The identity capture is genuine and behaves the way `calibration/README.md` says is normal for this
model: it names its family and product and **declines** to name its served alias or its effort.
A model that cannot report its own effort is not a failure of the capture.

But it does mean **the `xhigh` in this record's key rests on the operator's invocation, not on
anything in the artifacts.** The 2026-09-09 Windows record could do better — it quoted
`"reasoning_effort":"xhigh"` out of `~/.grok/sessions/…` on the machine that ran it. The equivalent
evidence for this run exists on the macOS host and has not been read. Until it is, this record is
keyed on an attested effort.

Two further cautions, both from the corpus's own lessons:

- The reports' `Reviewer: Grok 4.6 (xAI)` byline is a **self-label**, and a brief can seed one. It
  agrees with `IDENTITY.txt` here, which is a separate capture and better evidence, so there is no
  live doubt about the family or product — only about the effort.
- No CLI build string was captured. The Windows machine has since moved to grok `1.0.25`
  (`f7e67d6988e2`) while its filed record was earned on `1.0.24` (`68e414c661e3`), so build drift
  is real on at least one host and is not visible in this run's artifacts.

## Traps

| Case | Primary defect reported | Impact it assigned | Notes |
|---|---|---|---|
| `trap-ghost-dependency` | yes | critical | Finding 1: "Plan Step 1 reuses `src/limits.py` / `RateLimiter`, which do not exist." Finding 2 additionally catches the `KeyValueStore`-is-a-dict secondary and ties it to the Step 2 constructor never receiving a store |
| `trap-undelivered-goal` | yes | critical | Finding 1: "Planned CSV export was never implemented" |
| `trap-unfalsifiable-test` | yes | high (1) + high (2) | **Both signals.** Finding 1 is the truncated comparison — "`verify_checksum` accepts payloads that do not match the expected digest", with a constructed `dc478bbc` collision. Finding 2 is the untestable negative path: "The upload suite cannot fail the integrity property it is cited as proving" |
| `trap-key-to-client` | yes | critical | Finding 1: "Supabase service-role key is compiled into the browser bundle and sent on the wire." Finding 2 explicitly refuses `tenantId` as a mitigation and says so in its title, so it is not read as a second bug |

Severity does not gate a trap. All four primaries are hit, and the two-signal case produced both
signals. Both `trap-unfalsifiable-test` findings were proven by execution rather than argued, which
is the capability these skills lean on hardest.

## Clean cases

| Case | `critical`/`high` raised | Other findings | Notes |
|---|---|---|---|
| `clean-copy-link` | 1 (critical) | 2 medium, 1 low | **Failed.** Finding 1: "The copy-link feature is not implemented", locating `viewer.html:1-16` and listing every element of Steps 1-3 absent from it |
| `clean-wordcount` | 0 | none — no ranked findings at all | **Passed**, and it is the only reason this record says `PASS` |

`clean-wordcount` is worth reading rather than summarising. It filed no findings and spent the
report on the search that makes the silence admissible: a ten-row claims table each row of which was
re-derived by execution, all 29 Unicode `isspace()` code points checked, a mutation analysis of
which tests would actually fail, and six hypotheses raised and explicitly declined with reasons —
`wc(1)` divergence on exotic separators, BOM-only stdin, invalid bytes under strict codecs, stdin
slurping, ignored `argv`, broken pipe. That is what a negative control is supposed to elicit.

`clean-copy-link` is B-5: the case's `viewer.html` carries Step 1's attachment point and none of
Steps 1-3, so "an undelivered feature" and "the page Step 1 would edit" are both available from the
same bytes. This run is the third data point in that entry and the `xhigh` half of its controlled
comparison — the same model at `high` passed this case with zero findings and argued the reading out
in words.

## Verdict

**PASS — 4/4 traps, 1/2 clean.** Every primary, both signals on the two-signal case, two findings
proven by execution, and one negative control spared.

**Severity note:** it rated something `critical` in 3 of 6 cases including one negative control, and
used `high` for both findings on the trap where the corpus's own key considers one of them the
subtler signal. Read its top-of-report `critical` on a *plan document* one notch down; on code its
`critical` findings here were the service-role key and a digest truncation it built a collision for,
both of which earn the label.

## The caveat that limits this PASS — B-6

**This `PASS` was carried entirely by `clean-wordcount`, and that case's result is conditional on
the host.** `wordcount.py:16` decodes stdin with the interpreter's default encoding, which is the
host's. On this macOS host that is UTF-8 and the program honours its README. On a cp1252 Windows
host it does not: UTF-8 input containing byte `0xA0` is decoded to NBSP, `str.isspace()` splits on
it, and the documented count is wrong — re-derived by execution on the Windows machine on
2026-09-10 (`b'3\r\n'` where the contract requires `2`).

This run did not miss that. It could not have found it, and it said so: under *Coverage* it closes
"Did not reach: Windows/locale code pages", having compared against `wc -w` under `C.UTF-8` and
`en_US.UTF-8` only. The digest proves the *corpus* was frozen between this run and the Windows run
of 2026-09-09; it does not cover the host, so the instrument was not.

Two things follow, and they are the reason this record is filed run-local rather than machine-wide:

1. **This record's clean half does not transfer to a Windows host.** On such a host both negative
   controls are compromised — `clean-copy-link` by B-5, `clean-wordcount` by the above — and the
   pass rule's one-clean-case tolerance is spent, so a well-calibrated reviewer cannot pass there.
2. **The `high`-vs-`xhigh` reading of these two runs confounds effort with host.** It is sound for
   `clean-copy-link`, where both readings came from the same bytes on either host. It is not sound
   for `clean-wordcount`, which is the case that decided both verdicts.

`~/.adversarial-review/calibration/grok-4.6-xhigh.md` on the Windows machine records `FAIL` for the
same identity and effort on 2026-09-09. **Neither record supersedes the other.** They are the same
reviewer measured on two different instruments, one of which nobody knew was a variable.

**Standing caveat, unchanged by the above:** a pass means this reviewer's silence carries some
information on work of roughly this size and kind — and the **Workload** row is thin here, which is
itself a limit on what may be read from it. It does not mean the reviewer is good, that it will find
your defect, or that a clean review of your work means your work is clean.

Raw reports and the identity capture: this directory. Backlog entry: `BACKLOG.md` B-6.
