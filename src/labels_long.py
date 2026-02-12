import pandas as pd
import numpy as np


def add_long_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["ticker", "datetime"])

    df["price_t22"] = df.groupby("ticker")["close"].shift(-22)
    df["price_t63"] = df.groupby("ticker")["close"].shift(-63)

    df["ret_long"] = (df["price_t63"] / df["price_t22"]) - 1
    df["ret_long_norm"] = df["ret_long"] / df["vol_63"]

    df = df.dropna(subset=["ret_long_norm"]).reset_index(drop=True)

    return df
