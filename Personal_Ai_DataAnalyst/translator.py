import io
import tempfile
import subprocess
from pathlib import Path
import textwrap
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys 
import os

def prompt_to_code(prompt: str, df: pd.DataFrame):
    """
    Convert known prompt templates into runnable python code strings.
    If the prompt is custom/unrecognized, return None (so UI can send to LLM instead).
    """

    p=prompt.strip().lower()

    if p.startswith("summarize the dataset"):
        code = textwrap.dedent("""
            # produce a short summary as printed text
            info = []
            info.append(f"Rows: {len(df)}, Columns: {len(df.columns)}")
            info.append("Column types: " + ", ".join([f\"{c}:{str(df[c].dtype)[:10]}\" for c in df.columns[:10]]))
            miss = df.isnull().sum().sort_values(ascending=False).head(10)
            info.append("Top missing: " + ", ".join([f\"{idx}:{val}\" for idx,val in miss.items() if val>0]))
            numeric = df.select_dtypes(include=['number']).columns.tolist()
            info.append(f\"Numeric columns count: {len(numeric)}\")
            # print concise bullets
            result = \"\\n\".join([\"- \"+i for i in info])
        """)
        return code
    if "top 10 counts for the categorical column" in p or "top 10 counts" in p and "'" in p:
        import re
        m = re.search(r"'([^']+)'", prompt)
        m = re.search(r'"([^"]+)"', prompt)
        col = m.group(1) if m else None
        if col:
             code = textwrap.dedent(f"""
                # top 10 counts for '{col}'
                result = df['{col}'].value_counts(dropna=False).head(10).reset_index()
                result.columns = ['value','count']
            """)
        return code
    if p.startswith("create a histogram of the numeric column") or "histogram of the numeric column" in p:
        import re
        m = re.search(r"'([^']+)'", prompt)
        col = m.group(1) if m else None
        if col:
            code = textwrap.dedent(f"""
                # histogram for '{col}'
                plt.figure(figsize=(6,4))
                df['{col}'].dropna().astype(float).hist(bins=30)
                plt.title('Histogram of {col}')
                plt.xlabel('{col}')
                plt.ylabel('count')
                # produce an image by saving to result_img_path variable
                result_img_path = None
            """)
            # We'll return plotting code that uses plt; execution will save figure
            return code

    # Scatter plot
    if "scatter plot comparing" in p and "vs" in p:
        import re
        m = re.search(r"'([^']+)' \\(x\\) vs '([^']+)' \\(y\\)", prompt)
        if m:
            xcol, ycol = m.group(1), m.group(2)
            code = textwrap.dedent(f"""
                plt.figure(figsize=(6,4))
                df.plot.scatter(x='{xcol}', y='{ycol}')
                plt.title('{ycol} vs {xcol}')
                result_img_path = None
            """)
            return code

    # Top N rows sorted by col
    if p.startswith("show the top 10 rows sorted by"):
        import re
        m = re.search(r"by '([^']+)'", prompt)
        if m:
            col = m.group(1)
            code = textwrap.dedent(f"""
                result = df.sort_values('{col}', ascending=False).head(10).reset_index(drop=True)
            """)
            return code

    # Time series monthly sum
    if "monthly sum" in p and "using the datetime column" in p:
        import re
        m = re.search(r"sum of '([^']+)' using the datetime column '([^']+)'", prompt)
        if m:
            ag, dcol = m.group(1), m.group(2)
            code = textwrap.dedent(f"""
                tmp = df.copy()
                tmp['{dcol}'] = pd.to_datetime(tmp['{dcol}'], errors='coerce')
                res = tmp.dropna(subset=['{dcol}'])
                res = res.set_index('{dcol}').resample('M')['{ag}'].sum().reset_index()
                result = res
            """)
            return code

    # Counts per month (datetime only)
    if "counts per month using the datetime column" in p:
        import re
        m = re.search(r"datetime column '([^']+)'", prompt)
        dcol = m.group(1) if m else None
        if dcol:
            code = textwrap.dedent(f"""
                tmp = df.copy()
                tmp['{dcol}'] = pd.to_datetime(tmp['{dcol}'], errors='coerce')
                res = tmp.dropna(subset=['{dcol}']).set_index('{dcol}').resample('M').size().reset_index(name='count')
                result = res
            """)
            return code

    # Correlation heatmap
    if "correlation matrix heatmap" in p or "correlation heatmap" in p:
        code = textwrap.dedent("""
            corr = df.select_dtypes(include=['number']).corr()
            import matplotlib.pyplot as plt
            plt.figure(figsize=(6,5))
            plt.imshow(corr, cmap='viridis', aspect='auto')
            plt.colorbar()
            plt.xticks(range(len(corr)), corr.columns, rotation=90)
            plt.yticks(range(len(corr)), corr.columns)
            plt.title('Correlation matrix')
            result_img_path = None
        """)
        return code

    # Anomaly detection using z-score
    if "anomalies" in p and "z-score" in p:
        code = textwrap.dedent("""
            from scipy import stats
            num = df.select_dtypes(include=['number']).dropna()
            if num.shape[1]==0:
                result = pd.DataFrame()
            else:
                z = np.abs(stats.zscore(num.select_dtypes(include=['number'])))
                mask = (z > 3).any(axis=1)
                result = df.loc[mask].head(20).reset_index(drop=True)
        """)
        return code

    # Unknown / custom prompts -> return None
    return None
