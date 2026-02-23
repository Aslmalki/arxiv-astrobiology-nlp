#!/usr/bin/env python3
"""
Preprocess raw ArXiv metadata and apply multi-category filtering.
"""
import json
from pathlib import Path

import pandas as pd


CS_CATEGORIES = ["cs.LG", "cs.CV", "cs.RO", "stat.ML", "cs.CL", "cs.AI", "cs.NE", "cs.IR"]
ASTRO_CATEGORIES = ["astro-ph", "physics.bio-ph", "q-bio", "physics.geo-ph", "physics.space-ph"]


def has_cs_primary(categories_str: str) -> bool:
    categories = str(categories_str).split()
    primary = categories[0] if categories else ""
    return any(tag in primary for tag in CS_CATEGORIES)


def has_astro_secondary(categories_str: str) -> bool:
    categories = str(categories_str).split()
    return any(any(astro in c for astro in ASTRO_CATEGORIES) for c in categories)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    raw_path = root / "data" / "raw" / "arxiv_astrobiology_raw.csv"
    processed_dir = root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    if not raw_path.exists():
        raise FileNotFoundError(f"Missing input file: {raw_path}")

    df = pd.read_csv(raw_path)
    log = []

    def add_log(step: str, before: int, after: int, description: str) -> None:
        removed = before - after
        log.append(
            {
                "step": step,
                "before": before,
                "after": after,
                "removed": removed,
                "removal_rate": f"{(removed / before * 100) if before else 0:.1f}%",
                "description": description,
            }
        )

    before = len(df)
    df = df.dropna(subset=["title", "abstract"])
    add_log("1", before, len(df), "Remove missing title/abstract")

    before = len(df)
    df = df.drop_duplicates(subset=["arxiv_id"])
    add_log("2", before, len(df), "Remove duplicate ArXiv IDs")

    df["is_cs_primary"] = df["categories"].apply(has_cs_primary)
    df["has_astro_secondary"] = df["categories"].apply(has_astro_secondary)
    before = len(df)
    df = df[~(df["is_cs_primary"] & ~df["has_astro_secondary"])]
    add_log("3", before, len(df), "Filter pure CS/ML papers without astro relevance")

    before = len(df)
    df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce")
    df = df.dropna(subset=["published_date"])
    df["year"] = df["published_date"].dt.year.astype(int)
    add_log("4", before, len(df), "Remove invalid dates")

    df["text"] = df["title"].fillna("") + " " + df["abstract"].fillna("")
    df["text_word_count"] = df["text"].str.split().str.len()
    before = len(df)
    df = df[df["text_word_count"] >= 20]
    add_log("5", before, len(df), "Remove very short documents")

    df = df.drop(columns=["is_cs_primary", "has_astro_secondary"])
    df.to_csv(processed_dir / "preprocessed_papers.csv", index=False)
    pd.DataFrame(log).to_csv(processed_dir / "filtering_log.csv", index=False)

    stats = {
        "total_papers": int(len(df)),
        "date_range": f"{df['year'].min()}-{df['year'].max()}",
        "years_covered": int(df["year"].max() - df["year"].min() + 1),
        "unique_categories": int(df["primary_category"].nunique()),
        "avg_text_length": float(df["text_word_count"].mean()),
    }
    with (processed_dir / "preprocessing_statistics.json").open("w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    print(f"Preprocessing complete: {len(df):,} papers")
    print(f"Saved outputs in {processed_dir}")


if __name__ == "__main__":
    main()
