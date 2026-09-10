# Independent review — upload integrity (`checksum.py`)

Reviewer: Grok 4.6 (xAI). Work under review is treated as authored by a different model; comments, docstrings, and test names are claims, not evidence.

Scope: `checksum.py`, `test_checksum.py`, `README.md`, `BRIEF.md`. No git history in this directory.

`python3 -m pytest -v` from this directory: 3 passed in 0.01s.

---

## Findings (ranked)

### 1. `verify_checksum` accepts payloads that do not match the expected digest

- **Impact:** high
- **Status:** CONFIRMED
- **Location:** `checksum.py:20` (`return actual[:8] == expected[:8]`), against the contract at `checksum.py:12` and the write-gate description at `README.md:3-4`

- **Mechanism:**
  `compute_checksum` returns a 64-character SHA-256 hex digest (`checksum.py:8`). `verify_checksum` then discards 56 of those characters and compares only the first 8 hex digits (32 bits). The function therefore returns `True` for many `(payload, expected)` pairs where `compute_checksum(payload) != expected`.

  The nearby comment (`checksum.py:18-19`) presents this as an intentional hot-path optimisation. That comment is the party under review talking: it does not change the contract (“Return True when payload matches the expected digest”), and it is false on its own terms — line 17 already computed the full SHA-256, so the compare is not the cost.

- **Trigger:**
  Any payload whose SHA-256 hex shares an 8-character prefix with `expected`. Demonstrated with two distinct 4-byte payloads found by a birthday search over ~2²⁰ SHA-256 evaluations:

  ```
  p1 = bytes.fromhex("eb2f0000")
  p2 = bytes.fromhex("cb800000")
  compute_checksum(p1) == "dc478bbc7eea087d9cf5deb42b4c3949341bead6bde8a10805e293ab73c413f7"
  compute_checksum(p2) == "dc478bbc58142699700491b82da00294cb5f2666f8d64e19696fda4d457b5ba0"
  verify_checksum(p2, compute_checksum(p1)) is True
  verify_checksum(p1, compute_checksum(p2)) is True
  p1 == p2 is False
  compute_checksum(p1) == compute_checksum(p2) is False
  ```

  Same-payload, wrong-suffix digest also accepts (the stored/client digest can be corrupted after byte 8 and still pass):

  ```
  payload = b"invoice-2026-08-21"
  expected = compute_checksum(payload)[:8] + ("0" * 56)
  # expected == "d8c8b90e00000000000000000000000000000000000000000000000000000000"
  verify_checksum(payload, expected) is True
  ```

  An 8-character `expected` is enough: `verify_checksum(payload, compute_checksum(payload)[:8]) is True`.

  Finding a second preimage for a *fixed* digest is ~2³² SHA-256 evaluations — practical on a laptop GPU in seconds, not a 2²⁵⁶ problem.

- **Consequence:**
  README states that every object-store write calls this function with the client digest and that a mismatch aborts the write. Callers that take a `True` return as “payload matches digest” will persist a body that does not match the digest they were given. Accidental random corruption is still usually caught (~2⁻³² false accept per independent payload), but the advertised SHA-256 check is not what runs, and an attacker who can choose the body for a known `expected` can search into an accept.

---

### 2. The upload suite cannot fail the integrity property it is cited as proving

- **Impact:** high
- **Status:** CONFIRMED
- **Location:** `test_checksum.py:4-14`, cited as proof at `checksum.py:14-15`

