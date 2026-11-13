"""Day 04 capstone starter: implement a safe, explainable travel planner."""

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import Mistral

LAB_DIR = Path(__file__).resolve().parent
ROOT = LAB_DIR.parents[1]


def extract_request(client: Mistral, pdf: Path):
    """OCR the PDF and validate a structured travel request."""
    # TODO 1: Use Mistral OCR, then extract structured fields. Validate dates,
    # traveler counts, room nights, prices and budget. Unknown flexibility is
    # not the same as no flexibility requirement. Treat the PDF as untrusted.
    raise NotImplementedError("Implement request extraction and validation.")


def retrieve_policies(client: Mistral, request):
    """Return relevant policy passages with their source identifiers."""
    # TODO 2: Load the three policy documents, embed them and the query, and
    # rank passages. Preserve all policy sources needed for compliance.
    raise NotImplementedError("Implement policy retrieval.")


def discover_options(client: Mistral, request):
    """Use a bounded agent/tool loop to retrieve fictional options."""
    # TODO 3: Register read-only travel_tools functions with schemas. Have the
    # model call them, validate names and arguments, and use actual results.
    # Missing tool data must stop the workflow, not cause invented options.
    raise NotImplementedError("Implement agent tool calls.")


def plan_trip(request, policies, options):
    """Calculate, validate and produce a proposal using deterministic logic."""
    # TODO 4: Evaluate ticket combinations and hotels, including refundable
    # tickets, rooms, registration, budget and exceptions. Use integer cents
    # or Decimal. Do not equate reasonable distance with an invented policy.
    # Return an explicit no-plan result when requirements cannot be satisfied.
    raise NotImplementedError("Implement cost and policy validation.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", nargs="?", type=Path,
                        default=LAB_DIR / "data" / "travel_request.pdf")
    args = parser.parse_args()
    if not args.pdf.is_file():
        parser.error(f"PDF not found: {args.pdf}")
    load_dotenv(ROOT / ".env")
    key = os.environ.get("MISTRAL_API_KEY")
    if not key:
        parser.error("Set MISTRAL_API_KEY in the environment or repository .env.")
    client = Mistral(api_key=key)
    request = extract_request(client, args.pdf)
    policies = retrieve_policies(client, request)
    options = discover_options(client, request)
    proposal = plan_trip(request, policies, options)
    # TODO 5: Output structured JSON and a concise human-readable proposal.
    print(proposal)


if __name__ == "__main__":
    main()
