"""
Data Connectors & Normalization Layer
Ingests multi-channel weekly spend, geo holdout experiments, and precomputed Bayesian models.
Enforces defensive prompt-injection sanitization.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

DATA_DIR = Path(__file__).parent
SAMPLE_DATA_DIR = DATA_DIR / "sample_data"

INJECTION_PATTERN = re.compile(
    r"(ignore\s+(all\s+)?(previous\s+)?instructions|override\s+system|system\s+prompt|transfer\s+\$|emergency\s+budget|approve\s+budget|authorize\s+)",
    re.IGNORECASE
)


def sanitize_text(text: str) -> str:
    """Sanitizes text inputs against adversarial injection directives."""
    if not isinstance(text, str):
        return text
    return INJECTION_PATTERN.sub("[SANITIZED_INSTRUCTION_REMOVED]", text).strip()


class MMMDataConnector:
    """Connectors for marketing mix time-series, geo holdouts, and priors."""

    def __init__(self, sample_data_dir: Path = SAMPLE_DATA_DIR):
        self.sample_data_dir = sample_data_dir

    def load_weekly_mmm_data(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """Loads and parses weekly multi-channel ad spend, revenue, and controls."""
        path = Path(file_path) if file_path else self.sample_data_dir / "multi_channel_mmm_weekly.csv"
        df = pd.read_csv(path)
        df["week_start"] = pd.to_datetime(df["week_start"])
        numeric_cols = [
            "google_search_spend", "meta_ads_spend", "retail_media_spend",
            "youtube_video_spend", "email_marketing_spend", "promotional_discount_pct",
            "seasonality_index", "revenue", "conversions"
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
        return df.sort_values("week_start").reset_index(drop=True)

    def load_geo_holdout_data(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """Loads DMA-level geo experiment data for causal inference."""
        path = Path(file_path) if file_path else self.sample_data_dir / "geo_holdout_experiment.csv"
        df = pd.read_csv(path)
        for col in ["pre_test_weekly_revenue", "test_weekly_revenue", "test_weekly_spend", "conversions_pre", "conversions_test"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
        return df

    def load_precomputed_model(self, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Loads precomputed Bayesian MMM posterior parameters for zero-cost demo execution."""
        path = Path(file_path) if file_path else self.sample_data_dir / "precomputed_mmm_results.json"
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


connector = MMMDataConnector()
