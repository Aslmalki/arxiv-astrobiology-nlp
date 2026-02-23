#!/usr/bin/env python3
"""
Generate pipeline diagram for manuscript Figure 1.
"""
from pathlib import Path

import matplotlib.pyplot as plt


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    fig_dir = root / "figures" / "paper"
    fig_dir.mkdir(parents=True, exist_ok=True)

    steps = [
        "1. Data Collection\n(18 NASA queries via ArXiv API)",
        "2. Preprocessing\n(deduplicate, filter, quality checks)",
        "3. Embeddings\n(SBERT all-mpnet-base-v2)",
        "4. UMAP Reduction\n(5D for clustering)",
        "5. HDBSCAN Clustering\n(min_cluster_size=60)",
        "6. Topic Representation\n(c-TF-IDF keywords)",
        "7. Validation and Interpretation\n(ArXiv categories + coherence)",
    ]

    plt.figure(figsize=(10, 10))
    for i, step in enumerate(steps):
        y = len(steps) - i
        plt.text(
            0.5,
            y,
            step,
            ha="center",
            va="center",
            bbox={"boxstyle": "round,pad=0.5", "facecolor": "#eef2ff", "edgecolor": "#4f46e5"},
            fontsize=10,
        )
        if i < len(steps) - 1:
            plt.annotate("", xy=(0.5, y - 0.6), xytext=(0.5, y - 0.15), arrowprops={"arrowstyle": "->", "lw": 1.5})

    plt.xlim(0, 1)
    plt.ylim(0.5, len(steps) + 0.8)
    plt.axis("off")
    plt.title("Astrobiology ArXiv Topic Modeling Pipeline")
    plt.tight_layout()
    plt.savefig(fig_dir / "pipeline_diagram.pdf", dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved pipeline diagram to {fig_dir}.")


if __name__ == "__main__":
    main()
