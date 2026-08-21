"""Reports page query layer."""


def run_report(filters: dict) -> list[dict]:
    """Return the rows matching filters, newest first."""
    rows = _query(filters)
    return sorted(rows, key=lambda r: r["created_at"], reverse=True)


def _query(filters: dict) -> list[dict]:
    raise NotImplementedError("wired to the warehouse client in production")
