from pathlib import Path
import pandas as pd

from utils.path_utils import processed_data_path, sample_data_path


REQUIRED_COLUMNS = [
    "arxiv_id",
    "title",
    "abstract",
    "authors",
    "published_date",
    "year",
    "primary_category",
    "categories",
    "source_query",
    "nasa_goal",
]


def load_main_or_sample() -> pd.DataFrame:
    """
    Load full processed dataset when available; otherwise use sample data.
    """
    primary = processed_data_path()
    fallback = sample_data_path()

    if primary.exists():
        df = pd.read_csv(primary)
    elif fallback.exists():
        df = pd.read_csv(fallback)
    else:
        raise FileNotFoundError(
            "Missing both processed dataset and sample_data.csv. "
            "Place full data in data/processed/ or keep data/sample_data.csv."
        )

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    if "text" not in df.columns:
        df["text"] = df["title"].fillna("") + " " + df["abstract"].fillna("")
    if "text_word_count" not in df.columns:
        df["text_word_count"] = df["text"].str.split().str.len()

    return df


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
