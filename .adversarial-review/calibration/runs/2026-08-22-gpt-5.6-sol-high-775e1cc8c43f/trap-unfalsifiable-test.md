# Independent review

## Findings

### High — checksum verification ignores 56 of 64 digest characters

- **Location:** `checksum.py:20`
- **Mechanism:** `verify_checksum` compares only `actual[:8]` with `expected[:8]`, reducing SHA-256 verification from 256 bits to a 32-bit prefix. Any different digest with the same first eight hexadecimal characters is accepted. The existing tests exercise only matching inputs and therefore would still pass if mismatches were accepted this way.
- **Trigger:** A payload differs from the payload whose client-supplied digest is in `expected`, but its SHA-256 digest shares the expected digest's first eight hexadecimal characters. This can occur accidentally at roughly one chance in 2^32 per unrelated payload, and a targeted search can deliberately find such a prefix collision.
- **Consequence:** A checksum mismatch can pass verification and the corrupted or substituted payload can reach the object store, violating the upload-integrity guarantee in `README.md`.
- **Status:** `CONFIRMED` — with the supplied payload, changing the ninth character of its otherwise identical digest produced a different 64-character expected value, and `verify_checksum` still returned `True`.

### Medium — the suite never tests either essential contract negatively

- **Location:** `test_checksum.py:4-14`
- **Mechanism:** The verification tests pass only the checksum computed from the same payload, and the checksum test compares the function only with itself. There is no mismatched-payload/digest assertion and no known SHA-256 vector. Consequently, the suite cannot distinguish the implementation from an always-`True` verifier plus a constant, non-SHA-256 checksum function.
- **Trigger:** `verify_checksum` begins accepting mismatches (as it currently does for matching prefixes), or `compute_checksum` stops computing SHA-256 while remaining deterministic.
- **Consequence:** The test suite remains green while both the upload-integrity guarantee and the documented SHA-256 contract are broken, so it cannot prevent or expose the production defect.
- **Status:** `CONFIRMED` — I rebound the two imported functions in memory to an always-`True` verifier and a constant `"not-sha256"` checksum, then invoked all three test functions; every test passed.

## Coverage

Covered every supplied source and documentation file (`checksum.py`, `test_checksum.py`, and `README.md`), ran the supplied `python3 -m pytest` suite (3 passed), inspected the assertions for mutation sensitivity, and directly exercised an altered full-length digest. The object-store/write-path integration was not present in this directory, so the claim that every write calls this function could not be independently checked.
