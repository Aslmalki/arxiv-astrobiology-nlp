#!/usr/bin/env python3
"""
Compute clustered/unclustered and astrobiology-relevance corpus structure.
"""
from pathlib import Path

import pandas as pd


def has_astro_category(categories_str: str) -> bool:
    categories = str(categories_str).split()
    return any(c.startswith("astro-ph") or c == "physics.space-ph" for c in categories)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    doc_topics = pd.read_csv(root / "results" / "topics" / "document_topics.csv")
    papers_path = root / "data" / "processed" / "preprocessed_papers.csv"
    if not papers_path.exists():
        papers_path = root / "data" / "sample_data.csv"
    papers = pd.read_csv(papers_path)

    df = papers.merge(doc_topics[["arxiv_id", "topic"]], on="arxiv_id", how="inner")
    df["is_clustered"] = df["topic"] != -1
    df["is_astro_related"] = df["categories"].apply(has_astro_category)

    total = len(df)
    summary = pd.DataFrame(
        {
            "Category": [
                "Clustered + Astrobiology-Related",
                "Clustered + Off-Topic",
                "Unclustered + Astrobiology-Related",
                "Unclustered + Off-Topic",
                "TOTAL",
            ],
            "Count": [
                ((df["is_clustered"]) & (df["is_astro_related"])).sum(),
                ((df["is_clustered"]) & (~df["is_astro_related"])).sum(),
                ((~df["is_clustered"]) & (df["is_astro_related"])).sum(),
                ((~df["is_clustered"]) & (~df["is_astro_related"])).sum(),
                total,
            ],
        }
    )
    summary["Percentage of Total"] = (summary["Count"] / total * 100).round(1).astype(str) + "%"

    out_dir = root / "results" / "validation"
    out_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out_dir / "corpus_structure_numbers.csv", index=False)
    print(f"Saved corpus structure summary to {out_dir}.")


if __name__ == "__main__":
    main()
