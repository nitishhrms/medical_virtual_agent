"""
Generates synthetic patient records (no real patient data).
Saves results to data/synthetic_patients/patients.json
"""

import json
import random
from pathlib import Path
from datetime import date, timedelta

OUTPUT_PATH = Path(__file__).parent / "synthetic_patients" / "patients.json"

MEDICATIONS = [
    "metformin", "aspirin", "lisinopril", "atorvastatin", "amlodipine",
    "omeprazole", "sertraline", "levothyroxine", "gabapentin", "albuterol",
    "ibuprofen", "acetaminophen", "warfarin", "furosemide", "metoprolol",
    "insulin", "glipizide", "prednisone", "cetirizine", "loratadine",
]

CONDITIONS = [
    "Type 2 Diabetes", "Hypertension", "Asthma", "Hypothyroidism",
    "Depression", "Anxiety", "Heart Failure", "Atrial Fibrillation",
    "GERD", "Chronic Pain", "High Cholesterol", "Arthritis",
    "Epilepsy", "COPD", "Allergic Rhinitis",
]

ALLERGIES = [
    "Penicillin", "Sulfa drugs", "Aspirin", "Ibuprofen",
    "Codeine", "Latex", "None", "None", "None",  
]

GENDERS = ["Male", "Female", "Non-binary"]

BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


def random_dob(min_age=18, max_age=85) -> str:
    today = date.today()
    days_range = (max_age - min_age) * 365
    dob = today - timedelta(days=random.randint(min_age * 365, min_age * 365 + days_range))
    return dob.isoformat()


def generate_patient(patient_id: int) -> dict:
    dob = random_dob()
    age = (date.today() - date.fromisoformat(dob)).days // 365

    num_conditions = random.randint(1, 4)
    conditions = random.sample(CONDITIONS, num_conditions)

    num_meds = random.randint(1, 5)
    current_meds = random.sample(MEDICATIONS, num_meds)

    allergy = random.choice(ALLERGIES)

    return {
        "patient_id": f"P{patient_id:04d}",
        "name": f"Patient_{patient_id}",  # anonymized
        "date_of_birth": dob,
        "age": age,
        "gender": random.choice(GENDERS),
        "blood_type": random.choice(BLOOD_TYPES),
        "conditions": conditions,
        "current_medications": current_meds,
        "allergies": [allergy] if allergy != "None" else [],
        "notes": f"Patient has {', '.join(conditions).lower()}. Currently on {len(current_meds)} medications."
    }


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    patients = [generate_patient(i) for i in range(1, 101)]  # 100 patients

    with open(OUTPUT_PATH, "w") as f:
        json.dump(patients, f, indent=2)

    print(f"Generated {len(patients)} synthetic patient records -> {OUTPUT_PATH}")

    print("\nSample patient:")
    
    print(json.dumps(patients[0], indent=2))


if __name__ == "__main__":
    main()
