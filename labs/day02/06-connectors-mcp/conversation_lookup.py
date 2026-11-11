"""Let a model use an allowlisted documentation connector."""

import argparse
import asyncio
import os

from common import get_client, get_connector_id
from query_connector import QUESTION


async def ask_with_connector(client, connector_id: str, model: str, question: str):
    # TODO 6 (Bonus): Start a conversation with the question and a connector
    # tool restricted to ask_wiki_question for the public sqlite/sqlite
    # repository. Request grounded answers, use store=False, and return
    # the response.
    raise NotImplementedError("Complete TODO 6: start a connector conversation")


def display_conversation(response) -> None:
    # TODO 7 (Bonus): Inspect response.outputs and show tool execution names
    # and assistant answer text. Handle both string and text-chunk content.
    # Report missing answer text and warn if no tool execution is visible.
    raise NotImplementedError("Complete TODO 7: inspect conversation outputs")


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--question", default=QUESTION)
    args = parser.parse_args()
    if not args.question.strip():
        parser.error("Question must not be empty.")
    client = get_client()
    response = await ask_with_connector(
        client, get_connector_id(), os.environ.get("MISTRAL_MODEL", "mistral-small-latest"),
        args.question,
    )
    display_conversation(response)


if __name__ == "__main__":
    asyncio.run(main())
