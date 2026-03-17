"""
Fetches drug label data (uses, dosage, side effects, warnings) from OpenFDA API.
Saves results to data/raw/medications.json
"""

import requests
import json
import time
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent / "raw" / "medications.json"

# 75 common medications to fetch
MEDICATIONS = [
    "metformin", "aspirin", "ibuprofen", "lisinopril", "atorvastatin",
    "amlodipine", "omeprazole", "simvastatin", "losartan", "albuterol",
    "levothyroxine", "gabapentin", "hydrochlorothiazide", "sertraline",
    "fluoxetine", "amoxicillin", "azithromycin", "prednisone", "warfarin",
    "clopidogrel", "pantoprazole", "escitalopram", "rosuvastatin", "furosemide",
    "metoprolol", "montelukast", "acetaminophen", "cetirizine", "loratadine",
    "alprazolam", "clonazepam", "tramadol", "oxycodone", "hydrocodone",
    "morphine", "insulin", "glipizide", "glimepiride", "sitagliptin",
    "doxycycline", "ciprofloxacin", "cephalexin", "clindamycin", "trimethoprim",
    "naproxen", "diclofenac", "meloxicam", "celecoxib", "cyclobenzaprine",
    "tizanidine", "baclofen", "carvedilol", "bisoprolol", "diltiazem",
    "verapamil", "digoxin", "spironolactone", "bumetanide", "torsemide",
    "ramipril", "enalapril", "valsartan", "candesartan", "olmesartan",
    "pravastatin", "fluvastatin", "fenofibrate", "gemfibrozil", "ezetimibe",
    "ranitidine", "famotidine", "esomeprazole", "lansoprazole", "sucralfate"
]

BASE_URL = "https://api.fda.gov/drug/label.json"


def fetch_drug(drug_name: str) -> dict | None:
    params = {
        "search": f"openfda.generic_name:{drug_name}",
        "limit": 1
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            if results:
                r = results[0]
                openfda = r.get("openfda", {})
                return {
                    "name": drug_name,
                    "brand_names": openfda.get("brand_name", []),
                    "generic_name": openfda.get("generic_name", []),
                    "indications_and_usage": r.get("indications_and_usage", ["N/A"])[0][:1000],
                    "dosage_and_administration": r.get("dosage_and_administration", ["N/A"])[0][:1000],
                    "warnings": r.get("warnings", ["N/A"])[0][:1000],
                    "adverse_reactions": r.get("adverse_reactions", ["N/A"])[0][:1000],
                    "contraindications": r.get("contraindications", ["N/A"])[0][:500],
                    "drug_interactions": r.get("drug_interactions", ["N/A"])[0][:500],
                }
    except Exception as e:
        print(f"  Error fetching {drug_name}: {e}")
    return None


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    medications = []

    print(f"Fetching {len(MEDICATIONS)} medications from OpenFDA...\n")
    for i, drug in enumerate(MEDICATIONS, 1):
        print(f"[{i}/{len(MEDICATIONS)}] Fetching: {drug}")
        result = fetch_drug(drug)
        if result:
            medications.append(result)
            print(f"  OK - {result['brand_names'][:2]}")
        else:
            print(f"  SKIPPED (no data found)")
        time.sleep(0.3)  # respect rate limit

    with open(OUTPUT_PATH, "w") as f:
        json.dump(medications, f, indent=2)

    print(f"\nDone. Saved {len(medications)} medications to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
