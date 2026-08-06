"""
Tripadvisor API: A Quick Start Example
See more at: https://apify.com/johnvc/tripadvisor-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/tripadvisor-api/input-schema?fpr=9n7kx3

This script shows how to call the Tripadvisor API on Apify from Python and
read its structured JSON output. The default run stays deliberately small so
your first call is inexpensive; the --example recipes mirror the API's main
use cases (see the README Recipes section).

Get your free Apify API key at: https://apify.com?fpr=9n7kx3

Examples:
  uv run python tripadvisor-api-example.py
  uv run python tripadvisor-api-example.py --example export_reviews
"""

from __future__ import annotations

import argparse
import os
from typing import Any

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

ACTOR_ID = "johnvc/tripadvisor-api"


def _print_items(items: list[dict[str, Any]]) -> None:
    """Print a short summary of dataset items."""
    print(f"Returned {len(items)} item(s).\n")
    for item in items:
        print(item.get('title'), item.get('rating'), item.get('reviewCount'), item.get('location'))


def run_default(client: ApifyClient) -> None:
    """Cheap general quick-start. Inputs stay small on purpose."""
    run_input: dict[str, Any] = {
        "search_mode": "search",
        "query": "hotels in paris",
        "max_results": 3,  # small on purpose to keep the first run inexpensive
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_export_reviews(client: ApifyClient) -> None:
    """Export a place's reviews (mirrors the export-tripadvisor-reviews use case).

    The placeId comes from any search-mode row. 143336 is Paris Las Vegas, a
    place with tens of thousands of reviews, so it always returns data.
    """
    run_input: dict[str, Any] = {
        "search_mode": "reviews",
        "place_id": "143336",
        "max_results": 3,  # small on purpose; raise once you know your budget
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_hotel_dataset(client: ApifyClient) -> None:
    """Build a small, fresh hotel dataset for one city (ACCOMMODATION only)."""
    run_input: dict[str, Any] = {
        "search_mode": "search",
        "query": "hotels in rome",
        "place_types": ["ACCOMMODATION"],
        "max_results": 3,  # small on purpose; raise once you know your budget
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def main() -> None:
    """Dispatch a quick-start or use-case recipe."""
    parser = argparse.ArgumentParser(description="Tripadvisor API examples")
    parser.add_argument(
        "--example",
        default="default",
        choices=['default', 'export_reviews', 'hotel_dataset'],
        help="Which recipe to run (see README Recipes).",
    )
    args = parser.parse_args()

    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        raise SystemExit("Set APIFY_API_TOKEN in .env or the environment.")

    client = ApifyClient(token)
    dispatch = {
        "default": run_default,
        "export_reviews": run_export_reviews,
        "hotel_dataset": run_hotel_dataset,
    }
    dispatch[args.example](client)


if __name__ == "__main__":
    main()
