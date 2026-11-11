"""Extract invoice data with Mistral document annotations."""

import argparse
import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import Mistral
from mistralai.extra import response_format_from_pydantic_model

from schemas import Invoice

LAB_DIR = Path(__file__).resolve().parent


def extract_invoice(client: Mistral, pdf_path: Path) -> Invoice:
    """Request a document annotation and validate it as an Invoice."""
    # TODO 3 (Required): Encode pdf_path's bytes as Base64, and call
    # client.ocr.process() with the PDF data URL and model="mistral-ocr-latest".
    # Pass response_format_from_pydantic_model(Invoice) as
    # document_annotation_format. Add a document_annotation_prompt telling the
    # model not to invent missing values.
    #
    # TODO 4 (Required): Check response.document_annotation is a nonempty
    # JSON string. Validate it with Invoice.model_validate_json() and return it.
    # If the annotation is missing, raise an error instead of returning an
    # empty invoice.
    raise NotImplementedError("Complete TODOs 3 and 4 in extract_invoice()")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "pdf",
        nargs="?",
        type=Path,
        default=LAB_DIR / "data" / "invoice.pdf",
        help="PDF to process (default: supplied invoice)",
    )
    args = parser.parse_args()

    load_dotenv(LAB_DIR / ".env")
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        parser.error("Set MISTRAL_API_KEY in the environment or the lab's .env file.")
    if not args.pdf.is_file():
        parser.error(f"Cannot find PDF: {args.pdf}")

    invoice = extract_invoice(Mistral(api_key=api_key), args.pdf)
    print(invoice.model_dump_json(indent=2))

    # TODO 6 (Bonus): If subtotal and tax_amount are available, check whether
    # their sum matches total_amount within one cent; report a mismatch.


if __name__ == "__main__":
    main()
