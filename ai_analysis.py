import sqlite3
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_top_drugs():
    conn = sqlite3.connect("fda_drugs.db")
    cursor = conn.cursor()
    result = cursor.execute("""
        SELECT drug_name, COUNT(*) as frequency
        FROM drug_events
        WHERE drug_name != ''
        GROUP BY drug_name
        ORDER BY frequency DESC
        LIMIT 5
    """).fetchall()
    conn.close()
    return result

def analyze_with_groq(drugs):
    drug_list = [row[0] for row in drugs]
    drug_text = ", ".join(drug_list)
    
    print(f"Analyzing drugs: {drug_text}\n")
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{
                "role": "user",
                "content": f"""You are a clinical pharmacist analyzing FDA adverse event data.
These drugs appeared most in serious adverse event reports: {drug_text}

For each drug provide:
1. Risk level: HIGH/MEDIUM/LOW
2. Most common dangerous interaction
3. One-line patient warning

Be concise and clinical."""
            }],
            "max_tokens": 500
        }
    )
    
    result = response.json()
    print("API Response:", result)
    
    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {result}"

# Run
drugs = get_top_drugs()
print("Top drugs in FDA serious adverse events:")
for drug in drugs:
    print(f"  {drug[0]}: {drug[1]} records")

print("\n=== AI RISK ANALYSIS ===")
analysis = analyze_with_groq(drugs)
print(analysis)