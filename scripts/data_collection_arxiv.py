#!/usr/bin/env python3
"""
Collect astrobiology-related metadata from the ArXiv API.
"""
import json
import time
from pathlib import Path

import arxiv
import pandas as pd


QUERIES = {
    "astrobiology": {"goal": "All", "rationale": "Core astrobiology term"},
    "biosignature": {"goal": "Goal 7", "rationale": "Life signatures"},
    "atmospheric biosignature": {"goal": "Goal 7", "rationale": "Exoplanet biosignatures"},
    "life detection": {"goal": "Goals 2, 7", "rationale": "Detection methods"},
    "technosignature": {"goal": "Goal 7", "rationale": "Technological signatures"},
    "SETI": {"goal": "Goal 7", "rationale": "Technosignature search"},
    "exoplanet habitability": {"goal": "Goal 1", "rationale": "Habitability"},
    "ocean worlds": {"goal": "Goals 1, 2", "rationale": "Solar system habitats"},
    "habitable zone": {"goal": "Goal 1", "rationale": "Planetary habitability"},
    "prebiotic chemistry": {"goal": "Goals 2, 3", "rationale": "Pre-life chemistry"},
    "origin of life": {"goal": "Goals 3, 4", "rationale": "Life origins"},
    "panspermia": {"goal": "Goal 3", "rationale": "Life transfer hypotheses"},
    "extremophile": {"goal": "Goals 4, 5, 6", "rationale": "Life limits"},
    "hyperthermophile": {"goal": "Goal 5", "rationale": "Heat adaptation"},
    "psychrophile": {"goal": "Goal 5", "rationale": "Cold adaptation"},
    "halophile": {"goal": "Goal 5", "rationale": "Salt adaptation"},
    "acidophile": {"goal": "Goal 5", "rationale": "Acid adaptation"},
    "extraterrestrial life": {"goal": "Goals 2, 7", "rationale": "Life beyond Earth"},
}


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    raw_dir = root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    all_papers = []
    seen_ids = set()
    query_stats = {}

    for query_text, query_info in QUERIES.items():
        search = arxiv.Search(
            query=query_text,
            max_results=10000,
            sort_by=arxiv.SortCriterion.SubmittedDate,
        )

        total_found = 0
        new_found = 0

        for result in search.results():
            total_found += 1
            arxiv_id = result.entry_id.split("/")[-1]
            if arxiv_id in seen_ids:
                continue

            all_papers.append(
                {
                    "arxiv_id": arxiv_id,
                    "title": result.title,
                    "abstract": result.summary,
                    "authors": ", ".join([a.name for a in result.authors]),
                    "published_date": result.published.strftime("%Y-%m-%d"),
                    "year": result.published.year,
                    "primary_category": result.primary_category,
                    "categories": " ".join(result.categories),
                    "source_query": query_text,
                    "nasa_goal": query_info["goal"],
                }
            )
            seen_ids.add(arxiv_id)
            new_found += 1

        query_stats[query_text] = {
            "total_found": total_found,
            "new_papers": new_found,
            "goal": query_info["goal"],
        }
        time.sleep(3)

    df = pd.DataFrame(all_papers)
    df.to_csv(raw_dir / "arxiv_astrobiology_raw.csv", index=False)

    with (raw_dir / "query_statistics.json").open("w", encoding="utf-8") as f:
        json.dump(query_stats, f, indent=2)

    query_mapping = []
    for query, info in QUERIES.items():
        query_mapping.append(
            {
                "query": query,
                "nasa_goal": info["goal"],
                "rationale": info["rationale"],
                "papers_found": query_stats.get(query, {}).get("total_found", 0),
                "new_papers": query_stats.get(query, {}).get("new_papers", 0),
            }
        )
    pd.DataFrame(query_mapping).to_csv(raw_dir / "query_mapping.csv", index=False)

    print(f"Collected {len(df):,} unique papers.")
    print(f"Saved raw data to {raw_dir}.")


if __name__ == "__main__":
    main()
