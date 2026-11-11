# Day 02, Lab 03: Document Q&A

**40 minutes · Hands-on experiments**

## Scenario

An engineering organization is reviewing an architecture proposal
comparing hosted AI inference and self-hosted inference. Build an application
that sends the proposal PDF and a natural-language question to Mistral, then
evaluate the answer against the source.

OCR extracts content; document annotations extract predefined fields; direct
document Q&A answers questions about supplied documents. The Chat Completions
request can contain the PDF and question together; this lab does not require
a separate application-managed OCR call or a persistent search index.

## Setup

Requires Python 3.10+, internet access, and a Mistral API key with access to a
model supporting document inputs. The hosted service receives the PDF and
question: use only fictional or approved material and follow data-handling
requirements.

From the repository root on macOS/Linux:

```bash
cd labs/day02/03-document-qna
python3 --version  # Must be 3.10 or later
python -m pip install -r ../../../requirements.txt
```


Set `MISTRAL_API_KEY` in your environment using the training center's approved
method, or put `MISTRAL_API_KEY=your-key` in a local `.env` file in this lab
directory. Never commit or print the key. To check for a non-empty environment
variable without revealing it:

```bash
python -c "import os; print('Key is set' if os.environ.get('MISTRAL_API_KEY') else 'Key is not set in the environment')"
python -c "from mistralai.client import Mistral; print('Mistral SDK import OK')"
```

The key check does not read `.env`; the application does. The default model is
`mistral-small-latest`, as in the
[Document Q&A documentation](https://docs.mistral.ai/studio/document-processing/document_qna).
Set `MISTRAL_MODEL` in the environment or the lab `.env` to select another
model that supports PDF inputs and is available to your account.

## Required — factual question

Open `data/architecture_proposal.pdf`, then complete **TODOs 1–3** in
`document_qna.py`:

1. Encode the PDF as Base64 and create a PDF data URL.
2. Send one `client.chat.complete()` request with a system instruction and a
   user message containing both a text question and a `document_url` chunk.
   Ask for answers grounded in the document and section names when available.
3. Extract the assistant's text; explicitly report a missing or non-text
   answer instead of treating it as success.

The provided entry point initializes the client and accepts a PDF and question.
The [official documentation](https://docs.mistral.ai/studio/document-processing/document_qna)
shows the message format. A local PDF data URL starts with
`data:application/pdf;base64,`.

Run from the lab directory:

```bash
python document_qna.py
```

The default question asks for the three non-functional requirements.
**Success:** a natural-language answer is printed. Compare each requirement
and section reference against the PDF. The starter intentionally raises
`NotImplementedError` until the required TODOs are complete.

## Exploration — synthesize trade-offs

Complete **TODO 4** by experimenting with a question that combines sections:

```bash
python document_qna.py --question "Compare the deployment alternatives, their advantages and limitations, and explain the recommendation."
```

Does the response distinguish explicit facts from interpretation? Check
the trade-offs and any citations against the PDF. A citation in a model
response is not proof that the cited section exists or supports the claim.

## Bonus — unsupported information

Complete **TODO 5** by trying a question the proposal cannot answer:

```bash
python document_qna.py --question "What was the actual production cost of the chosen architecture during October 2026?"
```

The document contains planning estimates but no actual production costs.
Does the answer acknowledge the gap? If it speculates, refine the system
instruction and repeat; prompts cannot guarantee a correct refusal.
Optionally add an `input()` loop to ask multiple questions. Make clear that
each independent request resends the PDF and has no automatic conversation
memory; each request may incur usage charges.

## Discussion and outcomes

For one-off review, direct document Q&A supplies a document with each
request. A retrieval-based application typically indexes a collection and
retrieves relevant passages first; it is better suited to searching large
collections, though it still needs answer and citation verification.
Which approach would you choose for one contract versus 10,000 documents?

By the end, you should be able to submit a PDF and question, compare factual
and analytical answers with the source, identify missing information and
explain the difference between direct document Q&A and RAG. If API access is
unavailable, use the original PDF for discussion; no model answers are
provided or claimed as observed.
