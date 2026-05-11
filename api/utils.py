import pandas as pd

def clean_columns(df):
    df.columns = df.columns.str.lower().str.strip()
    return df


def detect_columns(df):
    df = clean_columns(df)

    mapping = {}

    # flexible matching (NO hardcoding errors anymore)
    for col in df.columns:
        if "pm" in col and "2" in col:
            mapping["pm25"] = col
        elif "pm10" in col:
            mapping["pm10"] = col
        elif "no2" in col:
            mapping["no2"] = col
        elif "co" in col:
            mapping["co"] = col

    required = ["pm25", "pm10", "no2", "co"]

    missing = [r for r in required if r not in mapping]
    if missing:
        raise ValueError(f"Missing columns in dataset: {missing}")

    return mapping


def validate_dataset(df, target):
    df = clean_columns(df)

    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found")

    if df.isnull().sum().sum() > 0:
        raise ValueError("Dataset has missing values")

    return True