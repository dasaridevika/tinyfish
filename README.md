# TinyFish Keyword Finder

A streamlined Streamlit application that uses **TinyFish** to search the web or deep-scan specific URLs for your target keywords and extract structured insights based on your main goal.

---

## 🚀 Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

### 3. Usage
1. Enter your **Main Goal** (e.g. *Extract full roadmap, syllabus, and beginner guides*).
2. Enter your **Keywords** (e.g. *Python, AI agents, LangChain*).
3. *(Optional)* Provide a **Target URL** to deep-scan a specific webpage, or leave it blank to search the live web.
4. Click **Find Results**.

---

## 📂 Project Structure

```
tinyfish-keyword-monitor/
├── .env.example       # API Key configuration template
├── README.md          # Documentation
├── requirements.txt   # Minimal dependencies
└── app.py             # Single-file Streamlit application
```
