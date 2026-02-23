# Reproducibility Map

This document maps manuscript figures/tables to scripts and recommended run order.

## Recommended Run Order

1. `python scripts/data_collection_arxiv.py` (optional if using existing raw data)
2. `python scripts/data_preprocessing.py`
3. `python scripts/sensitivity_elbow_analysis.py`
4. `python scripts/topic_modeling_bertopic.py`
5. `python scripts/topic_validation.py`
6. `python scripts/hierarchical_clustering_topics.py`
7. `python scripts/temporal_trend_analysis.py`
8. `python scripts/corpus_structure_analysis.py`
9. `python scripts/semantic_distance_figure.py`
10. `python scripts/unclustered_temporal_figure.py`
11. `python scripts/pipeline_diagram.py`
12. `python scripts/generate_paper_outputs.py`
13. `python scripts/legacy_methods/top2vec_modeling.py` (for Table 4)
14. `python scripts/legacy_methods/top2vec_validation.py` (for Table 4)
15. `python scripts/legacy_methods/generate_table4_method_comparison.py` (for Table 4)

## Figure-to-Script Mapping

- **Figure 1 (Research Pipeline)**: `scripts/pipeline_diagram.py`
- **Figure 2 (Elbow Method for min_cluster_size)**: `scripts/sensitivity_elbow_analysis.py`
- **Figure 3 (Corpus Structure: clustered/unclustered vs relevance)**: `scripts/corpus_structure_analysis.py`
- **Figure 4 (Semantic Distance Distribution)**: `scripts/semantic_distance_figure.py`
- **Figure 5 (Temporal Trend of Unclustered Papers)**: `scripts/unclustered_temporal_figure.py`
- **Figure 6 (Hierarchical Topic Clustering)**: `scripts/hierarchical_clustering_topics.py`
- **Figure 7 (Graphical Abstract Summary)**: assembled from outputs of scripts 4-10 and finalized as publication figure

## Table-to-Script Mapping

- **Table 1 (Search queries from NASA roadmap)**: `scripts/data_collection_arxiv.py`
- **Table 2 (Filtering summary)**: `scripts/data_preprocessing.py`
- **Table 3 (Filtering examples)**: source filtering outputs + manual curation
- **Table 4 (Top2Vec vs BERTopic comparison)**:
  - `scripts/legacy_methods/top2vec_modeling.py`
  - `scripts/legacy_methods/top2vec_validation.py`
  - `scripts/legacy_methods/generate_table4_method_comparison.py`
- **Table 5 (BERTopic parameter configuration)**: `scripts/topic_modeling_bertopic.py`
- **Table 6 (ArXiv validation categories)**: `scripts/corpus_structure_analysis.py` and validation definitions
- **Table 7 (Sensitivity analysis)**: `scripts/sensitivity_elbow_analysis.py`
- **Table 8 (Corpus structure cross-tab)**: `scripts/corpus_structure_analysis.py`
- **Table 9 (Unclustered astrobiology examples)**: validation outputs + manual curation
- **Table 10 (Topic labels and counts)**: `scripts/topic_modeling_bertopic.py`, `scripts/topic_validation.py`
- **Table 11 (Query-noise topics)**: topic validation outputs and post-processing
- **Table 12 (Top keywords per topic)**: `scripts/topic_modeling_bertopic.py`
- **Table 13 (Distance statistics)**: `scripts/semantic_distance_figure.py`
- **Table 14 (Temporal bins and unclustered percentages)**: `scripts/unclustered_temporal_figure.py`

## Full-Data vs Sample-Data Behavior

- Full reproduction requires:
  - `data/raw/arxiv_astrobiology_raw.csv` and/or
  - `data/processed/preprocessed_papers.csv`
- If full processed data is unavailable, scripts fall back to:
  - `data/sample_data.csv`

## Notes for Peer Reviewers

- All paths are project-root-relative.
- No local machine absolute paths are required.
- No private directories are referenced.
