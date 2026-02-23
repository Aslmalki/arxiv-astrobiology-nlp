#!/usr/bin/env python3
"""
Legacy baseline: validate Top2Vec topics via C_v coherence.
"""
import json
import sys
from pathlib import Path

import pandas as pd
from gensim.corpora import Dictionary
from gensim.models.coherencemodel import CoherenceModel


ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
from utils.data_utils import load_main_or_sample  # noqa: E402


def main() -> None:
    topic_info_path = ROOT / "results_top2vec" / "topics" / "topic_info.csv"
    if not topic_info_path.exists():
        raise FileNotFoundError("Missing Top2Vec topic info. Run top2vec_modeling.py first.")

    topic_info = pd.read_csv(topic_info_path)
    topics = [kw.split(", ") for kw in topic_info["Keywords"]]

    df = load_main_or_sample()
    texts = [text.split() for text in df["text"].fillna("")]
    dictionary = Dictionary(texts)
    dictionary.filter_extremes(no_below=2, no_above=0.5)

    coherence_model = CoherenceModel(
        topics=topics,
        texts=texts,
        dictionary=dictionary,
        coherence="c_v",
        processes=1,
    )
    coherence_score = coherence_model.get_coherence()

    out_dir = ROOT / "results_top2vec" / "validation"
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "coherence_scores.json").open("w", encoding="utf-8") as f:
        json.dump(
            {
                "coherence_cv": coherence_score,
                "num_topics": len(topics),
                "num_documents": len(texts),
                "dictionary_size": len(dictionary),
            },
            f,
            indent=2,
        )

    print(f"Top2Vec coherence (C_v): {coherence_score:.3f}")
    print(f"Saved validation output to {out_dir}")


if __name__ == "__main__":
    main()
