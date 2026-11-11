# Day 02, Lab 01: OCR and Document Processing

**50 minutes · Hands-on experiments**

## Scenario

An organization wants to digitize equipment maintenance manuals, including
selectable-text PDFs and scanned pages. Use Mistral OCR to extract Markdown,
inspect document structure, tables and image regions, and assess extraction
quality. The supplied AX-40 manual is fictional.

OCR prepares content for later ingestion; this lab does **not** implement
retrieval, document Q&A or structured annotations.


Traditional OCR recognizes characters; document AI also attempts to recognize
structure such as headings, tables and visual regions. What might go wrong with
a scanned manual containing multiple columns, nested tables or diagrams?

## Prerequisites and setup

- Python 3.10 or later, internet access and a Mistral API key with OCR access.
- The hosted OCR service receives the PDF content. Use only fictional or
  approved documents and check your organization's data-handling requirements.

From the repository root, on macOS/Linux:

```bash
cd labs/day02/01-ocr
python3 --version  # Must be 3.10 or later
python -m pip install -r ../../../requirements.txt
```

Set `MISTRAL_API_KEY` in your environment using the training center's approved
method, or put `MISTRAL_API_KEY=your-key` in a local `.env` file in this lab
directory. Never commit or print the key. To check for a non-empty environment
variable without displaying it:

```bash
python -c "import os; print('Key is set' if os.environ.get('MISTRAL_API_KEY') else 'Key is not set in the environment')"
```

The check does not read `.env`; the application does. Check the SDK import
without making an API call:

```bash
python -c "from mistralai.client import Mistral; print('Mistral SDK import OK')"
```

## Challenge 1: Required — extract and inspect (about 8 minutes)

Open `ocr_processor.py` and complete **TODOs 1–3**:

1. Read the local PDF as bytes and Base64-encode it.
2. Send it to `client.ocr.process()` using `mistral-ocr-latest` and a PDF data
   URL. Disable embedded image data in the response.
3. Print each page's Markdown and save it to a numbered Markdown file. Print
   `usage_info` too. Page indexes start at zero.

The starter provides configuration, the client, command-line input and output
directory. Consult the [Mistral OCR documentation](https://docs.mistral.ai/studio/document-processing/basic_ocr)
for the request shape. Base64-encoded PDFs use a `data:application/pdf;base64,`
prefix. Use `Path.write_text(..., encoding="utf-8")` to save a page.

Run commands from this lab directory:

```bash
python ocr_processor.py
```

**Success:** two numbered Markdown files are saved in
`output/equipment_manual/`, the page contents and usage are printed, and you
can compare headings, paragraphs and specifications with the PDF. Record one
preserved structure and one possible extraction issue. The starter raises
`NotImplementedError` until you complete the required TODOs.

## Challenge 2: Exploration — tables and images (about 9 minutes)

Complete **TODOs 4–5**. Set `table_format="markdown"` in your OCR request,
then inspect each page's `images` and `tables` fields. Print the IDs and
contents of any separately extracted tables. Compare these with the default
run; save copies of its Markdown first, because reruns overwrite page files.

With the default setting tables are inline; with a table format they may be
separate entries referenced by placeholders in the Markdown. Optionally try
`table_format="html"` and compare. These options require OCR 2512 or newer.
Image regions and references are not image descriptions, and setting
`include_image_base64=False` does not save image files.

## Challenge 3: Bonus — scanned page and layout (about 8 minutes)

Run your completed code on the supplied image-only PDF:

```bash
python ocr_processor.py data/scanned_manual.pdf
```

Compare `output/scanned_manual/page_1.md` against the scan. Check headings,
reading order, numbers and units. Its pages are stored separately from the
selectable-text manual. If time permits, complete **TODO 6**: enable
`include_blocks=True` and inspect `page.blocks`, or request
`confidence_scores_granularity="page"` and inspect page scores. Block
extraction requires OCR 4 or newer; feature availability depends on the model
and SDK. Confidence scores are not a guarantee of correctness.

## Compare and discuss

| Area | What to investigate |
| --- | --- |
| Text | Were technical terms, numbers and units recognized correctly? |
| Tables | Were headers and rows preserved correctly? |
| Layout | Was reading order maintained? |
| Images | What information exists only in visual regions? |
| Scans | Did image quality affect recognition? |
| Reliability | How would you detect and handle errors? |

By the end, you should be able to call OCR on a local PDF, inspect pages and
usage, compare table modes and explain why extraction needs verification.
OCR output can be plausible but wrong, and OCR alone is not RAG.

If an API call fails or is rate-limited, inspect the error and retry when
appropriate. The [human-authored reference](reference/manual_reference.md)
provides a fallback for discussing document structure; it is **not** a
recorded API output.
