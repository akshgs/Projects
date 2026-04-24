# 🤖 Personal AI Data Analyst

An interactive data analysis dashboard built with **Streamlit** that lets you upload a dataset and instantly get AI-powered insights — no coding required.

---

## 🚀 Features

- 📂 Upload **CSV, Excel, or JSON** files
- 🔍 **Auto-suggests** relevant analysis prompts based on your data
- 📊 Built-in support for:
  - Dataset summary
  - Histograms & scatter plots
  - Correlation heatmap
  - Top N value counts
  - Time series monthly aggregation
  - Anomaly detection (z-score)
- 🤖 Optional **local LLM support** via [Ollama](https://ollama.com) for custom prompts
- ⬇️ Download results as CSV

---

## 🗂️ Project Structure

```
Personal_Ai_DataAnalyst/
│
├── app.py                # Main Streamlit UI
├── analyst.py            # Prompt → Python code translator
├── Execution.py          # Safe code execution engine
├── llm.py                # Ollama LLM integration
├── data_loading.py       # File loader (CSV/Excel/JSON)
├── prompt_suggesion.py   # Auto-suggest prompts from dataset
├── .env                  # API keys (not committed)
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/akshgs/Projects.git
cd Projects/Personal_Ai_DataAnalyst
```

### 2. Install dependencies
```bash
pip install streamlit pandas numpy matplotlib scipy openpyxl
```

### 3. Run the app
```bash
streamlit run app.py
```

---

## 🧠 Using Local LLM (Optional)

For custom prompts beyond the built-in patterns, you can use [Ollama](https://ollama.com):

```bash
# Install Ollama
winget install Ollama.Ollama

# Pull a model
ollama pull llama3.1
```

Then enable **"Use local LLM"** in the sidebar.

> ⚠️ Requires ~5 GB of free storage for the model.

---

## 📸 Screenshots

> Upload a file → Select a prompt → Click Run analysis → Get instant results!

---

## 🛠️ Built With

- [Streamlit](https://streamlit.io)
- [Pandas](https://pandas.pydata.org)
- [Matplotlib](https://matplotlib.org)
- [NumPy](https://numpy.org)
- [SciPy](https://scipy.org)
- [Ollama](https://ollama.com) *(optional)*

---

## 👤 Author

**Akash** — [GitHub](https://github.com/akshgs)