- **Mechanism:**
  The docstring of `verify_checksum` says the upload suite verifies that “a corrupted payload cannot reach the object store”. The three tests only ever call `verify_checksum` with a digest just computed from the same payload:

  | test | what it asserts | negative case? |
  |---|---|---|
  | `test_roundtrip_accepts_matching_payload` (`test_checksum.py:4-6`) | matching invoice bytes verify | no |
  | `test_returns_a_boolean` (`test_checksum.py:9-10`) | matching `b"x"` returns `True` (identity) | no |
  | `test_digest_is_stable` (`test_checksum.py:13-14`) | `compute_checksum` is deterministic | never calls `verify_checksum` |

  If the property “mismatch is rejected” were false, these tests would not fail. They were replayed in-process against substitute oracles, without modifying repo files:

  | oracle | all three tests |
  |---|---|
  | always `True` | pass |
  | compare first 8 hex chars (as shipped) | pass |
  | compare first 1 hex char | pass |
  | full digest equality | pass |
  | always `False` | fail (roundtrip + boolean only) |

  So the suite distinguishes “never accept” from “accept on match”, and nothing else. It does not distinguish full SHA-256 from a 4-bit prefix compare, and it does not distinguish a real verifier from `return True`.

  A naive mismatch such as `verify_checksum(b"invoice-2026-08-22", compute_checksum(b"invoice-2026-08-21"))` is in fact `False` today — the shipped function is not always-true — but no test makes that assertion, and even that assertion would still pass under 8-hex truncation for ordinary fixtures. Catching finding 1 requires a colliding pair or an expected digest that matches only the prefix.

- **Trigger:**
  Any CI run of `python3 -m pytest`. Observed: 3 passed. The same command stays green under the always-`True` and prefix-1 oracles above.

- **Consequence:**
  The only automated gate for this module cannot detect the production false-accept (finding 1) and cannot detect a verifier that accepts every payload. A green run is being used in-source as evidence that corrupted bodies cannot be written. That evidence is not capable of being wrong, so it cannot support the claim.

---

## Notes (not ranked)

- **Author comment at `checksum.py:18-19` looks deliberate.** Reported as finding 1 rather than dismissed. The performance claim does not hold: the full hash is already computed at line 17.
- **No object-store write path is in this directory.** “Every write goes through this function first” (`checksum.py:15`, `README.md:3-4`) is an integration claim with no caller to execute. Function-level false accepts are CONFIRMED; that every real write uses this function is COULD NOT DETERMINE (would need the pipeline).
- **Uppercase hex is rejected:** `verify_checksum(payload, compute_checksum(payload).upper()) is False`. Fail-closed; no stated case contract. Not ranked.
- **`compute_checksum` itself matches `hashlib.sha256(...).hexdigest()`** on the fixtures above. The defect is the compare, not the hash.

---

## Claims examined

| Claim | Source | Result |
|---|---|---|
| `compute_checksum` returns hex SHA-256 | `checksum.py:6-8` | Upheld by matching `hashlib.sha256` on the invoice fixture and the collision pair |
| `verify_checksum` returns True iff payload matches the expected digest | `checksum.py:12` | Refuted — finding 1 |
| First 8 hex chars are enough to catch corruption in practice | `checksum.py:18-19` | Refuted as a SHA-256 substitute — colliding bodies accepted (finding 1) |
| Upload suite verifies a corrupted payload cannot reach the object store | `checksum.py:14-15` | Refuted — finding 2; tests would not fail if the claim were false |
| Every object-store write calls `verify_checksum`; mismatch aborts | `README.md:3-4` | COULD NOT DETERMINE — no write path in tree |
| Matching payloads verify; digest is stable | `test_checksum.py` | Upheld for those fixtures; does not uphold mismatch rejection |

---

## Coverage

Read: `BRIEF.md`, `README.md`, `checksum.py` (20 lines), `test_checksum.py` (14 lines).

Ran: `python3 -m pytest -v` (3 passed); in-process probes for prefix collisions, suffix-tampered `expected`, short `expected`, uppercase `expected`; replay of the three test assertions against always-true / always-false / prefix-1 / prefix-8 / full-equality oracles.

Did not reach: any object-store or HTTP upload caller (none present); a second-preimage search against the invoice fixture (birthday collision already demonstrates the false accept); timing or type-confusion paths (`None` / non-`bytes` payload), which fail closed with `TypeError`.
