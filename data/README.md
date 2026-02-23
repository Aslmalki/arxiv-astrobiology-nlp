# Data Structure

This folder is organized for reproducible execution while keeping the public repository lightweight.

## Files and Folders

- `sample_data.csv`: small test subset for quick validation and CI-style checks.
- `raw/`: place full raw ArXiv collection file here when available (`arxiv_astrobiology_raw.csv`).
- `processed/`: place full processed dataset here (`preprocessed_papers.csv`).

## Required Schema

Both `sample_data.csv` and `processed/preprocessed_papers.csv` should include:

- `arxiv_id`
- `title`
- `abstract`
- `authors`
- `published_date`
- `year`
- `primary_category`
- `categories`
- `source_query`
- `nasa_goal`

Optional but recommended:

- `text`
- `text_word_count`

## Reproducibility Notes

- Scripts automatically try `data/processed/preprocessed_papers.csv` first.
- If full data is missing, scripts fall back to `data/sample_data.csv`.
- For full paper reproduction, use the complete processed dataset.
