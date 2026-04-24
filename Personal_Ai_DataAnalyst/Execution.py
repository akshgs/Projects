import io
import sys
import tempfile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def run_code(df: pd.DataFrame, code: str) -> dict:
    """
    Execute code string in a restricted local namespace.
    Returns a dict with one of:
      - {"type": "text",      "output": str}
      - {"type": "dataframe", "df": pd.DataFrame}
      - {"type": "image",     "path": str}
    """
    local_ns = {"pd": pd, "np": np, "df": df, "plt": plt}

    old_stdout = sys.stdout
    stdout_buf = io.StringIO()
    sys.stdout = stdout_buf

    try:
        exec(code, {}, local_ns)  # noqa: S102

        # 1. Explicit image path set by code
        if local_ns.get("result_img_path"):
            return {"type": "image", "path": local_ns["result_img_path"]}

        # 2. Matplotlib figure present → save to temp PNG
        if plt.get_fignums():
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
                plt.savefig(f.name, bbox_inches="tight", dpi=150)
                plt.close("all")
                return {"type": "image", "path": f.name}

        # 3. result variable set
        if "result" in local_ns:
            res = local_ns["result"]
            if isinstance(res, pd.DataFrame):
                return {"type": "dataframe", "df": res}
            return {"type": "text", "output": str(res)}

        # 4. Captured stdout
        out = stdout_buf.getvalue().strip()
        if out:
            return {"type": "text", "output": out}

        return {"type": "text", "output": "Execution finished. No result produced."}

    except Exception as e:
        return {"type": "text", "output": f"Execution error: {e}"}

    finally:
        sys.stdout = old_stdout
        plt.close("all")  # FIX: leftover figures