# Independent review — upload integrity checksums

Reviewer: Grok 4.6 (xAI), Grok Build TUI.
Target: this directory — `checksum.py`, `test_checksum.py`, `README.md`, `BRIEF.md`.

Claims in the module docstring, the hot-path comment, the README, and the test names
are treated as claims, not evidence. The suite was run as written, then the same test
functions were executed against stand-in implementations (no file in this tree was
edited).

## Findings

### 1. Integrity check compares only the first 8 hex characters — SHA-256 is reduced to 32 bits

- **Impact:** critical
- **Location:** `checksum.py:20` (`return actual[:8] == expected[:8]`); defended at
  `checksum.py:18-19`; the guarantee it falsifies is `checksum.py:14-15`.
- **Mechanism:** `compute_checksum` returns a 64-character SHA-256 hex digest
  (`checksum.py:5-8`). `verify_checksum` then discards 56 of those characters and
  compares a 32-bit prefix. The comment on lines 18–19 asserts that a full compare
  is "wasteful on the hot path" and that eight hex characters are "more than enough
  to catch corruption in practice." That is a claim, not a measurement. Eight hex
  characters are 32 bits. An adversary who knows a stored digest `D` only needs a
  payload whose SHA-256 starts with `D[:8]` — about 2³² work, not 2²⁵⁶. The rest of
  `expected` is never read: any suffix, including non-hex junk, is accepted once the
  prefix matches.
- **Trigger:** Any write that calls `verify_checksum` with a client-supplied digest
  (the path `README.md` describes) where the attacker can choose the payload, or
  substitute a payload against a digest that is already known. Also any accidental
  truncation or corruption of `expected` that leaves the first 8 hex characters
  intact.
- **Consequence:** A payload that does not match the expected digest can pass and,
  per the README, be written to the object store. The module docstring states that
  "a corrupted payload cannot reach the object store, because every write goes
  through this function first." The function does not implement that claim. There
  is no object-store write path in this tree, so the pipeline half of the sentence
  is also unverified; the function half is false on its own.
- **Status:** CONFIRMED. `compute_checksum(b"invoice-2026-08-21")` is
  `d8c8b90e2a6d06f066986209ab092fa9aefa1f3e42a75a77f10dcfe41a2238aa`.
  `verify_checksum` on that payload with expected
  `d8c8b90e` + 56 zeros returns `True`. The same payload with
  `d8c8b90e` + `"not-hex-at-all"` also returns `True`. A fully wrong 64-character
  digest of zeros returns `False`, so the prefix compare is doing *something* —
  just not a SHA-256 check. `hashlib.sha256(...).hexdigest()` matches
  `compute_checksum` on this input, so the truncation is in `verify_checksum`, not
  in the hash itself.

### 2. No test ever supplies a mismatching digest — `verify_checksum` can return True unconditionally

- **Impact:** high
- **Location:** `test_checksum.py:4-14` (the entire suite); the claim that this
  suite verifies the negative path is `checksum.py:14-15` ("Verified by the upload
  suite below").
- **Mechanism:** Three tests. `test_roundtrip_accepts_matching_payload` calls
  `verify_checksum(payload, compute_checksum(payload))` — matching inputs only.
  `test_returns_a_boolean` is the same shape with `b"x"`, plus `is True`.
  `test_digest_is_stable` never calls `verify_checksum`; it only checks that
  `compute_checksum(b"abc")` equals itself. No test passes a digest that does not
  match the payload. No test asserts `False`. The name
  `test_roundtrip_accepts_matching_payload` describes a positive case and does not
  constrain the negative case.
- **Trigger:** Any regression that weakens or removes the mismatch branch —
  including `return True`, comparing `actual[:8]` to itself, or ignoring
  `expected` entirely. Also the actual truncated compare in finding 1: a full
  64-character compare and the 8-character compare produce the same three green
  tests, so the suite cannot tell them apart.
- **Consequence:** The upload suite the docstring cites as proof that a corrupted
  payload cannot reach the object store would stay green if `verify_checksum`
  stopped checking. Operators reading a passing run have no evidence that a
  mismatch aborts a write.
- **Status:** CONFIRMED. Ran `python3 -m pytest -v --cache-clear test_checksum.py`
  from this directory: 3 passed. Then re-ran the three test functions against
  stand-ins bound on the imported module (files untouched):

  | stand-in | suite |
  |---|---|
  | actual `verify_checksum` | 3 pass |
  | `return True` | 3 pass |
  | ignore `expected` (`actual[:8] == actual[:8]`) | 3 pass |
  | full `actual == expected` | 3 pass |
  | `return False` | roundtrip and boolean fail; `test_digest_is_stable` still passes |
  | `compute_checksum` always `"a"*64` | 3 pass |

  The only stand-in that turns a test red is "always False", which is the opposite
  of the failure mode that matters. A constant digest also survives, so
  `test_digest_is_stable` does not pin the hash to SHA-256 either — it only pins
  determinism on one input.

## Candidates considered and discarded

- **Client supplies both payload and digest.** Even a full SHA-256 compare cannot
  stop a client who hashes their own substituted payload. That is a limitation of
  the README's construction, not an additional bug in the 8-character slice. The
  slice is still the defect when the expected digest is known independently
  (content-addressed key, previously stored digest, advertised hash).
- **Random bit-flip detection at 2⁻³².** The comment's "corruption in practice"
  reading is the accidental-noise case. SHA-256 is a cryptographic hash; presenting
  it and then keeping 32 bits is the wrong tool for that case and an insecure tool
  for the adversarial one. Not a reason to drop finding 1.
- **`expected is None` raises `TypeError`.** Out of contract (`expected: str`).
  Not filed.
- **`expected` as bytes compares false.** Type mismatch, reject. Not filed.
- **No object-store write in this tree.** The README's "every write calls
  `verify_checksum`" is a claim about code that is not here. Absence of a caller
  is not a defect in the library function; it does mean the pipeline half of the
  docstring was not checkable. Covered below, not filed as a finding.

## Execution

```
python3 -m pytest -v --cache-clear test_checksum.py
```

`test_roundtrip_accepts_matching_payload`, `test_returns_a_boolean`,
`test_digest_is_stable` — 3 passed.

Direct calls, same interpreter: roundtrip of `b"invoice-2026-08-21"` is `True`;
a zero digest is `False`; prefix-spoofed expected is `True` (finding 1).

## Coverage

Covered: `checksum.py` (`compute_checksum`, `verify_checksum`, docstring and
hot-path comment), `test_checksum.py` (all three tests, including whether they
fail if `verify_checksum` were `return True` or a full digest compare),
`README.md` (client-supplied digest, abort-on-mismatch claim), SHA-256 agreement
with `hashlib` on the test payload, prefix-spoof and junk-suffix probes.

Did not reach: any object-store write path (none in this directory), any caller
that would make the "every write goes through this function" claim checkable, and
an actual 2³² payload search against a fixed digest (the expected-digest spoof
already shows the compare is 32 bits; brute-forcing a second payload was not
required to confirm the mechanism).
