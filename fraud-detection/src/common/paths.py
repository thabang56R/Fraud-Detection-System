from pathlib import Path


def _find_project_root() -> Path:
    """
    Find the real project root by looking upward for files/folders
    that should exist in the repository.
    Falls back to the current working directory if needed.
    """
    candidates = [Path.cwd(), *Path(__file__).resolve().parents]

    for candidate in candidates:
        if (
            (candidate / "pyproject.toml").exists()
            and (candidate / "configs").exists()
            and (candidate / "src").exists()
        ):
            return candidate

    # fallback
    return Path.cwd()


ROOT_DIR = _find_project_root()

APPS_DIR = ROOT_DIR / "apps"
CONFIGS_DIR = ROOT_DIR / "configs"
DATA_DIR = ROOT_DIR / "data"
DOCS_DIR = ROOT_DIR / "docs"
FEATURES_DIR = ROOT_DIR / "features"
MODELS_DIR = ROOT_DIR / "models"
NOTEBOOKS_DIR = ROOT_DIR / "notebooks"
PIPELINES_DIR = ROOT_DIR / "pipelines"
SRC_DIR = ROOT_DIR / "src"
TESTS_DIR = ROOT_DIR / "tests"

RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLES_DATA_DIR = DATA_DIR / "samples"

MODEL_ARTIFACTS_DIR = MODELS_DIR / "artifacts"
LOGS_DIR = ROOT_DIR / "logs"
REPORTS_DIR = ROOT_DIR / "reports"
MLRUNS_DIR = ROOT_DIR / "mlruns"

for directory in [
    RAW_DATA_DIR,
    INTERIM_DATA_DIR,
    PROCESSED_DATA_DIR,
    SAMPLES_DATA_DIR,
    MODEL_ARTIFACTS_DIR,
    LOGS_DIR,
    REPORTS_DIR,
    MLRUNS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)