"""Ask a question using the Document Library tool."""

import argparse
import os

from common import get_client, get_library_id

DEFAULT_QUESTION = "How long are production backups retained?"


def ask_knowledge_base(client, library_id: str, model: str, question: str) -> None:
    # TODO 4 (Required): Start client.beta.conversations.start() with the
    # selected model, question as inputs, store=False, and a document_library
    # tool pointing to library_id. In instructions, request grounded answers,
    # sources, and an explicit response when information is missing.
    # TODO 5 (Required): Inspect response.outputs and display message.output
    # text, tool.execution entries, and any tool_reference citations.
    # If there is no answer text, raise an error instead of reporting success.
    # TODO 6 (Exploration): Try the questions in tests/test_questions.md.
    # TODO 7 (Bonus): Evaluate source accuracy and unsupported questions.
    raise NotImplementedError("Complete TODOs 4 and 5 in ask_knowledge_base()")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--question", default=DEFAULT_QUESTION)
    args = parser.parse_args()
    if not args.question.strip():
        parser.error("Question must not be empty.")
    library_id = get_library_id()
    client = get_client()
    model = os.environ.get("MISTRAL_MODEL", "mistral-medium-latest")
    ask_knowledge_base(client, library_id, model, args.question)


if __name__ == "__main__":
    main()
