import io
import tempfile
import subprocess
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys 
import os


try: 
    import duckdb
except Exception:
    duckdb=None


#Load data
def look_csv(raw_bytes: bytes) -> bool:
    try:
        sample=raw_bytes[:1024].decode(errors="ignore")
    except Exception :
        return False
    return "," in sample and "\n" in sample

def load_data(file_or_path)-> pd.DataFrame:
    """
    Accptss Stremlit Uploaded file or a file path and returns a pandas DataFrame.
    """

    if isinstance(file_or_path,(str,Path)):
        p=Path(file_or_path)
        s=p.suffix.lower()
        if s == ".csv":
            return pd.read_csv(p)
        if s in {".xls",".xlsx"}:
            return pd.read_excel(p)
        if s==".json":
            return pd.read_json(p)
        
        name=getattr(file_or_path,"name",None)
        suffix=Path(name).suffix.lower() if name else None
        raw=file_or_path.read()
        if isinstance(raw,str):
            raw=raw.encode()
        bio=io.BytesIO(raw)

        try:
            return pd.read_csv(bio)
        except Exception:
            bio.seek(0); return  pd.read_json(bio)
