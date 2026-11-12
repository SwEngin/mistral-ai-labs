"""Build an incident investigation agent using local function tools."""

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import Mistral

from incident_tools import get_incident_details, get_recent_deployments, get_service_health

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_QUESTION = (
    "Investigate incident INC-1042. Which service is affected, what is its "
    "current health, and was there a recent deployment that might be relevant?"
)
MAX_MODEL_REQUESTS = 8

# TODO 1 (Required): Write instructions to investigate using the tools,
# acknowledge missing information and distinguish correlation from root cause.
INSTRUCTIONS = ""

# TODO 2 (Required): Describe all three functions using Mistral function tool
# schemas. Define required string parameters incident_id or service_name.
TOOLS = []


def run_agent(client: Mistral, model: str, question: str) -> str:
    """Investigate a question through a bounded model/tool conversation."""
    # TODO 3 (Required): Send a system message and user question to
    # client.chat.complete(), passing TOOLS and tool_choice="auto".
    # Inspect the assistant message and handle a text-only final response.
    #
    # TODO 4 (Required): For every requested function call, display its name
    # and arguments, execute only the three supplied functions, and display
    # the result. Add the assistant message and one tool result per call to
    # the conversation using the matching tool_call_id. Continue until the
    # model answers; stop explicitly at MAX_MODEL_REQUESTS. Report missing
    # choices, missing call IDs and missing final text.
    #
    # TODO 5 (Exploration): Validate tool names and JSON argument shape.
    # Investigate INC-9999 and INC-1043. Return tool error objects to the
    # model, rather than fabricating data or treating them as successful facts.
    raise NotImplementedError("Complete TODOs 1–5 in the incident agent")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()
    if not args.question.strip():
        parser.error("Question must not be empty.")
    load_dotenv(ROOT / ".env")
    key = os.environ.get("MISTRAL_API_KEY")
    if not key:
        parser.error("Set MISTRAL_API_KEY in the environment or repository .env.")
    model = os.environ.get("MISTRAL_MODEL", "mistral-small-latest")
    print(f"User: {args.question}")
    answer = run_agent(Mistral(api_key=key), model, args.question)
    print(f"\nFinal answer: {answer}")


if __name__ == "__main__":
    main()
