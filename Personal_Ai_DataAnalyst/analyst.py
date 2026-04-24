import re
import textwrap
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def prompt_to_code(prompt: str, df: pd.DataFrame):
    """
    Convert known prompt templates into runnable python code strings.
    Returns None for custom/unrecognized prompts (UI sends to LLM instead).
    """
    p = prompt.strip().lower()

    # ── Summarize ──
    if p.startswith("summarize the dataset") or "summarize the dataset" in p or "5 bullet points" in p:
        code = textwrap.dedent("""
            info = []
            info.append(f"Rows: {len(df)}, Columns: {len(df.columns)}")
            info.append("Column types: " + ", ".join([f"{c}:{str(df[c].dtype)[:10]}" for c in df.columns[:10]]))
            miss = df.isnull().sum().sort_values(ascending=False).head(10)
            info.append("Top missing: " + ", ".join([f"{idx}:{val}" for idx, val in miss.items() if val > 0]) or "None")
            numeric = df.select_dtypes(include=['number']).columns.tolist()
            info.append(f"Numeric columns count: {len(numeric)}")
            result = "\\n".join(["- " + i for i in info])
        """)
        return code

    # ── Top 10 counts for categorical column ──
    if "top 10 counts for the categorical column" in p:
        m = re.search(r"'([^']+)'", prompt)
        col = m.group(1) if m else None
        if col:
            code = textwrap.dedent(f"""
                result = df['{col}'].value_counts(dropna=False).head(10).reset_index()
                result.columns = ['value', 'count']
            """)
            return code

    # ── Histogram ──
    if "histogram of the numeric column" in p:
        m = re.search(r"'([^']+)'", prompt)
        col = m.group(1) if m else None
        if col:
            code = textwrap.dedent(f"""
                plt.figure(figsize=(6,4))
                df['{col}'].dropna().astype(float).hist(bins=30)
                plt.title('Histogram of {col}')
                plt.xlabel('{col}')
                plt.ylabel('count')
                result_img_path = None
            """)
            return code

    # ── Scatter plot ──
    if "scatter plot comparing" in p and "vs" in p:
        # FIX: raw string — 
        m = re.search(r"'([^']+)' \(x\) vs '([^']+)' \(y\)", prompt)
        if m:
            xcol, ycol = m.group(1), m.group(2)
            code = textwrap.dedent(f"""
                plt.figure(figsize=(6,4))
                df.plot.scatter(x='{xcol}', y='{ycol}')
                plt.title('{ycol} vs {xcol}')
                result_img_path = None
            """)
            return code

    # ── Top 10 rows sorted ──
    if "top 10 rows sorted by" in p:
        m = re.search(r"by '([^']+)'", prompt)
        if m:
            col = m.group(1)
            code = textwrap.dedent(f"""
                result = df.sort_values('{col}', ascending=False).head(10).reset_index(drop=True)
            """)
            return code

    # ── Monthly sum (time series) ──
    if "monthly sum" in p and "using the datetime column" in p:
        m = re.search(r"monthly sum of '([^']+)' using the datetime column '([^']+)'", prompt, re.IGNORECASE)
        if m:
            ag, dcol = m.group(1), m.group(2)
            code = textwrap.dedent(f"""
                tmp = df.copy()
                tmp['{dcol}'] = pd.to_datetime(tmp['{dcol}'], errors='coerce')
                res = tmp.dropna(subset=['{dcol}'])
                res = res.set_index('{dcol}').resample('ME')['{ag}'].sum().reset_index()
                result = res
            """)
            return code

    # ── Counts per month ──
    if "counts per month using the datetime column" in p:
        m = re.search(r"datetime column '([^']+)'", prompt, re.IGNORECASE)
        dcol = m.group(1) if m else None
        if dcol:
            code = textwrap.dedent(f"""
                tmp = df.copy()
                tmp['{dcol}'] = pd.to_datetime(tmp['{dcol}'], errors='coerce')
                res = tmp.dropna(subset=['{dcol}']).set_index('{dcol}').resample('ME').size().reset_index(name='count')
                result = res
            """)
            return code

    # ── Correlation heatmap ──
    if "correlation matrix heatmap" in p or "correlation heatmap" in p:
        code = textwrap.dedent("""
            corr = df.select_dtypes(include=['number']).corr()
            plt.figure(figsize=(6,5))
            plt.imshow(corr, cmap='viridis', aspect='auto')
            plt.colorbar()
            plt.xticks(range(len(corr)), corr.columns, rotation=90)
            plt.yticks(range(len(corr)), corr.columns)
            plt.title('Correlation matrix')
            result_img_path = None
        """)
        return code

    # ── Anomaly detection ──
    if "anomalies" in p and "z-score" in p:
        code = textwrap.dedent("""
            from scipy import stats
            num = df.select_dtypes(include=['number']).dropna()
            if num.shape[1] == 0:
                result = pd.DataFrame()
            else:
                z = np.abs(stats.zscore(num))
                mask = (z > 3).any(axis=1)
                result = df.loc[mask].head(20).reset_index(drop=True)
        """)
        return code

    # ── Summary statistics ──
    if "summary statistics" in p:
        m = re.search(r"'([^']+)'", prompt)
        col = m.group(1) if m else None
        if col:
            code = textwrap.dedent(f"""
                result = df[['{col}']].describe().reset_index()
            """)
            return code

    return None