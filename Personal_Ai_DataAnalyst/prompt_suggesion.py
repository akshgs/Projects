import pandas as pd
import numpy as np

def detect_column_type(df: pd.DataFrame):
    numeric = df.select_dtypes(include=["number"]).columns.tolist()
    datetime = []
    for c in df.columns:
        if np.issubdtype(df[c].dtype, np.datetime64):
            datetime.append(c)
        else:
            try:
                sample = df[c].dropna().astype(str).iloc[:20]
                # FIX: format="mixed" 
                parsed = pd.to_datetime(sample, errors="coerce", format="mixed")
                if parsed.notna().sum() >= max(1, min(5, len(sample) // 2)):
                    datetime.append(c)
            except Exception:
                pass
    categorical = [
        c for c in df.columns
        if c not in numeric + datetime and df[c].nunique(dropna=True) <= 50
    ]
    return {"numeric": numeric, "datetime": datetime, "categorical": categorical}


def suggest_prompts(df: pd.DataFrame, max_suggestions: int = 8):
    col_types = detect_column_type(df)
    numeric = col_types["numeric"]
    datetime = col_types["datetime"]
    categorical = col_types["categorical"]

    suggestion = []

    suggestion.append("Summarize the dataset in 5 bullet points.")

    if categorical:
        col = categorical[0]
        suggestion.append(f"Show the top 10 counts for the categorical column '{col}'.")

    if numeric:
        col = numeric[0]
        suggestion.append(f"Show summary statistics for '{col}'.")
        suggestion.append(f"Create a histogram of the numeric column '{col}'.")
        if len(numeric) >= 2:
            suggestion.append(f"Scatter plot comparing '{numeric[0]}' (x) vs '{numeric[1]}' (y).")
        suggestion.append(f"Show the top 10 rows sorted by '{col}'.")

    if datetime:
        dcol = datetime[0]
        ag = numeric[0] if numeric else None
        if ag:
            suggestion.append(f"Monthly sum of '{ag}' using the datetime column '{dcol}'.")
        else:
            suggestion.append(f"Counts per month using the datetime column '{dcol}'.")

    if len(numeric) >= 2:
        suggestion.append("Show the correlation matrix heatmap.")

    suggestion.append("Find rows that look like anomalies using z-score > 3.")

    return suggestion[:max_suggestions]