from pathlib import Path


def project_root() -> Path:
    """Return the repository root from any script location."""
    return Path(__file__).resolve().parents[1]


def data_dir() -> Path:
    return project_root() / "data"


def raw_data_path() -> Path:
    return data_dir() / "raw" / "arxiv_astrobiology_raw.csv"


def processed_data_path() -> Path:
    return data_dir() / "processed" / "preprocessed_papers.csv"


def sample_data_path() -> Path:
    return data_dir() / "sample_data.csv"
