#!/usr/bin/env python3
"""
Legacy baseline: run Top2Vec for method comparison (Table 4).
"""
import sys
from pathlib import Path
import os

import pandas as pd
from top2vec import Top2Vec

try:
    import torch
except Exception:  # pragma: no cover
    torch = None


ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
from utils.data_utils import load_main_or_sample  # noqa: E402


def main() -> None:
    df = load_main_or_sample()
    texts = df["text"].fillna("").tolist()

    models_dir = ROOT / "models_top2vec"
    results_dir = ROOT / "results_top2vec" / "topics"
    models_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    model_path = models_dir / "top2vec_model"
    use_gpu = bool(torch and torch.cuda.is_available())
    workers = max(1, (os.cpu_count() or 4) - 1)

    if model_path.exists():
        model = Top2Vec.load(str(model_path))
    else:
        model = Top2Vec(
            documents=texts,
            speed="learn",
            embedding_model="distiluse-base-multilingual-cased",
            workers=workers,
            gpu_umap=use_gpu,
            gpu_hdbscan=use_gpu,
        )
        model.save(str(model_path))

    num_topics = model.get_num_topics()
    topic_sizes, topic_nums = model.get_topic_sizes()
    topic_words, _, _ = model.get_topics(num_topics)

    topic_info = pd.DataFrame(
        {
            "Topic": topic_nums,
            "Size": topic_sizes,
            "Keywords": [", ".join(words[:10]) for words in topic_words],
        }
    )
    topic_info.to_csv(results_dir / "topic_info.csv", index=False)

    doc_topics = pd.DataFrame(
        {
            "arxiv_id": df["arxiv_id"],
            "topic": model.doc_top,
            "year": df["year"],
        }
    )
    doc_topics.to_csv(results_dir / "document_topics.csv", index=False)

    print(f"Top2Vec topics: {num_topics}")
    print(f"Saved outputs to {results_dir}")


if __name__ == "__main__":
    main()
