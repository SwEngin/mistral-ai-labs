"""Fictional, read-only travel search tools for the capstone scenario."""

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data" / "options.json"


def _options() -> dict:
    with DATA.open(encoding="utf-8") as file:
        return json.load(file)


def search_transport(origin: str, destination: str, date: str) -> list[dict]:
    """Return fictional round-trip tickets only for the specified scenario."""
    if (origin.strip().casefold(), destination.strip().casefold(), date) != (
        "nuremberg", "hamburg", "2026-12-02"
    ):
        raise ValueError("No fictional transport data for this route and departure date.")
    return _options()["transport"]


def search_hotels(city: str, check_in: str, check_out: str) -> list[dict]:
    """Return fictional hotel rates only for the specified scenario."""
    if (city.strip().casefold(), check_in, check_out) != (
        "hamburg", "2026-12-02", "2026-12-04"
    ):
        raise ValueError("No fictional hotel data for this city and stay.")
    return _options()["hotels"]
