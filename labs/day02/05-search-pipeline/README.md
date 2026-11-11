# Day 02, Lab 05: Build and Evaluate a Search Pipeline

**70 minutes · Hands-on experiments**

## Scenario

Build a search function for short fictional technical articles on Kubernetes,
API authentication, databases and troubleshooting. Embed article passages and
a question using `mistral-embed`, compute cosine similarity, and return the
highest-ranked articles with their scores, IDs and passages. Each short article
is treated as one passage; this lab does not implement chunking or generation.


## Setup

Requires Python 3.10+, internet access and a Mistral API key with access to
`mistral-embed`. Each semantic run sends all articles and the query to the
hosted API and may incur charges. Use only fictional or approved content.

From the repository root on macOS/Linux:

```bash
cd labs/day02/05-search-pipeline
python3 --version  # Must be 3.10 or later
python -m pip install -r ../../../requirements.txt
```

Set `MISTRAL_API_KEY` using the training center's approved method, or place
`MISTRAL_API_KEY=your-key` in a local lab `.env`. Never print or commit it.
Check the environment and SDK without displaying the key:

```bash
python -c "import os; print('Key is set' if os.environ.get('MISTRAL_API_KEY') else 'Key is not set in the environment')"
python -c "from mistralai.client import Mistral; print('Mistral SDK import OK')"
```

The key check does not read `.env`; the semantic-search application does.
Keyword mode runs locally without an API key.

## Required — embeddings and top-k retrieval

Open `data/articles.json` and `search.py`, then complete **TODOs 1–3**:

1. Call `client.embeddings.create(model="mistral-embed", inputs=texts)`.
   Return one vector per text in input order. Check that response counts,
   indexes and vectors are valid; do not silently associate vectors with the
   wrong article. See the [official embeddings quickstart](https://docs.mistral.ai/inference/quickstarts/create-embeddings).
2. Compute cosine similarity: dot product divided by both vector norms.
   Reject empty, mismatched and zero vectors.
3. Embed each article's title and content plus the question. Score every
   article and return the top `k` sorted by descending score, with article ID
   as a deterministic tie-breaker.

The entry point prints each result's score, ID, title and full passage.
Before the TODOs are complete the starter intentionally raises
`NotImplementedError`.

```bash
python search.py "How can I make a slow SQL query faster?" --top-k 3
python search.py "My container keeps restarting, how can I investigate?" --top-k 1
```

**Success:** a semantic query returns at most `top-k` ranked results with
scores and passages. Check whether `DB-INDEX` and `K8S-HEALTH`, respectively,
are relevant results. Rankings may vary; compare them with the source rather
than assuming the top result is always correct.

## Exploration — keyword versus meaning

Complete **TODO 4**: tokenize query and article text, score by the number of
distinct query words shared, omit zero-score articles and sort by score then
ID. Run the same queries with `--mode keyword`:

```bash
python search.py "How can I make a slow SQL query faster?" --mode keyword --top-k 3
python search.py "My container keeps restarting, how can I investigate?" --mode keyword
```

Keyword scores are word counts; semantic scores are cosine similarities.
They are not directly comparable. Which terms overlap? Where do synonyms or
irrelevant common words affect the results?

## Bonus — evaluation and managed search

Use `tests/evaluation.md` to record top-1 and top-3 results and compute
hit rate@3 for the eight in-scope questions. Try the out-of-scope question:
semantic nearest-neighbor search still returns results even when none is
relevant. Discuss thresholds and evaluation rather than assuming a score
guarantees relevance.

The instructor will demonstrate or discuss:

- [Mistral Search Index](https://docs.mistral.ai/studio/search/search-index/quickstarts/create-and-query-an-index):
  hosted indexing, hybrid search and metadata filtering.
- [Mistral Search Toolkit](https://docs.mistral.ai/studio/search/search-toolkit/quickstart):
  configurable ingestion and retrieval components.
- Agentic search as a preview of iterative source exploration; implementation
  is reserved for Day 3.

The toolkit quickstart requires Python 3.12–3.14, a workspace with search
indexes enabled and `create_search_indexes` permission. Search Index is a
public preview; verify current availability and permissions before any live
demo. Hosted indexes are persistent resources and can incur costs: only use
approved fictional data, and delete a practice index after the demonstration.
If the prerequisites are unavailable, discuss the official quickstarts;
the core embeddings exercise remains independent of the toolkit.

## Discussion

Compare relevance, latency and control between the in-memory pipeline, managed
Libraries and Search Index. This exercise requests fresh embeddings on every
semantic run and does not persist vectors; production systems usually avoid
re-embedding unchanged documents. Embeddings support retrieval but do not
themselves guarantee answer quality or source attribution.
