PYTHON ?= python3

.PHONY: all manuscript legacy bundle collect preprocess clean

# One-command full run:
# - main manuscript pipeline
# - legacy Top2Vec comparison
# - consolidated paper bundle/checklist
all: manuscript legacy bundle

manuscript:
	$(PYTHON) scripts/topic_modeling_bertopic.py
	$(PYTHON) scripts/topic_validation.py
	$(PYTHON) scripts/hierarchical_clustering_topics.py
	$(PYTHON) scripts/temporal_trend_analysis.py
	$(PYTHON) scripts/corpus_structure_analysis.py
	$(PYTHON) scripts/semantic_distance_figure.py
	$(PYTHON) scripts/unclustered_temporal_figure.py
	$(PYTHON) scripts/pipeline_diagram.py

legacy:
	$(PYTHON) scripts/legacy_methods/top2vec_modeling.py
	$(PYTHON) scripts/legacy_methods/top2vec_validation.py
	$(PYTHON) scripts/legacy_methods/generate_table4_method_comparison.py

bundle:
	$(PYTHON) scripts/generate_paper_outputs.py

# Optional data creation steps
collect:
	$(PYTHON) scripts/data_collection_arxiv.py

preprocess:
	$(PYTHON) scripts/data_preprocessing.py

clean:
	rm -rf results figures paper_outputs models models_top2vec results_top2vec
