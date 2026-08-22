# Independent review

## Findings

### 1. High — checksum verification does not verify the supplied SHA-256 digest

- **Location:** `checksum.py:18-20`
- **Mechanism:** `verify_checksum` compares only the first eight hexadecimal characters (32 bits) of the computed and expected digests, rather than comparing the full SHA-256 value. Any expected value with the same eight-character prefix is accepted even when its remaining 56 characters differ. The supplied tests do not exercise a mismatch, so they cannot substantiate the docstring's corruption-prevention claim.
- **Trigger:** A caller supplies any string whose first eight characters match the payload's SHA-256 digest, including a different 64-character digest, a digest truncated to eight characters, or a matching prefix followed by non-hexadecimal text. For corruption against a previously fixed digest, any changed payload that collides on the first 32 bits also triggers it.
- **Consequence:** The verifier reports a checksum match for a non-matching client-supplied digest, weakening an intended 256-bit integrity check to a 32-bit prefix check and allowing colliding or deliberately altered checksum values through the upload guard.
- **Status:** CONFIRMED — direct probes showed `True` for (1) a different 64-character digest with a changed ninth character, (2) only the correct eight-character prefix, and (3) that prefix followed by non-hexadecimal text.

### 2. Medium — the upload suite cannot detect failure to reject bad checksums

- **Location:** `test_checksum.py:4-14` (and the unsupported verification claim at `checksum.py:14-15`)
- **Mechanism:** Both verifier assertions supply the checksum computed from the same unchanged payload and expect `True`; the remaining test merely computes the same checksum twice. There is no assertion for a corrupted payload, a mismatched digest, a truncated digest, or malformed input. Consequently, even an implementation that always accepts inputs satisfies the verifier tests.
- **Trigger:** `verify_checksum` regresses to accepting a mismatch, as the current prefix-only implementation already does.
- **Consequence:** CI remains green while the upload integrity guard admits invalid checksums, and the suite gives false confidence for the explicit claim that corrupted payloads cannot reach storage.
- **Status:** CONFIRMED — the supplied suite reported `3 passed`, while targeted mismatch and malformed-input probes against that same implementation demonstrated the false accepts in finding 1.

### 3. Low — the documented test command is unavailable in the audited environment

- **Location:** `README.md:6`
- **Mechanism:** The README instructs running `python -m pytest`, but this environment exposes Python as `python3` and has no `python` executable.
- **Trigger:** Following the documented command in this directory in the provided environment.
- **Consequence:** The documented verification step terminates immediately with `zsh: command not found: python`; a reviewer or developer must infer the `python3 -m pytest` replacement.
- **Status:** CONFIRMED — the documented command failed, while `python3 -m pytest -q` ran successfully and reported all three tests passing.

## Coverage

Covered every file in the directory (`README.md`, `checksum.py`, `test_checksum.py`, and `BRIEF.md`); ran the documented test command, the suite via the available Python 3 interpreter, and targeted full-length mismatch, truncated-digest, and malformed-suffix probes. Did not exercise an actual changed-payload 32-bit prefix collision or an object-store integration path, because no upload/object-store implementation is present in scope.
