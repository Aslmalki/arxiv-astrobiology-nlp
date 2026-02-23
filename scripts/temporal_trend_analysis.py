#!/usr/bin/env python3
"""
Analyze topic prevalence over time and estimate trend significance.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    doc_topics = pd.read_csv(root / "results" / "topics" / "document_topics.csv")
    labels_path = root / "results" / "topics" / "topic_labels_updated.csv"
    if not labels_path.exists():
        labels_path = root / "results" / "validation" / "topic_labels.csv"
    labels_df = pd.read_csv(labels_path)

    temporal_dir = root / "results" / "temporal"
    fig_dir = root / "figures" / "temporal"
    temporal_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    yearly_rows = []
    for year in sorted(doc_topics["year"].unique()):
        year_df = doc_topics[doc_topics["year"] == year]
        total = len(year_df)
        for topic_id in sorted(doc_topics["topic"].unique()):
            if topic_id == -1:
                continue
            topic_count = (year_df["topic"] == topic_id).sum()
            yearly_rows.append(
                {
                    "year": year,
                    "topic_id": topic_id,
                    "raw_count": topic_count,
                    "proportion": topic_count / total if total else 0,
                }
            )
    prevalence = pd.DataFrame(yearly_rows)
    prevalence.to_csv(temporal_dir / "topic_prevalence_over_time.csv", index=False)

    trends = []
    for topic_id in sorted(prevalence["topic_id"].unique()):
        td = prevalence[prevalence["topic_id"] == topic_id]
        if len(td) < 5:
            continue
        slope, intercept, r_val, p_val, std_err = stats.linregress(td["year"], td["proportion"])
        label_match = labels_df[labels_df["topic_id"] == topic_id]["label"]
        label = label_match.iloc[0] if len(label_match) else f"Topic {topic_id}"
        trends.append(
            {"topic_id": topic_id, "label": label, "slope": slope, "p_value": p_val, "significant": p_val < 0.05}
        )

    trends_df = pd.DataFrame(trends)
    trends_df.to_csv(temporal_dir / "all_trends.csv", index=False)
    trends_df[trends_df["significant"]].to_csv(temporal_dir / "significant_trends.csv", index=False)

    top10 = trends_df.nlargest(10, "slope")
    plt.figure(figsize=(14, 8))
    for _, row in top10.iterrows():
        td = prevalence[prevalence["topic_id"] == row["topic_id"]]
        plt.plot(td["year"], td["proportion"], marker="o", label=row["label"])
    plt.xlabel("Year")
    plt.ylabel("Proportion")
    plt.title("Topic Evolution Over Time (Top 10 Growing Topics)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(fig_dir / "topic_evolution_top10.pdf", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved temporal trends for {len(trends_df)} topics.")


if __name__ == "__main__":
    main()
