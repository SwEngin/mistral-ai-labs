"""Call a documentation tool directly, without a Mistral conversation."""

import argparse
import asyncio

from common import get_client, get_connector_id

QUESTION = "What is the role of SQLite's Virtual Database Engine?"


async def call_documentation_tool(client, connector_id: str, tool: str, question: str):
    # TODO 3 (Required): For "structure", call read_wiki_structure with
    # {"repoName": "sqlite/sqlite"} using call_tool_async.
    # TODO 4 (Exploration): For "question", call ask_wiki_question with
    # repoName and question. Return the complete tool response.
    raise NotImplementedError("Complete TODO 3 and TODO 4: call MCP tools")


def display_result(result) -> None:
    # TODO 5 (Required): Inspect result.content; print text blocks and
    # report any other block types. Report if no text is returned or if
    # result.metadata.mcp_meta.is_error indicates a tool error. The SDK
    # represents absent optional metadata with Unset.
    raise NotImplementedError("Complete TODO 5: inspect the tool response")


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", choices=("structure", "question"), default="structure")
    parser.add_argument("--question", default=QUESTION)
    args = parser.parse_args()
    if args.tool == "question" and not args.question.strip():
        parser.error("Question must not be empty.")
    response = await call_documentation_tool(
        get_client(), get_connector_id(), args.tool, args.question
    )
    display_result(response)


if __name__ == "__main__":
    asyncio.run(main())
