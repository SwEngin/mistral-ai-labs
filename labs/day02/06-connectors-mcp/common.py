"""Shared configuration for the connector exercises."""

import os
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import Mistral

LAB_DIR = Path(__file__).resolve().parent
CONNECTOR_ID_FILE = LAB_DIR / "connector_id.txt"


def get_client() -> Mistral:
    load_dotenv(LAB_DIR / ".env")
    key = os.environ.get("MISTRAL_API_KEY")
    if not key:
        raise ValueError("Set MISTRAL_API_KEY in the environment or the lab's .env file.")
    return Mistral(api_key=key)


def get_connector_id() -> str:
    connector_id = CONNECTOR_ID_FILE.read_text(encoding="utf-8").strip()
    if not connector_id:
        raise ValueError("connector_id.txt is empty; check your practice connector in Studio.")
    return connector_id
