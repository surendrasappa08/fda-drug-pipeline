import sqlite3
import csv
from datetime import datetime

conn = sqlite3.connect("fda_drugs.db")
cursor = conn.cursor()

# Create risk summary table
cursor.execute("DROP TABLE IF EXISTS drug_risk_summary")
cursor.execute("""
    CREATE TABLE drug_risk_summary (
        drug_name TEXT,
        total_reports INTEGER,
        analyzed_at TEXT
    )
""")

result = cursor.execute("""
    SELECT drug_name, COUNT(DISTINCT report_id) as reports
    FROM drug_events
    WHERE drug_name != ''
    GROUP BY drug_name
    ORDER BY reports DESC
    LIMIT 10
""").fetchall()

for row in result:
    cursor.execute("""
        INSERT INTO drug_risk_summary VALUES (?,?,?)
    """, (row[0], row[1], datetime.now().strftime("%Y-%m-%d %H:%M")))

conn.commit()

# Export to CSV for dashboard
with open("drug_risk_summary.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["drug_name", "total_reports", "analyzed_at"])
    writer.writerows(result)

print(f"Saved {len(result)} drugs to drug_risk_summary.csv")
conn.close()