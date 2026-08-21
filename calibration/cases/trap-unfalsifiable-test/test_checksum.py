from checksum import compute_checksum, verify_checksum


def test_roundtrip_accepts_matching_payload():
    payload = b"invoice-2026-08-21"
    assert verify_checksum(payload, compute_checksum(payload))


def test_returns_a_boolean():
    assert verify_checksum(b"x", compute_checksum(b"x")) is True


def test_digest_is_stable():
    assert compute_checksum(b"abc") == compute_checksum(b"abc")
