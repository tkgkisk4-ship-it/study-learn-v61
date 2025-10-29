
import os
import pandas as pd
import datetime as dt

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "vocab_seed.csv")

def load_vocab(path: str = DATA_PATH) -> pd.DataFrame:
    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame(columns=["word","ipa","meaning_ja","collocations","example_en","example_ja","image_hint","deck","ease","interval_days","due_date"])
    # Normalize
    if "due_date" in df.columns:
        df["due_date"] = pd.to_datetime(df["due_date"]).dt.date
    else:
        df["due_date"] = pd.to_datetime(dt.date.today()).date()
    for col in ["ease","interval_days"]:
        if col in df.columns:
            df[col] = df[col].fillna(0)
        else:
            df[col] = 0
    if "deck" not in df.columns:
        df["deck"] = "core"
    return df

def save_vocab(df: pd.DataFrame, path: str = DATA_PATH):
    df.to_csv(path, index=False)
    return path
