#!/usr/bin/env python3
"""
Compute topic coherence and generate initial labels.
"""
import json
import sys
from pathlib import Path

import pandas as pd
from bertopic import BERTopic
from gensim.corpora import Dictionary
from gensim.models.coherencemodel import CoherenceModel


ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
from utils.data_utils import load_main_or_sample  # noqa: E402


def main() -> None:
    df = load_main_or_sample()
    model_path = ROOT / "models" / "bertopic_model"
    topics_path = ROOT / "results" / "topics" / "topic_info.csv"
    validation_dir = ROOT / "results" / "validation"
    validation_dir.mkdir(parents=True, exist_ok=True)

    if not model_path.exists():
        raise FileNotFoundError(f"Missing model path: {model_path}")
    if not topics_path.exists():
        raise FileNotFoundError(f"Missing topic info: {topics_path}")

    topic_model = BERTopic.load(model_path)
    topic_info = pd.read_csv(topics_path)

    texts = df["text"].str.split().tolist()
    dictionary = Dictionary(texts)
    topics_words = []

    for topic_id in range(len(topic_info) - 1):
        words = [word for word, _ in topic_model.get_topic(topic_id)]
        topics_words.append(words)

    coherence_model = CoherenceModel(
        topics=topics_words,
        texts=texts,
        dictionary=dictionary,
        coherence="c_v",
        processes=1,
    )
    coherence_score = coherence_model.get_coherence()

    with (validation_dir / "coherence_scores.json").open("w", encoding="utf-8") as f:
        json.dump({"coherence_cv": coherence_score}, f, indent=2)

    labels = []
    for topic_id in range(len(topic_info) - 1):
        top_words = [word for word, _ in topic_model.get_topic(topic_id)[:3]]
        labels.append({"topic_id": topic_id, "label": f"Topic {topic_id}: {', '.join(top_words)}"})
    pd.DataFrame(labels).to_csv(validation_dir / "topic_labels.csv", index=False)

    print(f"Coherence (C_v): {coherence_score:.3f}")
    print(f"Saved validation outputs to {validation_dir}")


if __name__ == "__main__":
    main()
