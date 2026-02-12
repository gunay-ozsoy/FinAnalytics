import pandas as pd
import numpy as np


def add_long_label(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["ticker", "datetime"])

    # Future prices
    df["price_t22"] = df.groupby("ticker")["close"].shift(-22)
    df["price_t63"] = df.groupby("ticker")["close"].shift(-63)

    # Forward return (22 -> 63)
    df["ret_long"] = (df["price_t63"] / df["price_t22"]) - 1

    # Normalize with past volatility
    df["ret_long_norm"] = df["ret_long"] / df["vol_63"]

    # Threshold using quantiles
    upper = df["ret_long_norm"].quantile(0.70)
    lower = df["ret_long_norm"].quantile(0.30)

    conditions = [
        df["ret_long_norm"] > upper,
        df["ret_long_norm"] < lower
    ]

    choices = ["Up", "Down"]

    df["long_label"] = np.select(conditions, choices, default="Neutral")

    # Drop rows where future not available
    df = df.dropna(subset=["ret_long_norm"]).reset_index(drop=True)

    return df
