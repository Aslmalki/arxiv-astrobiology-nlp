#!/usr/bin/env python3
"""
Create yearly proportion figure for unclustered papers (paper Figure 5).
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    doc_topics = pd.read_csv(root / "results" / "topics" / "document_topics.csv")
    doc_topics = doc_topics[(doc_topics["year"] >= 1996) & (doc_topics["year"] <= 2025)].copy()

    rows = []
    for year in range(1996, 2026):
        subset = doc_topics[doc_topics["year"] == year]
        total = len(subset)
        unclustered = (subset["topic"] == -1).sum()
        rows.append(
            {"year": year, "total": total, "unclustered": unclustered, "proportion": (unclustered / total * 100) if total else 0}
        )
    yearly = pd.DataFrame(rows)

    fig_dir = root / "figures" / "temporal"
    fig_dir.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 6))
    plt.plot(yearly["year"], yearly["proportion"], marker="o", linewidth=1.8)
    plt.axhline(41.7, linestyle="--", linewidth=1, color="gray", label="Overall mean (41.7%)")
    plt.xlabel("Year")
    plt.ylabel("Unclustered papers (%)")
    plt.title("Temporal Trend of Unclustered Papers (1996-2025)")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_dir / "unclustered_temporal_trend.pdf", dpi=300, bbox_inches="tight")
    plt.close()

    out = root / "results" / "temporal"
    out.mkdir(parents=True, exist_ok=True)
    yearly.to_csv(out / "unclustered_temporal_trend.csv", index=False)
    print(f"Saved temporal figure and data to {fig_dir} and {out}.")


if __name__ == "__main__":
    main()
