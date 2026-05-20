"""Simple training wrapper for predictive models used in demos.

This is intentionally minimal: if a CSV `data/metrics.csv` with columns
`timestamp` and `value` exists, train a Prophet model and save it to `backend/models`.
"""
import os
import logging
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("train_wrapper")
logging.basicConfig(level=logging.INFO)

try:
    import pandas as pd
    from prophet import Prophet
except Exception as e:
    logger.warning("Predictive dependencies not installed: %s", e)

import pickle


def train_simple_prophet(data_path: Path, model_out: Path):
    if not data_path.exists():
        logger.error("Data file not found: %s", data_path)
        return False

    df = pd.read_csv(data_path)
    # Expect columns: timestamp (ISO) and value
    df = df.rename(columns={"timestamp": "ds", "value": "y"})
    df["ds"] = pd.to_datetime(df["ds"])

    m = Prophet()
    m.fit(df)

    model_out.parent.mkdir(parents=True, exist_ok=True)
    with open(model_out, "wb") as fh:
        pickle.dump(m, fh)

    logger.info("Saved predictive model to %s", model_out)
    return True


def main():
    base = Path.cwd()
    data_file = base / "data" / "metrics.csv"
    model_file = base / "backend" / "models" / "prophet_model.pkl"
    train_simple_prophet(data_file, model_file)


if __name__ == "__main__":
    main()
