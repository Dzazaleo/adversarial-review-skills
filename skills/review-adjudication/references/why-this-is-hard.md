# Why adjudication is hard — the four forces, and which rule resists each

Background for `SKILL.md`. Nothing here is an instruction; every obligation it motivates is
stated in the skill itself. Read it when a rule looks arbitrary and you are deciding whether to
follow it, and when you are about to dismiss a finding and want to know which reflex is talking.

The naive framing of this task — "decide what's worth implementing" — is the failure mode, not the
goal. Three forces push toward wrongly disposing of real findings, and every rule below exists to
resist one of them.

1. **You are usually mid-phase and want the phase closed.** Dismissal is the cheapest path to that,
   and it wears good clothes: "pre-existing", "out of scope", "scaffold only", "will handle later."
   A finding you just found and immediately deferred is the tell. Deferral is a legitimate outcome
   *only* when it costs something — a durable backlog artifact that exists on disk before the
   ledger is written.

2. **Rejection is held to a lower evidence standard than accusation.** The review brief made the
   reviewer produce Location · Mechanism · Trigger · Consequence · Status for every finding. A
   refutation typically arrives as a paragraph of reading. That asymmetry is where false REFUTEDs
   come from. **The refutation carries the same burden as the finding.** For any claim about
   runtime behaviour, a static read plus a reassuring code comment is not evidence — the comment is
   the party under review talking. Reconstruct and run the actual path.

3. **Self-review re-enters through the back door.** If you wrote the code, your refutation of a
   finding about that code is self-review again, and it carries the same blind spots that produced
   the defect. High-impact refutations of your own work need execution evidence or an independent
   check — never confident prose.

There is a fourth, quieter force running the other way: a reviewer with no access to your settled
decisions will reopen arguments you finished months ago, and implementing those is real damage —
churn, complexity, sometimes a reversal of a deliberate choice. Screening for that is legitimate and
is step 3. But it is a channel that dismissal will try to use, so it is gated: a "settled already"
ruling requires the citation, and a finding that brings **new evidence** the settled decision never
considered is not settled — it is reopened, and it goes to the owner.
