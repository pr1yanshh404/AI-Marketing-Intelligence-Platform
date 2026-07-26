# AdVantage AI - Marketing Intelligence & Business Analytics Platform

AdVantage AI is a production-grade AI-powered marketing intelligence platform built for modern business analysts and growth marketers. It unifies scattered data from multi-channel ad platforms (Meta Ads, Google Ads) and Web Analytics (Google Analytics 4), executes automated ETL processes, computes critical growth marketing KPIs, and provides generative AI insights and natural language database Q&A.

## 🚀 Key Features

1. **Multi-Brand Architecture**: Supports cross-brand portfolio analytics (**AuraFit Wireless**, **LuxeGlow Beauty**, and **UrbanKicks Apparel**) with side-by-side benchmarking and brand-specific deep dives.
2. **Robust Data Pipeline (ETL)**: Automatically ingests Meta Ads, Google Ads, and website tracking CSVs across brands, cleans/transforms the schema, and builds a relational SQLite database schema with Dimension & Fact tables.
2. **KPI Performance Dashboard**: Real-time interactive calculations of **ROAS, CAC, CTR, CPC, Conversion Rate, impressions, clicks, leads, and customer purchases** with beautiful, custom-themed Plotly charts.
3. **Automated AI Audits**: Leverages the Google Gemini API to analyze campaign data, explain performance in plain English, and pinpoint high-converting or wasteful campaigns.
4. **AI Budget Reallocations**: Generates optimal spend distribution suggestions dynamically to maximize overall revenue.
5. **Interactive SQL & LLM Agent Chat**: Translates raw business questions (e.g., *"Which Meta Ads campaign has the lowest CAC?"*) into standard SQL queries, runs them against the SQLite database, and returns the response in plain English.
6. **Weekly Report Writer**: Creates business-ready executive briefings for C-Suite alignment.
7. **SQL Playground**: Includes a developer sandbox for running custom SQL queries directly against database tables.

---

## 📁 Repository Structure

```
ai_marketing_platform/
├── README.md                 # Professional portfolio documentation
├── requirements.txt         # Package dependencies
├── app.py                   # Streamlit front-end application
├── sql/
│   ├── schema.sql           # SQLite database schema definitions
│   └── kpi_queries.sql      # Analytical SQL KPI scripts
├── src/
│   ├── data_generator.py    # Synthesizes 12 months of multi-channel ad data
│   ├── etl_pipeline.py      # Python ETL loading raw data to SQLite
│   └── ai_assistant.py      # Gemini API wrappers & SQLite AI chatbot agent
└── data/                    # Raw CSVs and SQLite databases (Generated on run)
```

---

## 🛠️ Tech Stack
- **Dashboard UI**: Streamlit with custom CSS (glassmorphism/dark mode)
- **Data Engineering**: Python, Pandas, SQLite
- **Visualizations**: Plotly (Scatter, Line, Donut, Bar charts)
- **AI/LLM Layer**: Google Gemini API (`google-generativeai`)

---

## ⚙️ Installation & Running Locally

### 1. Clone & Navigate to Folder
```bash
cd ai_marketing_platform
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Gemini API Key
To enable the AI capabilities, export your Gemini API key:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-gemini-api-key-here"

# Linux / Mac / Command Prompt
export GEMINI_API_KEY="your-gemini-api-key-here"
```
*(If no API key is provided, the platform will automatically fall back to rule-based analysis and pre-scripted database SQL responses to ensure a functional UI demo).*

### 4. Run the Platform
```bash
streamlit run app.py
```
*On launch, the platform will automatically trigger the synthetic data generator and run the ETL pipeline, creating the `data/marketing.db` SQLite database.*
