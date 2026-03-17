"""
Enriches interactions.json with accurate clinical descriptions for known drug pairs.
Overwrites data/raw/interactions.json with enriched data.
"""

import json
from pathlib import Path

PATH = Path(__file__).parent / "raw" / "interactions.json"

KNOWN_INTERACTIONS = {
    ("aspirin", "warfarin"): ("major", "Aspirin inhibits platelet aggregation and can displace warfarin from plasma proteins, significantly increasing bleeding risk."),
    ("ibuprofen", "aspirin"): ("moderate", "NSAIDs like ibuprofen can reduce the antiplatelet effect of low-dose aspirin and increase GI bleeding risk."),
    ("metformin", "alcohol"): ("moderate", "Alcohol combined with metformin increases risk of lactic acidosis, a rare but serious condition."),
    ("warfarin", "ibuprofen"): ("major", "Ibuprofen inhibits platelet function and can increase warfarin levels, raising bleeding risk."),
    ("lisinopril", "potassium"): ("moderate", "ACE inhibitors like lisinopril increase potassium retention; adding potassium supplements can cause hyperkalemia."),
    ("simvastatin", "amiodarone"): ("major", "Amiodarone inhibits CYP3A4, increasing simvastatin plasma levels and risk of myopathy/rhabdomyolysis."),
    ("clopidogrel", "omeprazole"): ("moderate", "Omeprazole inhibits CYP2C19, reducing conversion of clopidogrel to its active form and decreasing antiplatelet effect."),
    ("fluoxetine", "tramadol"): ("major", "Fluoxetine inhibits CYP2D6, increasing tramadol levels. Both lower seizure threshold and risk serotonin syndrome."),
    ("sertraline", "tramadol"): ("major", "Combination increases serotonin syndrome risk and can lower the seizure threshold."),
    ("alprazolam", "oxycodone"): ("major", "CNS depressant combination can cause profound sedation, respiratory depression, and death."),
    ("clonazepam", "alcohol"): ("major", "Alcohol potentiates CNS depression of benzodiazepines, increasing sedation and respiratory depression risk."),
    ("digoxin", "amiodarone"): ("major", "Amiodarone increases digoxin levels by reducing its renal and non-renal clearance, risking digoxin toxicity."),
    ("metformin", "ibuprofen"): ("moderate", "NSAIDs can reduce renal function, decreasing metformin excretion and increasing risk of lactic acidosis."),
    ("lisinopril", "ibuprofen"): ("moderate", "NSAIDs can blunt the antihypertensive effect of ACE inhibitors and increase risk of renal impairment."),
    ("atorvastatin", "clarithromycin"): ("major", "Clarithromycin inhibits CYP3A4, dramatically increasing atorvastatin levels and risk of myopathy."),
    ("simvastatin", "gemfibrozil"): ("major", "Gemfibrozil inhibits simvastatin metabolism via CYP2C8/OATP1B1, greatly increasing myopathy risk."),
    ("warfarin", "acetaminophen"): ("moderate", "High-dose or prolonged acetaminophen use can enhance warfarin anticoagulation, increasing bleeding risk."),
    ("metoprolol", "verapamil"): ("major", "Combined use can cause severe bradycardia, heart block, or cardiac arrest due to additive negative chronotropic effects."),
    ("carvedilol", "digoxin"): ("moderate", "Carvedilol increases digoxin levels by up to 60% in some patients; monitor for digoxin toxicity."),
    ("furosemide", "gentamicin"): ("major", "Both are ototoxic; combination significantly increases risk of hearing loss and nephrotoxicity."),
    ("hydrochlorothiazide", "lithium"): ("major", "Thiazide diuretics reduce renal lithium excretion, leading to lithium toxicity."),
    ("ciprofloxacin", "warfarin"): ("major", "Ciprofloxacin inhibits CYP1A2 and reduces gut flora that synthesize vitamin K, increasing warfarin effect."),
    ("doxycycline", "antacids"): ("moderate", "Divalent cations in antacids (Ca2+, Mg2+, Al3+) chelate doxycycline, reducing its oral absorption by up to 90%."),
    ("prednisone", "ibuprofen"): ("major", "Combining corticosteroids with NSAIDs greatly increases risk of GI ulcers and bleeding."),
    ("tramadol", "ssri"): ("major", "SSRIs plus tramadol increase serotonin syndrome risk and lower seizure threshold."),
    ("clopidogrel", "aspirin"): ("moderate", "Dual antiplatelet therapy increases bleeding risk; combination is intentional only in specific cardiovascular conditions."),
    ("losartan", "potassium"): ("moderate", "ARBs like losartan increase potassium retention; adding potassium supplements can cause hyperkalemia."),
    ("spironolactone", "lisinopril"): ("moderate", "Both increase potassium levels; combination risks hyperkalemia, especially in patients with renal impairment."),
    ("gabapentin", "oxycodone"): ("major", "CNS depressant combination increases risk of sedation, respiratory depression, and overdose death."),
    ("cyclobenzaprine", "alcohol"): ("major", "Alcohol potentiates CNS depression of cyclobenzaprine, increasing sedation and impairment."),
    ("cetirizine", "alcohol"): ("moderate", "Alcohol can enhance CNS sedation caused by antihistamines like cetirizine."),
    ("alprazolam", "alcohol"): ("major", "Life-threatening combination — additive CNS and respiratory depression."),
    ("morphine", "alcohol"): ("major", "Alcohol increases morphine CNS and respiratory depression, risking fatal overdose."),
    ("hydrocodone", "alprazolam"): ("major", "Opioid + benzodiazepine combination is a leading cause of overdose death; causes respiratory depression."),
    ("levothyroxine", "calcium"): ("moderate", "Calcium supplements bind levothyroxine in the gut, reducing its absorption by up to 40%. Separate doses by 4 hours."),
    ("levothyroxine", "iron"): ("moderate", "Iron salts chelate levothyroxine in the gut, reducing absorption. Separate doses by at least 4 hours."),
    ("metformin", "contrast_dye"): ("major", "Iodinated contrast media can cause acute kidney injury, impairing metformin excretion and triggering lactic acidosis."),
    ("warfarin", "vitamin_k"): ("moderate", "Vitamin K is the antidote to warfarin. Dietary changes in vitamin K intake can significantly alter INR."),
    ("fluoxetine", "maoi"): ("contraindicated", "Life-threatening serotonin syndrome. Fluoxetine must not be used within 14 days of an MAOI."),
    ("sertraline", "maoi"): ("contraindicated", "Life-threatening serotonin syndrome risk. SSRIs are contraindicated with MAOIs."),
    ("tizanidine", "ciprofloxacin"): ("contraindicated", "Ciprofloxacin inhibits CYP1A2, causing up to 10-fold increase in tizanidine levels, risking severe hypotension."),
    ("sildenafil", "nitrates"): ("contraindicated", "Both cause vasodilation; combination causes severe, life-threatening hypotension."),
    ("amoxicillin", "warfarin"): ("moderate", "Antibiotics reduce gut flora producing vitamin K, potentially enhancing warfarin's anticoagulant effect."),
    ("azithromycin", "warfarin"): ("moderate", "Azithromycin can increase warfarin effect through gut flora alteration and possible CYP inhibition."),
    ("escitalopram", "tramadol"): ("major", "Increased serotonin syndrome risk and additive seizure risk."),
    ("verapamil", "simvastatin"): ("major", "Verapamil inhibits CYP3A4, increasing simvastatin levels and myopathy risk. Max simvastatin 10mg with verapamil."),
    ("diltiazem", "simvastatin"): ("major", "Diltiazem inhibits CYP3A4; simvastatin dose should not exceed 10mg when combined."),
    ("rosuvastatin", "gemfibrozil"): ("major", "Gemfibrozil inhibits OATP1B1 transporter, increasing rosuvastatin levels and myopathy risk."),
    ("naproxen", "warfarin"): ("major", "NSAIDs inhibit platelet function and may raise warfarin levels, increasing bleeding risk."),
    ("celecoxib", "warfarin"): ("major", "Celecoxib inhibits CYP2C9-mediated warfarin metabolism; increases anticoagulant effect and bleeding risk."),
    ("diclofenac", "lithium"): ("major", "NSAIDs reduce renal lithium clearance, increasing lithium blood levels and toxicity risk."),
}


def normalize(a, b):
    return tuple(sorted([a.lower(), b.lower()]))


def main():
    with open(PATH) as f:
        interactions = json.load(f)

    enriched = 0
    for entry in interactions:
        key = normalize(entry["drug1"], entry["drug2"])
        if key in KNOWN_INTERACTIONS:
            severity, description = KNOWN_INTERACTIONS[key]
            entry["severity"] = severity
            entry["description"] = description
            entry["source"] = "clinical_reference"
            enriched += 1

    with open(PATH, "w") as f:
        json.dump(interactions, f, indent=2)

    print(f"Enriched {enriched}/{len(interactions)} interactions with clinical descriptions.")
    print(f"Saved to {PATH}")


if __name__ == "__main__":
    main()
