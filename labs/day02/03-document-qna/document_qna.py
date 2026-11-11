"""Ask questions about a fictional architecture proposal."""

import argparse
import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import Mistral

LAB_DIR = Path(__file__).resolve().parent
DEFAULT_QUESTION = (
    "What are the three most important non-functional requirements "
    "identified in the proposal?"
)


def ask_document(client: Mistral, model: str, pdf_path: Path, question: str) -> str:
    """Send the PDF and question in one chat request and return the answer."""
    # TODO 1 (Required): Read pdf_path as bytes and Base64-encode it.
    # Form a PDF data URL beginning with "data:application/pdf;base64,".
    #
    # TODO 2 (Required): Call client.chat.complete() with the selected model.
    # Include a system instruction to answer from the document, admit when
    # information is missing, and cite relevant section names.
    # The user message should contain both a text chunk for the question and
    # a document_url chunk holding the PDF data URL.
    #
    # TODO 3 (Required): Extract the assistant's text from the response.
    # If there is no text answer, raise an error instead of returning success.
    #
    # TODO 4 (Exploration): Try a synthesis question and check its sources.
    # TODO 5 (Bonus): Try an unsupported question and refine your instruction.
    raise NotImplementedError("Complete TODOs 1–3 in ask_document()")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "pdf",
        nargs="?",
        type=Path,
        default=LAB_DIR / "data" / "architecture_proposal.pdf",
        help="PDF to analyze (default: supplied architecture proposal)",
    )
    parser.add_argument(
        "--question", default=DEFAULT_QUESTION, help="Question to ask the document"
    )
    args = parser.parse_args()

    load_dotenv(LAB_DIR / ".env")
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        parser.error("Set MISTRAL_API_KEY in the environment or the lab's .env file.")
    if not args.pdf.is_file():
        parser.error(f"Cannot find PDF: {args.pdf}")
    if not args.question.strip():
        parser.error("Question must not be empty.")

    model = os.environ.get("MISTRAL_MODEL", "mistral-small-latest")
    answer = ask_document(Mistral(api_key=api_key), model, args.pdf, args.question)
    print(answer)


if __name__ == "__main__":
    main()
