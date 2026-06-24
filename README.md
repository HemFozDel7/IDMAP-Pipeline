# IDAMP — Intent-Driven Agentic Medallion Pipeline
### Accelerate with AI Training Demo

A full-stack agentic data pipeline built with Streamlit where autonomous AI agents
transform raw CSV data through **Bronze → Silver → Gold** medallion layers with
human-in-the-loop approval gates.

## Quick Start

```bash
# 1. Clone / open this folder in VS Code

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

## Test Data

Use the files in `test_data/` to try the pipeline immediately:
- `properties.csv` — 120 Atlanta properties
- `transactions.csv` — 120 sale transactions
- `listings.csv` — 120 active/sold listings

## Architecture

```
app.py                  ← Streamlit entry point + sidebar router
├── pages/
│   ├── home.py         ← Upload + intent form
│   ├── phase1.py       ← Profiler + Bronze STTM
│   ├── hitl_bronze.py  ← HITL Gate 1
│   ├── phase2.py       ← Bronze execution + Silver STTM
│   ├── hitl_silver.py  ← HITL Gate 2
│   ├── phase3.py       ← Silver execution + Gold STTM
│   ├── hitl_gold.py    ← HITL Gate 3
│   ├── phase4.py       ← Gold execution + Report generation
│   └── complete.py     ← Pipeline complete + downloads
├── agents/
│   ├── profiler.py     ← CSV profiling → profile.json
│   ├── sttm_generator.py ← STTM rules (Bronze/Silver/Gold)
│   ├── bronze_agent.py ← CSV → Parquet + metadata injection
│   ├── silver_agent.py ← Cleansing, dedup, type cast, SK
│   ├── gold_agent.py   ← Joins, aggregations, KPIs
│   └── reporter.py     ← HTML executive report with charts
├── utils/
│   ├── state.py        ← Session state management
│   └── styles.py       ← Dark-theme CSS
├── test_data/          ← Sample CSVs
└── .streamlit/
    └── config.toml     ← Theme configuration
```
