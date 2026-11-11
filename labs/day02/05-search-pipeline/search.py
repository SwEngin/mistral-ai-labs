"""Implement a small search pipeline over fictional technical articles."""

import argparse
import json
import math
import os
import re
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from mistralai.client import Mistral

LAB_DIR = Path(__file__).resolve().parent


class Article(TypedDict):
    id: str
    title: str
    content: str


class SearchResult(TypedDict):
    score: float
    article: Article


def load_articles() -> list[Article]:
    with (LAB_DIR / "data" / "articles.json").open(encoding="utf-8") as file:
        return json.load(file)


def embed_texts(client: Mistral, texts: list[str]) -> list[list[float]]:
    """Return one vector per text, in input order."""
    # TODO 1 (Required): Call client.embeddings.create() with model
    # "mistral-embed" and inputs=texts. Extract the vectors in input order.
    # Check response count, indexes and vector presence; report invalid
    # responses instead of silently mixing documents and vectors.
    raise NotImplementedError("Complete TODO 1: generate embeddings")


def cosine_similarity(left: list[float], right: list[float]) -> float:
    """Compute cosine similarity between two nonzero, equal-length vectors."""
    # TODO 2 (Required): Compute the dot product divided by both norms.
    # Reject empty vectors, different dimensions, and zero norms.
    raise NotImplementedError("Complete TODO 2: cosine similarity")


def semantic_search(
    client: Mistral, articles: list[Article], question: str, top_k: int
) -> list[SearchResult]:
    """Return ranked article passages for a question."""
    # TODO 3 (Required): Embed each article (title + content) and the question,
    # compute cosine scores, then return up to top_k SearchResult objects
    # sorted by descending score. Use article ID as a deterministic tie-breaker.
    raise NotImplementedError("Complete TODO 3: semantic top-k ranking")


def keyword_search(
    articles: list[Article], question: str, top_k: int
) -> list[SearchResult]:
    """Rank articles by the number of distinct query terms they contain."""
    # TODO 4 (Exploration): Tokenize using re.findall(r"\w+", text.lower()),
    # count distinct query words present in each title + content, and rank
    # positive matches by descending count, breaking ties by article ID.
    # Return up to top_k results in the same shape as semantic_search.
    raise NotImplementedError("Complete TODO 4: keyword search")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", help="Question to search for")
    parser.add_argument("--top-k", type=int, default=3, help="Maximum number of results")
    parser.add_argument("--mode", choices=("semantic", "keyword"), default="semantic")
    args = parser.parse_args()
    if not args.question.strip():
        parser.error("Question must not be empty.")
    if args.top_k < 1:
        parser.error("--top-k must be at least 1.")

    articles = load_articles()
    if args.mode == "keyword":
        results = keyword_search(articles, args.question, args.top_k)
    else:
        load_dotenv(LAB_DIR / ".env")
        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            parser.error("Set MISTRAL_API_KEY in the environment or the lab's .env file.")
        results = semantic_search(Mistral(api_key=api_key), articles, args.question, args.top_k)

    if not results:
        print("No matching articles.")
    for result in results:
        article = result["article"]
        print(f"\nScore: {result['score']:.4f} | {article['id']} | {article['title']}")
        print(article["content"])


if __name__ == "__main__":
    main()
