# The second opinion — when it is required, how to spawn it, and what it is worth

Background for `SKILL.md` §5's escalation rules. The obligations are in the skill; this is the
full procedure and the reasoning, kept out of the main file so the obligations sit above the
compaction cut.

- **That same verdict also requires a second opinion that was not handed the report.** Spawn a
  subagent, hand it the claim card and the code the claim concerns, and ask it to establish
  whether the mechanism holds — not to check your work, which would only give it your conclusion
  to agree with. It must not receive the reviewer's reasoning, your reasoning, or your verdict.
  Where the two of you disagree, the verdict is `COULD NOT DETERMINE` and the disagreement goes in
  the ledger. This is the expensive case and the only one that earns the cost: you authored the
  code, the reviewer called it serious, and you are about to write down that it was wrong. Where
  no subagent is available, the fallback is the one already above — `COULD NOT DETERMINE`, with
  the check named.

  **Carry the write boundary into the delegation, because nothing else will.** A spawned subagent
  does not inherit this skill — it never sees the rule at §7 that keeps this workflow read-only,
  and a general-purpose agent left unrestricted holds every tool its parent session has.

  **Spawn it with a tool allowlist that excludes `Write`, `Edit` and `NotebookEdit`**, and be
  exact about what that buys. In Claude Code the mechanism is the subagent's own definition: an
  agent file whose frontmatter declares `tools: Read, Bash, Glob, Grep` holds only those, whereas
  an unnamed general-purpose subagent inherits everything the parent has. So pick an existing
  agent type already defined read-only, or define one; do not select the default and hope.

  **The allowlist bounds which tools exist, not what they may write, and `Bash` is a write
  capability.** A verifier holding `Bash` can create, replace or delete files through redirection,
  `sed -i`, a formatter, or a script — and Anthropic's own permissions documentation is explicit
  that `Read` and `Edit` deny rules *"don't apply to arbitrary subprocesses that read or write
  files indirectly, like a Python or Node script that opens files itself"*
  (https://code.claude.com/docs/en/permissions). So a `Bash`-holding verifier is **trusted, not
  confined**, and the instruction below is the only thing standing between it and the target.
  Where the claim can be established without a shell, drop `Bash` from its list too and get the
  confinement rather than the promise; where it cannot, say in the ledger that the verifier held
  a write-capable tool.
  Then say the boundary in the delegation message as well: it is inspecting the code to establish
  whether a mechanism holds, and it edits nothing, runs nothing that writes, and reports back in
  prose. A second opinion that modifies the target while forming itself has destroyed the thing
  both of you were reading.

  **Where you cannot restrict its tools**, the second opinion still counts — but say so in the
  ledger beside the verdict it supports: that the verifier ran unbounded is a fact about the
  evidence, and a reader who is not told assumes otherwise.

  **What the allowlist does not buy — and this goes in the ledger too.** Excluding `Write` and
  `Edit` stops the verifier modifying the target. It does nothing about *reading*: the report
  is in the directory you spawned it into, and it kept `Read`, `Glob` and `Bash`. Real
  blindness takes a **sanitized copy** — a scratch directory holding the claim card and only
  the source files the claim concerns — and where you build one, say so. **Where you do not,
  the second opinion still counts, and you write beside the verdict that the verifier could
  have read the report.** Both facts are about the strength of the evidence, and a reader who
  is not told will assume the stronger one. Never write "blind" for a check that was merely
  uninformed.
