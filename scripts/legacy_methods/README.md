# Legacy Methods (Top2Vec Baseline)

This folder contains legacy baseline scripts used for method comparison with BERTopic.

## Scripts

- `top2vec_modeling.py`: trains or loads Top2Vec and saves topic outputs.
- `top2vec_validation.py`: computes C_v coherence for Top2Vec topics.
- `generate_table4_method_comparison.py`: builds manuscript Table 4 from BERTopic and Top2Vec results.

## Run Order

```bash
python scripts/legacy_methods/top2vec_modeling.py
python scripts/legacy_methods/top2vec_validation.py
python scripts/legacy_methods/generate_table4_method_comparison.py
```
