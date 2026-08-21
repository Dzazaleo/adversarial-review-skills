"""Public API request entry point."""

from store import KeyValueStore

store = KeyValueStore()


def handle_request(tenant_id: str, path: str, body: bytes) -> tuple[int, dict, bytes]:
    """Route one request. Returns (status, headers, body)."""
    if not tenant_id:
        return 401, {}, b""
    record = store.get(f"tenant:{tenant_id}")
    if record is None:
        return 404, {}, b""
    return 200, {"content-type": "application/json"}, body
