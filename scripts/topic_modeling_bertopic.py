#!/usr/bin/env python3
"""
Run BERTopic with min_cluster_size = 60 and save model outputs.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from bertopic import BERTopic
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer


ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.data_utils import load_main_or_sample  # noqa: E402


def main() -> None:
    df = load_main_or_sample()
    texts = df["text"].tolist()

    models_dir = ROOT / "models"
    results_dir = ROOT / "results" / "topics"
    figures_dir = ROOT / "figures" / "topics"
    for p in [models_dir, results_dir, figures_dir]:
        p.mkdir(parents=True, exist_ok=True)

    emb_path = models_dir / "embeddings.npy"
    embedding_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    if emb_path.exists():
        embeddings = np.load(emb_path)
    else:
        embeddings = embedding_model.encode(
            texts,
            show_progress_bar=True,
            batch_size=32,
            convert_to_numpy=True,
        )
        np.save(emb_path, embeddings)

    hdbscan_model = HDBSCAN(
        min_cluster_size=60,
        min_samples=None,
        metric="euclidean",
        cluster_selection_method="eom",
        prediction_data=True,
    )

    topic_model = BERTopic(
        embedding_model=embedding_model,
        hdbscan_model=hdbscan_model,
        min_topic_size=60,
        nr_topics="auto",
        calculate_probabilities=False,
        verbose=True,
    )

    topics, _ = topic_model.fit_transform(texts, embeddings)

    topic_model.save(models_dir / "bertopic_model")
    topic_info = topic_model.get_topic_info()
    topic_info.to_csv(results_dir / "topic_info.csv", index=False)

    doc_topics = pd.DataFrame(
        {"arxiv_id": df["arxiv_id"], "topic": topics, "year": df["year"]}
    )
    doc_topics.to_csv(results_dir / "document_topics.csv", index=False)

    outliers = df[doc_topics["topic"] == -1].copy()
    outliers.to_csv(results_dir / "outlier_papers_for_review.csv", index=False)

    fig = topic_model.visualize_barchart(top_n_topics=min(15, len(set(topics)) - 1), height=500)
    fig.write_html(figures_dir / "topic_sizes.html")
    try:
        fig.write_image(figures_dir / "topic_sizes.pdf")
    except Exception:
        pass

    num_topics = len(set(topics)) - 1
    outlier_pct = (doc_topics["topic"] == -1).mean() * 100
    print(f"Topic modeling complete: {num_topics} topics")
    print(f"Outlier rate: {outlier_pct:.1f}%")


if __name__ == "__main__":
    main()
