# Nearly Three Decades of Astrobiology on ArXiv: A Large-Scale Topic Modeling

**Authors:** Abdullah Almalki, Anamaria Berea

## Repository Description

This repository provides a reproducible computational pipeline for large-scale topic modeling of astrobiology-related ArXiv preprints (1996-2025).  
The workflow covers data collection, preprocessing, BERTopic modeling, validation, temporal analysis, and generation of paper-ready outputs.

## Project Structure

- `scripts/`: cleaned and publication-ready analysis scripts
- `scripts/legacy_methods/`: Top2Vec legacy baseline scripts for method comparison
- `utils/`: helper modules for path handling and data loading
- `data/`: sample data and schema documentation
- `results/`: intermediate and final analysis outputs (generated)
- `figures/`: manuscript figures (generated)
- `paper_outputs/`: consolidated paper tables/statistics (generated)

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## One-Command Execution

From the project root, run the full workflow (manuscript + legacy comparison + final bundle):

```bash
make all
```

Useful partial targets:

```bash
make manuscript
make legacy
make bundle
```

## Quick Reproducibility Run (Sample Data)

From the project root:

```bash
python scripts/topic_modeling_bertopic.py
python scripts/topic_validation.py
python scripts/hierarchical_clustering_topics.py
python scripts/temporal_trend_analysis.py
python scripts/corpus_structure_analysis.py
python scripts/semantic_distance_figure.py
python scripts/unclustered_temporal_figure.py
python scripts/pipeline_diagram.py
python scripts/generate_paper_outputs.py
```

## Legacy Method Comparison (Table 4)

To reproduce Top2Vec vs BERTopic comparison table:

```bash
python scripts/legacy_methods/top2vec_modeling.py
python scripts/legacy_methods/top2vec_validation.py
python scripts/legacy_methods/generate_table4_method_comparison.py
```

Generated files:

- `paper_outputs/tables/table4_method_comparison.csv`
- `paper_outputs/tables/table4_method_comparison.md`

## Full Reproduction Run (Complete Dataset)

1. Put full processed dataset in `data/processed/preprocessed_papers.csv`.
2. Run the same script sequence shown above.
3. See `REPRODUCIBILITY.md` for figure/table-to-script mapping and run order.

## Data Availability

Full dataset and archived outputs will be released at:  
10.5281/zenodo.18750923

## Citation

If you use this repository, please cite:

```bibtex
@article{almalki2026astrobiologyarxiv,
  title={Nearly Three Decades of Astrobiology on ArXiv: A Large-Scale Topic Modeling},
  author={Almalki, Abdullah and Berea, Anamaria},
  journal={Astrobiology},
  year={2026},
  note={In press / accepted manuscript}
}
```
