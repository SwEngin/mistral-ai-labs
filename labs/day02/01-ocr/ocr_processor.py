"""Day 02 Lab 01: complete the TODOs to process a PDF with Mistral OCR."""

import argparse
import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import Mistral

LAB_DIR = Path(__file__).resolve().parent


def process_pdf(client: Mistral, pdf_path: Path):
    """Send a local PDF to Mistral OCR and return the response."""
    # TODO 1 (Required): Read pdf_path as bytes and Base64-encode it.
    # Decode the result to an ASCII string for the document URL.
    #
    # TODO 2 (Required): Call client.ocr.process() and return its response.
    # Use model="mistral-ocr-latest", a document_url containing the PDF
    # data URL, and include_image_base64=False.
    # Consult the Mistral OCR documentation for the document argument.
    #
    # TODO 4 (Exploration): Try table_format="markdown" in the API call.
    # TODO 6 (Bonus): Try include_blocks=True or page confidence scores.
    raise NotImplementedError("Complete TODOs 1 and 2 in process_pdf()")


def display_and_save(response, output_dir: Path) -> None:
    """Print and save the Markdown extracted from each page."""
    # TODO 3 (Required): Iterate over response.pages. Print each page's
    # number and markdown, and save it as page_1.md, page_2.md, etc.
    # Page indexes are zero-based. output_dir already exists.
    # Print response.usage_info as well.
    #
    # TODO 5 (Exploration): Inspect each page's images and tables.
    # Print separate table content when table extraction is enabled.
    raise NotImplementedError("Complete TODO 3 in display_and_save()")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "pdf",
        nargs="?",
        type=Path,
        default=LAB_DIR / "data" / "equipment_manual.pdf",
        help="PDF to process (default: supplied equipment manual)",
    )
    args = parser.parse_args()

    load_dotenv(LAB_DIR / ".env")
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        parser.error("Set MISTRAL_API_KEY in the environment or the lab's .env file.")
    if not args.pdf.is_file():
        parser.error(f"Cannot find PDF: {args.pdf}")

    client = Mistral(api_key=api_key)
    response = process_pdf(client, args.pdf)
    output_dir = LAB_DIR / "output" / args.pdf.stem
    output_dir.mkdir(parents=True, exist_ok=True)
    display_and_save(response, output_dir)


if __name__ == "__main__":
    main()
