#!/usr/bin/env python3
"""
Analyze sensitivity results and identify elbow point for min_cluster_size.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    candidates = [
        root / "results" / "validation" / "sensitivity_analysis_min_cluster_size.csv",
        root / "Sensitive Analysis" / "results" / "sensitivity_analysis_systematic.csv",
        root / "Sensitive Analysis" / "results" / "sensitivity_analysis_min_cluster_size.csv",
    ]
    source = None
    for path in candidates:
        if path.exists():
            source = path
            break
    if source is None:
        raise FileNotFoundError("No sensitivity analysis CSV found.")

    df = pd.read_csv(source).sort_values("min_cluster_size")
    df = df[df["num_topics"] > 1].copy()
    df["topics_diff"] = df["num_topics"].diff()
    df["topics_diff2_abs"] = df["topics_diff"].diff().abs()
    elbow_row = df.loc[df["topics_diff2_abs"].idxmax()]

    fig_dir = root / "figures" / "validation"
    fig_dir.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 6))
    plt.plot(df["min_cluster_size"], df["num_topics"], marker="o")
    plt.axvline(elbow_row["min_cluster_size"], linestyle="--", color="red", label=f"Elbow: {int(elbow_row['min_cluster_size'])}")
    plt.xlabel("Minimum Cluster Size")
    plt.ylabel("Number of Topics")
    plt.title("Elbow Method for min_cluster_size")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_dir / "elbow_min_cluster_size.pdf", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Recommended min_cluster_size: {int(elbow_row['min_cluster_size'])}")
    print(f"Saved elbow figure to {fig_dir}.")


if __name__ == "__main__":
    main()
