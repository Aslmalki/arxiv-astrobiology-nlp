#!/usr/bin/env python3
"""
Create semantic distance distribution figure (paper Figure 4).
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def calculate_distances(embeddings: np.ndarray, clusters: np.ndarray, topic_ids: list[int]) -> tuple[np.ndarray, np.ndarray]:
    centroids = {}
    for t in topic_ids:
        centroids[t] = embeddings[clusters == t].mean(axis=0)

    clustered = []
    for emb, t in zip(embeddings[clusters != -1], clusters[clusters != -1]):
        clustered.append(1 - cosine_similarity([centroids[t]], [emb])[0, 0])

    centroid_matrix = np.array([centroids[t] for t in topic_ids])
    unclustered = []
    for emb in embeddings[clusters == -1]:
        d = 1 - cosine_similarity([emb], centroid_matrix)[0]
        unclustered.append(np.min(d))
    return np.array(clustered), np.array(unclustered)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    embeddings = np.load(root / "models" / "embeddings.npy")
    doc_topics = pd.read_csv(root / "results" / "topics" / "document_topics.csv")
    clusters = doc_topics["topic"].values
    topic_ids = sorted([t for t in np.unique(clusters) if t != -1])

    clustered, unclustered = calculate_distances(embeddings, clusters, topic_ids)

    fig_dir = root / "figures" / "validation"
    fig_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.hist(clustered, bins=50, alpha=0.6, density=True, label="Clustered")
    plt.hist(unclustered, bins=50, alpha=0.6, density=True, label="Unclustered")
    plt.axvline(clustered.mean(), linestyle="--", linewidth=1.5, label=f"Clustered mean={clustered.mean():.3f}")
    plt.axvline(unclustered.mean(), linestyle="--", linewidth=1.5, label=f"Unclustered mean={unclustered.mean():.3f}")
    plt.xlabel("Cosine distance to nearest cluster centroid")
    plt.ylabel("Density")
    plt.title("Semantic Distance: Clustered vs Unclustered Papers")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(fig_dir / "semantic_distance_distribution.pdf", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved semantic distance figure to {fig_dir}.")


if __name__ == "__main__":
    main()
