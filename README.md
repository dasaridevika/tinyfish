# TinyFish Keyword Finder

A streamlined Streamlit application that uses **TinyFish** to search the web or deep-scan specific URLs for your target keywords and extract structured insights based on your main goal.

---

## 🚀 Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Secret
Set your `TINYFISH_API_KEY` in:
- **Streamlit Community Cloud Secrets** (for cloud deployment: `TINYFISH_API_KEY = "sk-tinyfish-..."`)
- **Environment Variable** (for local run: `$env:TINYFISH_API_KEY="sk-tinyfish-..."` or local `.env` file)

### 3. Run the App
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## 📂 Project Structure

```
tinyfish-keyword-monitor/
├── README.md          # Documentation
├── requirements.txt   # Core dependencies
└── app.py             # Single-file Streamlit application
```
