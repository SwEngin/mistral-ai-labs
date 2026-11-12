"""Prepared Mistral agent using the same local inventory MCP server."""

import argparse
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from mistralai import agents

MCP_URL = "http://127.0.0.1:8000/mcp"
DEFAULT_QUESTION = (
    "Can we fulfill an order for 8 units of SKU-204? "
    "Explain any stock shortfall."
)


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()
    if not args.question.strip():
        parser.error("Question must not be empty.")
    load_dotenv(Path(__file__).resolve().parent / ".env")
    if not os.environ.get("MISTRAL_API_KEY"):
        parser.error("Set MISTRAL_API_KEY in the environment or this lab's .env.")
    agent = agents.Agent(
        name="inventory-assistant",
        model=os.environ.get("MISTRAL_AGENT_MODEL", "mistral-large-4"),
        instructions=(
            "Use the inventory tools to answer questions. Do not invent quantities. "
            "Report missing tools or errors and do not modify inventory or place orders."
        ),
        mcps={"inventory": agents.RemoteMCP(url=MCP_URL, model_access="direct")},
    )

    def show_event(event) -> None:
        if isinstance(event, agents.Notice):
            print(f"Notice ({event.level}): {event.message}", flush=True)

    result = await agent.run(args.question, on_event=show_event)
    if not isinstance(result, agents.Completed):
        raise RuntimeError(f"Agent did not complete: {result!r}")
    if not result.text or not result.text.strip():
        raise RuntimeError("Agent completed without a text answer.")
    if not result.tool_calls:
        print("Warning: no tool calls were recorded; verify the answer.")
    for call in result.tool_calls:
        print(f"Tool call: {call.name}; arguments: {call.arguments}")
    print(f"\nAnswer: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
