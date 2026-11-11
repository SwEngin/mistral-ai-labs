# Day 02, Lab 02: Document Annotations and Structured Extraction

**55 minutes · Hands-on experiments**

## Scenario

A finance team receives supplier invoices with different layouts. Extract
invoice details and line items from fictional PDFs into a validated Pydantic
object for a downstream accounting workflow.

Lab 1 extracted Markdown and document structure. Here, a single OCR request
also asks for a schema-constrained **document annotation** covering the whole
document. A **BBox annotation** instead describes an identified image region;
it is an optional instructor demonstration, not a required exercise.

## Prerequisites and setup

- Python 3.10+, internet access, and a Mistral API key with OCR access.
- The hosted API receives the entire PDF. Use only fictional or approved
  documents and follow your organization's data-handling rules.

From the repository root on macOS/Linux:

```bash
cd labs/day02/02-document-annotations
python3 --version  # Must be 3.10 or later
python -m pip install -r ../../../requirements.txt
```

Set `MISTRAL_API_KEY` using the training center's approved method, or create
a local `.env` file containing `MISTRAL_API_KEY=your-key`. Do not print or
commit the key. To check a non-empty environment variable without revealing it:

```bash
python -c "import os; print('Key is set' if os.environ.get('MISTRAL_API_KEY') else 'Key is not set in the environment')"
```

This check does not read `.env`; the application does. Check the SDK import:

```bash
python -c "from mistralai.client import Mistral; from mistralai.extra import response_format_from_pydantic_model; print('SDK imports OK')"
```

## Required — schema and first extraction

1. Open `data/invoice.pdf`. Complete **TODOs 1–2** in `schemas.py`: add the
   line-item price fields, nullable subtotal and tax fields with `None`
   defaults, and a required total. The invoice contains a list of items.
2. Complete **TODO 3** in `extract_invoice.py`: read and Base64-encode the
   PDF, call `client.ocr.process()` using a `document_url` PDF data URL, and
   pass the Pydantic schema through `response_format_from_pydantic_model()` as
   `document_annotation_format`. Add a prompt asking the model not to invent
   missing information. Use `mistral-ocr-latest`.
3. Complete **TODO 4**: inspect `response.document_annotation`, explicitly
   reject a missing or empty annotation, then validate the JSON with
   `Invoice.model_validate_json()`. The starter prints the resulting object
   as JSON. Refer to the [annotation documentation](https://docs.mistral.ai/studio/document-processing/annotations)
   and [OCR documentation](https://docs.mistral.ai/studio/document-processing/basic_ocr).

```bash
python extract_invoice.py
```

**Success:** a validated invoice object is printed as JSON with two line items.
Compare its fields and amounts with the source PDF; Pydantic validation does
not prove that extraction is factually correct. Before completing the TODOs,
the starter intentionally raises `NotImplementedError`.

## Exploration — a new field and a different layout

Complete **TODO 5**: add `purchase_order_number: str | None` to the
schema, with an instruction to use it only if explicitly present. Rerun the
first invoice and check the new field. Then process the second PDF without
changing the extraction code:

```bash
python extract_invoice.py data/invoice_alternative.pdf
```

Compare its line items and totals against the PDF. What happened to the
optional purchase order, due date and VAT ID? A different layout may produce
different extraction errors, even with the same schema.

## Bonus — validate amounts

Complete **TODO 6**: if both subtotal and tax amount are present, check their
sum against total using `math.isclose` with `rel_tol=0.0` and `abs_tol=0.01`.
Raise an explicit error on a mismatch. Test a matching total and a deliberately
incorrect total locally without making another API call. This illustrates an
arithmetic check; production financial systems generally need decimal
arithmetic and explicit rounding rules.

## Reference values and discussion

These are **fictional source values**, not recorded model outputs:

| Field | First invoice | Alternative invoice |
| --- | --- | --- |
| Invoice number | INV-2026-1042 | Not explicitly labeled; see below |
| Supplier | Example Components GmbH | Training Parts Supply |
| Subtotal | EUR 300.00 | EUR 180.00 |
| Tax | EUR 57.00 | EUR 36.00 |
| Total | EUR 357.00 | EUR 216.00 |
| Supplier VAT ID | Not specified | Not specified |
| Purchase order | PO-1042 | Not specified |
| Due date | 2026-05-01 | Not specified |

The alternative PDF labels `ALT-2026-008` as **Reference**, not invoice
number. Interpreting it as the invoice number is plausible but not explicitly
supported by that label. Compare the model's answer with the source and
discuss whether the application should flag the ambiguity for human review.
The current schema requires an `invoice_number` string, so it cannot
represent an unknown value as `null`; schema validity is not proof of
factual certainty.

Compare every item, date, unit price, currency and total with the PDF. What
would happen if the output has valid types but incorrect amounts? How would you
handle missing information, arithmetic errors and human review?

Document annotation requests are limited to eight pages according to Mistral's
documentation; both supplied invoices have one page.