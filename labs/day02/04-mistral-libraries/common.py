"""Shared configuration for the Libraries workshop."""

import os
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import Mistral

LAB_DIR = Path(__file__).resolve().parent
LIBRARY_ID_FILE = LAB_DIR / "library_id.txt"


def get_client() -> Mistral:
    load_dotenv(LAB_DIR / ".env")
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("Set MISTRAL_API_KEY in the environment or the lab's .env file.")
    return Mistral(api_key=api_key)


def get_library_id() -> str:
    try:
        library_id = LIBRARY_ID_FILE.read_text(encoding="utf-8").strip()
    except FileNotFoundError as exc:
        raise FileNotFoundError("Run create_library.py first; library_id.txt is missing.") from exc
    if not library_id:
        raise ValueError("library_id.txt is empty; provide the ID of your practice library.")
    return library_id
