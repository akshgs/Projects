import io
import tempfile
import subprocess
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys 
import os

from wsgiref import types
def detect_column_type(df: pd.DataFrame):
    numeric=df.select_dtypes(include=["np.number"]).columns.tolist()
    datetime=[]
    for c in df.columns:
        if np.issubdtype(df[c].dtype,np.datetime64):
            datetime.append(c)
        else:
            try:
                sample=df[c].dropna().astype(str).iloc[:20]
                parsed=pd.to_datetime(sample,errors="coerce")
                if parsed.notna().sum() >= max(1,min(5,len(sample)//2)):
                    datetime.append(c)
            except Exception:
                pass
    categorical=[c for c in df.columns if c  not in numeric + datetime and df[c].nunique(dropna=True)<=50]
    return {"numeric": numeric, "datetime": datetime, "categorical": categorical} 


def suggest_prompts(df: pd.DataFrame, max_suggestions: int = 8):
    """
    Return a list of helpful, ready-to-run prompt strings for the dataset.
    Deterministic and works without any LLM.
    """
    types = detect_column_type(df)
    numeric = types["numeric"]
    datetime = types["datetime"]
    categorical = types["categorical"]

    suggestion=[]

    suggestion.append("Summarize the dataset in 5 bullet points (rows, columns, missing values, numeric columns, top categorical).")

    if categorical:
        col=categorical[0]
        suggestion.append(f"Show the top 10 counts for the categorical column '{col}'.")

    if numeric:
        suggestion.append(f"Show summary statistics...")
    col = numeric[0]
    suggestion.append(f"Create a histogram of '{col}'.")
    if len(numeric) >= 2:
        suggestion.append(f"Scatter plot '{numeric[0]}' vs '{numeric[1]}'.")
    suggestion.append(f"Top 10 rows sorted by '{col}' descending.")
    if datetime:
        dcol = datetime[0]
    ag = numeric[0] if numeric else None
    if ag:
        suggestion.append(f"Time series of monthly sum of '{ag}' using '{dcol}'.")
    else:
        suggestion.append(f"Show counts per month using '{dcol}'.")
    if len(numeric) >= 2:
        suggestion.append("Show the correlation matrix heatmap...")

    suggestion.append("Find rows that look like anomalies using z-score > 3...")

    return suggestion[:max_suggestions]




 
    