#!/usr/bin/env python3
"""
Create hierarchical clustering dendrogram for discovered topics.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from scipy.spatial.distance import squareform
from sklearn.metrics.pairwise import cosine_similarity


ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))


def main() -> None:
    emb_path = ROOT / "models" / "embeddings.npy"
    doc_topics_path = ROOT / "results" / "topics" / "document_topics.csv"
    labels_path = ROOT / "results" / "topics" / "topic_labels_updated.csv"
    if not labels_path.exists():
        labels_path = ROOT / "results" / "validation" / "topic_labels.csv"

    embeddings = np.load(emb_path)
    doc_topics = pd.read_csv(doc_topics_path)
    labels_df = pd.read_csv(labels_path)

    topic_embeddings = {}
    for topic_id in sorted(doc_topics["topic"].unique()):
        if topic_id == -1:
            continue
        mask = doc_topics["topic"] == topic_id
        topic_embeddings[topic_id] = embeddings[mask].mean(axis=0)

    topic_ids = sorted(topic_embeddings.keys())
    topic_matrix = np.array([topic_embeddings[t] for t in topic_ids])

    sim = cosine_similarity(topic_matrix)
    dist = 1 - sim
    np.fill_diagonal(dist, 0)
    linkage_matrix = linkage(squareform(dist), method="ward")

    fig_dir = ROOT / "figures" / "hierarchy"
    fig_dir.mkdir(parents=True, exist_ok=True)
    label_map = dict(zip(labels_df["topic_id"], labels_df["label"]))
    labels = [label_map.get(t, f"Topic {t}") for t in topic_ids]

    plt.figure(figsize=(15, 8))
    dendrogram(linkage_matrix, labels=labels, leaf_rotation=90, leaf_font_size=8)
    plt.xlabel("Topics")
    plt.ylabel("Distance")
    plt.title("Hierarchical Clustering of Topics")
    plt.tight_layout()
    plt.savefig(fig_dir / "hierarchical_dendrogram.pdf", dpi=300, bbox_inches="tight")
    plt.close()

    clusters = fcluster(linkage_matrix, t=linkage_matrix[:, 2].max() * 0.5, criterion="distance")
    out = pd.DataFrame({"topic_id": topic_ids, "cluster": clusters})
    out_dir = ROOT / "results" / "hierarchy"
    out_dir.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_dir / "topic_clusters.csv", index=False)
    print(f"Saved dendrogram and {out['cluster'].nunique()} clusters.")


if __name__ == "__main__":
    main()
