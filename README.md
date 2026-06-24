# FDA Drug Interaction Pipeline with AI Risk Analysis

An end-to-end data pipeline that ingests real FDA adverse event data, stores it in a database, and uses AI to flag dangerous drug interactions and risk levels.

## Architecture
FDA OpenFDA API → fetch_drugs.py → SQLite Database
→ ai_analysis.py (Groq LLaMA AI) → Risk Flags
→ save_results.py → drug_risk_summary.csv → Dashboard

## What it does
1. **Ingest** — Pulls real serious adverse event reports from FDA's public API
2. **Store** — Saves 338+ drug records into a SQLite database
3. **AI Analysis** — Uses Groq LLaMA AI to assess risk level, dangerous interactions, and patient warnings for each drug
4. **Export** — Saves summary table to CSV for dashboard visualization

## Tech Stack
- Python 3 — data ingestion and pipeline orchestration
- FDA OpenFDA API — real government drug safety data (no API key needed)
- SQLite — relational database storage
- Groq API (LLaMA 3) — free AI model for drug risk analysis
- CSV — summary export for dashboarding

## Key Results
- Ingested 100 serious adverse event reports → 338 drug records
- AI flagged HIGH risk drugs: JAKAFI (CYP3A4 interactions), PREDNISONE (immunosuppression)
- AI flagged LOW risk drugs: CEFTRIAXONE (calcium interaction only)

## How to Run
1. Clone this repo
2. Install dependencies: pip3 install requests python-dotenv
3. Create a `.env` file with your free Groq API key: GROQ_API_KEY=your_key_here
4. Run the pipeline:
python3 fetch_drugs.py
python3 ai_analysis.py
python3 save_results.py

## What I Learned
- How to call a real government REST API (FDA OpenFDA)
- How to integrate a free AI model (Groq/LLaMA) into a data pipeline
- How to structure an ETL pipeline with multiple scripts
- Secure API key management with environment variables