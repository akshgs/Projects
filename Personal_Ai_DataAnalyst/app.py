import streamlit as st
from data_loading import load_data
from prompt_suggesion import suggest_prompts
from analyst import prompt_to_code
from Execution import run_code
from llm import ask_llm
import pandas as pd

st.set_page_config(page_title="Personal AI Data Analyst", layout="wide")
st.title("🤖 Personal AI Data Analyst — Interactive Dashboard")

st.sidebar.header("Settings")
use_llm = st.sidebar.checkbox("Use local LLM (ollama) for custom prompts", value=False)
llm_model = st.sidebar.text_input("LLM model name (ollama)", value="llama3.1")
st.sidebar.markdown("If you don't have `ollama` installed, leave this off and use built-in prompts.")

uploaded = st.file_uploader("Upload CSV, Excel, or JSON", type=["csv", "xls", "xlsx", "json"])
if uploaded is None:
    st.info("Upload a CSV / XLSX / JSON to get started. Suggestions will appear automatically.")
    st.stop()

# ── Load data ──
try:
    df = load_data(uploaded)
except Exception as e:
    st.error(f"Failed to load file: {e}")
    st.stop()

st.success(f"✅ File loaded! Rows: {len(df)}, Columns: {len(df.columns)}")
with st.expander("Preview data (first 100 rows)"):
    st.dataframe(df.head(100), width='stretch')

# ── Suggestions ──
suggestions = suggest_prompts(df)
st.markdown("## Suggested analyses (pick one or write your own)")
col1, col2 = st.columns([3, 1])
with col1:
    selected = st.selectbox("Choose a suggested prompt", options=suggestions)
    custom = st.text_area(
        "Or write a custom prompt (leave blank to use the selected suggestion)",
        height=80
    )
with col2:
    st.markdown("**Quick actions**")
    if st.button("Show suggestions again"):
        st.write(suggestions)

# ── Final prompt ──
final_prompt = custom.strip() if custom and custom.strip() else selected

st.markdown("### Final prompt")
st.write(final_prompt)

# ── Run button ──
if st.button("▶ Run analysis", type="primary"):

    res = None

    with st.spinner("Running..."):

        # Step 1: built-in translator
        code = prompt_to_code(final_prompt, df)

        if code:
            res = run_code(df, code)

        else:
            if use_llm:
                system = (
                    "You are a helpful data analyst and will respond with Python code only.\n"
                    "You must return code inside a ```python ... ``` block. The DataFrame is named `df`.\n"
                    "Use pandas for data manipulation and matplotlib for charts. Do not import heavy libs.\n"
                    "If returning a chart, produce matplotlib code that draws the figure (no show()) and nothing else.\n"
                )
                raw = system + "\n# User prompt: " + final_prompt
                llm_out = ask_llm(raw, model=llm_model)

                if llm_out.startswith("[LLM-"):
                    st.warning("LLM unavailable or returned an error.")
                    st.write(llm_out)
                    st.stop()

                if "```python" in llm_out:
                    try:
                        code = llm_out.split("```python")[1].split("```")[0].strip()
                        res = run_code(df, code)
                    except Exception as e:
                        st.error(f"Failed to execute code from LLM: {e}")
                        st.write(llm_out)
                        st.stop()
                else:
                    st.error("LLM did not return a python code block. Showing raw LLM output:")
                    st.write(llm_out)
                    st.stop()
            else:
                st.error(
                    "This prompt doesn't match any built-in pattern. "
                    "Enable 'Use local LLM' in the sidebar, or choose a suggested prompt."
                )
                st.stop()

    # ── Display result ──
    if res is None:
        st.warning("No result was produced.")
        st.stop()

    if res["type"] == "text":
        st.markdown("#### Output (text)")
        st.text(res["output"])

    elif res["type"] == "dataframe":
        st.markdown("#### Output (table)")
        st.dataframe(res["df"], width='stretch')
        csv = res["df"].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Download result as CSV",
            data=csv,
            file_name="result.csv",
            mime="text/csv"
        )

    elif res["type"] == "image":
        st.markdown("#### Output (chart)")
        st.image(res["path"], width='stretch')

    else:
        st.write("Unknown result type", res)