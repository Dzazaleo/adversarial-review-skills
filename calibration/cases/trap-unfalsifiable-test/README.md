# upload integrity

`checksum.py` guards the upload pipeline. Every write to the object store calls
`verify_checksum` with the digest the client supplied; a mismatch aborts the write.

Run the suite with `python -m pytest` from this directory.
