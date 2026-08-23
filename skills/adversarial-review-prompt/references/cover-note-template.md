# Cover-note skeleton

The cover note is what the user pastes into the reviewer's chat box. The audit brief stays on
disk; this is the short message that sends the reviewer to it and tells it how to deliver.

Keep it to roughly 20–30 lines of plain prose. No markdown headings, no tables, no nested code
fences — a chat box mangles them, and a reviewer that opens on a wall of structure treats the
brief as secondary reading. Numbered points are fine and are the only structure needed.

Text in `«guillemets»` is an instruction to you and must not survive into the output.

---

## Shape — four parts, nothing else

1. **Context and authorization** — one paragraph, first person, the user's own voice.
2. **The pointer** — the brief's path, on its own indented line.
3. **Delivery** — two numbered points: write the report to a file as you go; summarize in chat.
4. **Host gotchas** — only the ones that would otherwise read as defects.

What stays out: the adversarial framing (the brief carries it in full — restating a compressed
version here dilutes it and risks contradicting it), and anything about the author's own
suspicions (they anchor the reviewer, and this note is read *first*, so anchoring here is worse
than in the brief). The doubts themselves do not exist yet: the skill forms them in §9, after this
file is saved, and searches **this file as well as the brief** when bucketing them.

Part 1 is not politeness. An audit brief arriving cold — attack this, find what is wrong,
prove it — reads like a request to break into someone else's system, and a reviewer that is
unsure spends its first output on hedges and its effort on the safe parts. One paragraph of
true provenance removes that entirely. State only what is actually true.

---

## Template

```text
Context: this is a «pre-release reliability and correctness» review of my own code —
«one or two sentences: what the software is, who it runs for, and its exposure. e.g. a local,
single-user Windows desktop utility I'm building. No server, no network service, no accounts,
no remote input: it scans a folder of PNG texture files I point it at and reports which ones
can have their alpha channel dropped.» I own the repo, it's an «unreleased build on my own
machine», and I'm reviewing it before I ship it «to myself». The defects I care about are the
ones that «give an ordinary user a wrong answer or a frozen window».

Please read and execute the audit brief at:

  «path/to/NN-EXTERNAL-REVIEW-PROMPT.md — written as the reviewer will see it from the
  directory its session is rooted at»

Two things about how to deliver it, which the brief also states:

1. WRITE YOUR REPORT TO A FILE as you go:
   «path/to/NN-EXTERNAL-REVIEW.md»
   Create it early, append each finding as you confirm it, and finish with a pass that sets
   the final ranking and the coverage line. Do not hold the report only in memory. «One line
   of why, grounded in something that actually happened where it has: a chat reply that never
   arrived, a run that was cut short, a closed session.» Writing that one file is authorized.
   Everything under «src/, scripts/, tests/» and all config files stay read-only, and commit
   nothing. «Network, stated either way and never omitted: Web search is allowed — cite the
   URLs. / No network access; work only from what is in the repository.»

2. In your reply here, give me only a short summary: your coverage line, the ranked finding
   titles with impact levels, and the file path. Keep all detail in the file.

«Host gotchas — one short sentence each, only where a wrong guess would look like a finding.
The recurring one on Windows: If you're driving PowerShell, use npm.cmd rather than npm —
this host's execution policy blocks the npm.ps1 wrapper and it fails before npm starts, which
looks like a test failure but isn't.»
```

The capitalised `WRITE YOUR REPORT TO A FILE` is deliberate: it is the one instruction whose
loss costs the entire run, and it is competing with a long brief for the reviewer's attention.

**Every permission axis the brief states, this note states too — including the ones that grant
nothing.** Invariant 3 is `agree exactly`, and omission breaks it as surely as contradiction: a
reviewer reading only this note cannot tell an ungranted capability from an unmentioned one.

**Copy this checklist into the note's draft and tick every row before sending.** Round 6 shipped a
brief granting web search beside a cover note silent on network; round 7 then shipped *two* cover
notes silent on **its own tools** and **effort budget** — because the author cross-checked ten axes
of their own choosing instead of the six §7 enumerates. Prose telling you to "walk the table" is
what failed twice; the list is the fix.

| Axis | Brief says | This note says |
|---|---|---|
| Reading | | |
| Writing | | |
| Executing | | |
| Network | | |
| Its own tools (subagents, MCP) | | |
| Effort budget | | |

**Read-scope exclusions carry across.** Where the brief withholds a path — a residual-doubts
hand-off, a sibling reviewer's brief — this note names the same exclusion in the same words. Round 7
excluded `ROUND-6-HANDOFF.md` from one of two reviewers and left the other free to read it.

**Name the repository by absolute path, and give a one-command identity check.** A bare relative
path trip-wires on the wrong *model* and not on the wrong *tree*: round 7's Grok session started in
a stale clone four rounds behind, and only recovered because the file it needed was missing. Where
the target had existed at that older state, the audit would have run silently against superseded
work. Tell the reviewer to run `git -C «abs path» rev-parse --short HEAD` and stop if it does not
match the commit the brief pins.

---

## Variants

**Mutation testing authorized.** The write boundary in point 1 changes and must match the
brief exactly — name the report file, name the probe location, keep "commit nothing" and the
restore obligation. Do not describe the envelope as read-only.

**Reviewer has no filesystem access** — a plain web chat rather than an agentic session in the
repo. A path it cannot open is useless and the write instruction is impossible. Do not emit
this cover note at all. Tell the user instead: attach the brief as a file if the chat accepts
uploads — most do, and an attachment preserves the fences and tables a paste mangles — and
paste it whole only as a last resort; the report will come back in chat, and they should save
it to `NN-EXTERNAL-REVIEW.md` themselves. **And tell them to send a single "continue" if the
report stops at a section boundary** — the brief tells the reviewer to stop there and wait, and
it cannot resume itself, so a user who is not told files a truncated report as a complete one.
Say this here rather than relying on the skill's §10 checklist: §10 sits below the compaction cut
and this variant does not.

**Several reviewers, one brief — or one range split across briefs.** Give each reviewer its own
report path — `NN-EXTERNAL-REVIEW-<reviewer>.md` — so the second run cannot overwrite the first,
and say in each cover note that the file is that reviewer's alone. **This is not optional when the
runs may overlap in time**, and it applies to a split audit as much as to a shared brief: two
sessions writing one path is not a race the later one loses politely, it is the earlier report
destroyed. **Bind the cover note to its brief in the same breath** — each cover note names the
brief it belongs to and the reviewer it is for, so a note pasted into the wrong session is visible
in its first line rather than after the run. A reviewer given the wrong note follows it correctly
and audits the wrong half; that has happened here.

**A follow-up or delta review.** Point 1 must say whether to append to the existing report or
start a new file, and name it. A reviewer left to guess will overwrite.
