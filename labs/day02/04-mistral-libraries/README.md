# Day 02, Lab 04: Mistral Libraries and Knowledge Retrieval

**65 minutes · Hands-on experiments**

## Scenario

Northstar Cloud, a fictional SaaS company, maintains separate support,
release and backup policies. Create a persistent Mistral Library containing
these documents and ask questions without specifying which document to search.

The service manages document processing, storage, indexing and retrieval.
Your application still needs to check access permissions, freshness,
retrieval relevance, grounding and answer quality. Unlike Lab 3, documents
are uploaded before questions arrive rather than supplied in each request.
No custom chunker or embedding pipeline is implemented in this lab.


## Setup and safety

You need Python 3.10+, internet access, a Mistral API key, permission to create
and delete Libraries in an approved workspace, and access to a compatible
model and Document Library tool. Remote creation, processing and queries may
incur charges. API-key sessions may create workspace-owned Libraries visible
to other authorized workspace members; **do not assume they are private**.
Upload fictional or explicitly approved documents only.

From the repository root, on macOS/Linux:

```bash
cd labs/day02/lab-04-mistral-libraries
python3 --version  # Must be 3.10 or later
python -m pip install -r ../../../requirements.txt
```

Set `MISTRAL_API_KEY` through the training center's approved method or edit
the lab's local `.env`. Never print or commit it. The default query model is
`mistral-medium-latest`; set `MISTRAL_MODEL` to another compatible model if
needed. To check for a non-empty environment key without revealing it:

```bash
python -c "import os; print('Key is set' if os.environ.get('MISTRAL_API_KEY') else 'Key is not set in the environment')"
python -c "from mistralai.client import Mistral; print('Mistral SDK import OK')"
```

The first check does not read `.env`; the scripts do. The lab's `.gitignore`
excludes `.env` and `library_id.txt`. The latter contains a resource ID, not
the API key.

## Required — create, ingest and query

Read the three fictional files in `data/`, then complete **TODOs 1–5**:

1. In `create_library.py`, create a Library using
   `client.beta.libraries.create()`. Print its ID before saving it in
   `library_id.txt`. The provided entry point refuses to create another if
   that file already exists. This is a persistent remote resource.
2. In `upload_documents.py`, upload each file with
   `client.beta.libraries.documents.upload()`, then poll its
   `documents.status()` until `process_status == "done"`. Treat `todo`,
   `in_progress` and `waiting_for_capacity` as pending; report any other
   state as an error. Add a five-minute deadline and a brief polling delay.
   Print each document ID so a failed run can be investigated.
3. In `ask_knowledge_base.py`, call `client.beta.conversations.start()` with
   `inputs=question`, a `document_library` tool containing the saved ID,
   `store=False`, and instructions requesting grounded answers and sources.
   Display tool executions, answer text and any `tool_reference` citations
   from `response.outputs`. Report a missing answer explicitly.

The [official Libraries quickstart](https://docs.mistral.ai/studio/search/libraries/quickstart)
shows the SDK methods. Consult the [Libraries documentation](https://docs.mistral.ai/studio/search/libraries)
for response output types. The starter functions intentionally raise
`NotImplementedError` until completed.

Run these commands **from this lab directory**, in order:

```bash
python create_library.py
python upload_documents.py
python ask_knowledge_base.py
```

**Success:** a library ID is saved, all three documents reach `done`, and
the query prints an answer about backup retention. Inspect whether a
`document_library` tool execution appears, and verify any citations and
answer against `data/backup_policy.md`. A tool execution alone does not
prove that an answer is correct.

The remote library is not automatically deleted. If saving the ID fails,
use the printed ID to recover it in `library_id.txt` or clean up in Studio.
If an upload or status check fails, inspect the printed document IDs and
the Library in Studio **before retrying**; rerunning the whole upload script
can create duplicate documents. A timeout does not mean processing failed
or that the uploaded document was deleted.

## Exploration — multiple documents

Complete **TODO 6** by running the first three questions in
`tests/test_questions.md`, including the cross-document Priority 1/Sunday
emergency-release question:

```bash
python ask_knowledge_base.py --question "If a Priority 1 incident requires an emergency release on Sunday, what support and approval rules apply?"
```

Check whether the answer covers both support availability and release
approval. Compare claims and source references with both policy files.

## Bonus — missing information and evaluation

Complete **TODO 7**: ask which database engine Northstar Cloud uses. No
provided policy specifies one. Does the answer acknowledge that? Record
observations in the worksheet and evaluate retrieval relevance, correctness,
grounding, completeness, abstention and source attribution. If an answer
cites a source, verify it; the instruction to cite or abstain is not a
guarantee.

## Cleanup

When finished, delete **only your practice Library** and its documents:

```bash
python cleanup_library.py
```

The script reads and displays the saved ID, then requires you to type the
entire ID to confirm. A mismatch makes no deletion request. The local ID is
removed only after the delete call succeeds. If the ID file is missing or
was not saved, use the printed ID and Studio to identify and delete the
correct practice resource. Never delete a shared or valuable library.

## Discussion

What did managed Libraries handle, and which details of chunking, embeddings
and ranking were not directly controlled in this exercise? What would change
if you needed custom filtering, hybrid search or ranking?

If service access or ingestion prevents a live run, use the policy files and
worksheet for discussion. They are source facts, not recorded API results.
The next semantic-search exercise can explore retrieval controls in more detail.
