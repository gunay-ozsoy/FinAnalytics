import pandas as pd
import numpy as np

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["ticker", "datetime"])

    # 1 day return
    df["ret_1"] = df.groupby("ticker")["close"].pct_change()

    # 63 day volatility
    df["vol_63"] = (
        df.groupby("ticker")["ret_1"]
        .rolling(63)
        .std()
        .reset_index(level=0, drop=True)
    )

    # 63 day momentum
    df["mom_63"] = df.groupby("ticker")["close"].pct_change(63)

    df = df.dropna().reset_index(drop=True)
    return df
