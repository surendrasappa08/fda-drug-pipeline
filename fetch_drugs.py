import requests
import json
import sqlite3

# FDA OpenFDA API - completely free, no API key needed
BASE_URL = "https://api.fda.gov/drug/event.json"

def fetch_drug_events(limit=100):
    """Fetch drug adverse event reports from FDA"""
    params = {
        "limit": limit,
        "search": "serious:1"  # Only serious adverse events
    }
    
    print("Fetching drug data from FDA API...")
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    results = data.get("results", [])
    print(f"Fetched {len(results)} drug event reports")
    return results

def save_to_database(events):
    """Save drug events to SQLite database"""
    conn = sqlite3.connect("fda_drugs.db")
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS drug_events")
    cursor.execute("""
        CREATE TABLE drug_events (
            report_id TEXT,
            patient_age REAL,
            patient_sex TEXT,
            reaction TEXT,
            drug_name TEXT,
            drug_role TEXT,
            serious INTEGER
        )
    """)
    
    count = 0
    for event in events:
        report_id = event.get("safetyreportid", "")
        serious = event.get("serious", 0)
        
        patient = event.get("patient", {})
        age = patient.get("patientonsetage", None)
        sex = patient.get("patientsex", "")
        
        reactions = patient.get("reaction", [])
        reaction_text = reactions[0].get("reactionmeddrapt", "") if reactions else ""
        
        drugs = patient.get("drug", [])
        for drug in drugs:
            drug_name = drug.get("medicinalproduct", "")
            drug_role = drug.get("drugcharacterization", "")
            
            cursor.execute("""
                INSERT INTO drug_events VALUES (?,?,?,?,?,?,?)
            """, (report_id, age, sex, reaction_text, drug_name, drug_role, serious))
            count += 1
    
    conn.commit()
    print(f"Saved {count} drug records to database")
    conn.close()

# Run it
events = fetch_drug_events(100)
save_to_database(events)