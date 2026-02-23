#!/usr/bin/env python3
"""
Generate Table 4: Top2Vec vs BERTopic comparison.
"""
import json
from pathlib import Path

import pandas as pd


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    root = Path(__file__).resolve().parents[2]

    bertopic_topic_info = pd.read_csv(root / "results" / "topics" / "topic_info.csv")
    bertopic_doc_topics = pd.read_csv(root / "results" / "topics" / "document_topics.csv")
    bertopic_coherence_path = root / "results" / "validation" / "coherence_scores.json"

    top2vec_topic_info = pd.read_csv(root / "results_top2vec" / "topics" / "topic_info.csv")
    top2vec_doc_topics = pd.read_csv(root / "results_top2vec" / "topics" / "document_topics.csv")
    top2vec_coherence_path = root / "results_top2vec" / "validation" / "coherence_scores.json"

    bertopic_num_topics = int((bertopic_topic_info["Topic"] != -1).sum())
    bertopic_unclustered_pct = float((bertopic_doc_topics["topic"] == -1).mean() * 100)
    bertopic_coherence = load_json(bertopic_coherence_path).get("coherence_cv")

    top2vec_num_topics = int(len(top2vec_topic_info))
    top2vec_unclustered_pct = float((top2vec_doc_topics["topic"] == -1).mean() * 100)
    top2vec_coherence = load_json(top2vec_coherence_path).get("coherence_cv")

    comparison = pd.DataFrame(
        [
            {
                "Method": "Top2Vec",
                "Topics": top2vec_num_topics,
                "Unclustered": f"{top2vec_unclustered_pct:.1f}%",
                "Coherence_Cv": round(float(top2vec_coherence), 3) if top2vec_coherence is not None else None,
                "Interpretability": "High granularity" if top2vec_num_topics >= 100 else "Moderate granularity",
            },
            {
                "Method": "BERTopic",
                "Topics": bertopic_num_topics,
                "Unclustered": f"{bertopic_unclustered_pct:.1f}%",
                "Coherence_Cv": round(float(bertopic_coherence), 3) if bertopic_coherence is not None else None,
                "Interpretability": "Moderate granularity" if bertopic_num_topics <= 50 else "High granularity",
            },
        ]
    )

    out_dir = root / "paper_outputs" / "tables"
    out_dir.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(out_dir / "table4_method_comparison.csv", index=False)

    md = [
        "| Method | Topics | Unclustered | Coh. (Cv) | Interpretability |",
        "|---|---:|---:|---:|---|",
    ]
    for _, row in comparison.iterrows():
        md.append(
            f"| {row['Method']} | {row['Topics']} | {row['Unclustered']} | "
            f"{row['Coherence_Cv']} | {row['Interpretability']} |"
        )
    (out_dir / "table4_method_comparison.md").write_text("\n".join(md), encoding="utf-8")

    print(f"Saved Table 4 outputs to {out_dir}")


if __name__ == "__main__":
    main()
