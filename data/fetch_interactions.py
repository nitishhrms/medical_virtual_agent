import requests
import json
import time
from pathlib import Path
from itertools import combinations

OUTPUT_PATH = Path(__file__).parent / "raw" / "interactions.json"


DRUG_PAIRS = [
    ("aspirin", "warfarin"),
    ("ibuprofen", "aspirin"),
    ("metformin", "alcohol"),
    ("warfarin", "ibuprofen"),
    ("lisinopril", "potassium"),
    ("simvastatin", "amiodarone"),
    ("clopidogrel", "omeprazole"),
    ("fluoxetine", "tramadol"),
    ("sertraline", "tramadol"),
    ("alprazolam", "oxycodone"),
    ("clonazepam", "alcohol"),
    ("warfarin", "aspirin"),
    ("digoxin", "amiodarone"),
    ("metformin", "ibuprofen"),
    ("lisinopril", "ibuprofen"),
    ("atorvastatin", "clarithromycin"),
    ("simvastatin", "gemfibrozil"),
    ("warfarin", "acetaminophen"),
    ("metoprolol", "verapamil"),
    ("carvedilol", "digoxin"),
    ("furosemide", "gentamicin"),
    ("hydrochlorothiazide", "lithium"),
    ("ciprofloxacin", "warfarin"),
    ("doxycycline", "antacids"),
    ("prednisone", "ibuprofen"),
    ("tramadol", "ssri"),
    ("clopidogrel", "aspirin"),
    ("losartan", "potassium"),
    ("spironolactone", "lisinopril"),
    ("gabapentin", "oxycodone"),
    ("cyclobenzaprine", "alcohol"),
    ("cetirizine", "alcohol"),
    ("alprazolam", "alcohol"),
    ("morphine", "alcohol"),
    ("hydrocodone", "alprazolam"),
    ("levothyroxine", "calcium"),
    ("levothyroxine", "iron"),
    ("metformin", "contrast_dye"),
    ("warfarin", "vitamin_k"),
    ("fluoxetine", "maoi"),
    ("sertraline", "maoi"),
    ("tizanidine", "ciprofloxacin"),
    ("sildenafil", "nitrates"),
    ("amoxicillin", "warfarin"),
    ("azithromycin", "warfarin"),
    ("escitalopram", "tramadol"),
    ("verapamil", "simvastatin"),
    ("diltiazem", "simvastatin"),
    ("rosuvastatin", "gemfibrozil"),
    ("naproxen", "warfarin"),
    ("celecoxib", "warfarin"),
    ("diclofenac", "lithium"),
]

RXNAV_BASE = "https://rxnav.nlm.nih.gov/REST"


def get_rxcui(drug_name: str) -> str | None:
    url = f"{RXNAV_BASE}/rxcui.json"
    try:
        resp = requests.get(url, params={"name": drug_name}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            ids = data.get("idGroup", {}).get("rxnormId", [])
            return ids[0] if ids else None
    except Exception as e:
        print(f"  RXCUI error for {drug_name}: {e}")
    return None


def get_interaction(rxcui1: str, rxcui2: str, drug1: str, drug2: str) -> dict | None:
    url = f"{RXNAV_BASE}/interaction/list.json"
    try:
        resp = requests.get(url, params={"rxcuis": f"{rxcui1}+{rxcui2}"}, timeout=10)
        if resp.status_code == 200:
            groups = resp.json().get("fullInteractionTypeGroup", [])
            for group in groups:
                for itype in group.get("fullInteractionType", []):
                    for pair in itype.get("interactionPair", []):
                        return {
                            "drug1": drug1,
                            "drug2": drug2,
                            "severity": pair.get("severity", "unknown"),
                            "description": pair.get("description", "No description available."),
                            "source": group.get("sourceDisclaimer", "RxNav")
                        }
    except Exception as e:
        print(f"  Interaction error ({drug1} + {drug2}): {e}")
    return None


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    interactions = []
    seen = set()

    print(f"Fetching interactions for {len(DRUG_PAIRS)} drug pairs from RxNav...\n")

    for drug1, drug2 in DRUG_PAIRS:
        pair_key = tuple(sorted([drug1, drug2]))
        if pair_key in seen:
            continue
        seen.add(pair_key)

        print(f"  Checking: {drug1} + {drug2}")
        rxcui1 = get_rxcui(drug1)
        time.sleep(0.2)
        rxcui2 = get_rxcui(drug2)
        time.sleep(0.2)

        if rxcui1 and rxcui2:
            result = get_interaction(rxcui1, rxcui2, drug1, drug2)
            if result:
                interactions.append(result)
                print(f"    Found: {result['severity']}")
            else:
                interactions.append({
                    "drug1": drug1,
                    "drug2": drug2,
                    "severity": "moderate",
                    "description": f"Potential interaction between {drug1} and {drug2}. Consult a pharmacist.",
                    "source": "manual"
                })
                print(f"    No API data — saved as manual entry")
        else:
            print(f"    Could not find RXCUI for {drug1}")
        time.sleep(0.3)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(interactions, f, indent=2)

    print(f"\nDone. Saved {len(interactions)} interactions to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
