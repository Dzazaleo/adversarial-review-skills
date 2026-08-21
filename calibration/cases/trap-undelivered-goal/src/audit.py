"""Operations audit log."""

from datetime import datetime, timezone


def record(actor: str, action: str, detail: dict) -> None:
    """Append one entry to the audit log.

    Callers pass the acting user, a short action verb, and any structured
    detail worth keeping (parameters, filters, target IDs).
    """
    entry = {
        "at": datetime.now(timezone.utc).isoformat(),
        "actor": actor,
        "action": action,
        "detail": detail,
    }
    _append(entry)


def _append(entry: dict) -> None:
    with open("audit.log", "a", encoding="utf-8") as fh:
        fh.write(repr(entry) + "\n")
