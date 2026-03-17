"""
Master script: runs all data collection steps in order.
Run this from the project root: python data/run_data_collection.py
"""

import subprocess
import sys
from pathlib import Path

scripts = [
    ("Generating synthetic patients", "data/generate_patients.py"),
    ("Fetching medications from OpenFDA", "data/fetch_openfda.py"),
    ("Fetching drug interactions from RxNav", "data/fetch_interactions.py"),
]

base = Path(__file__).parent.parent

for label, script in scripts:
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    result = subprocess.run(
        [sys.executable, str(base / script)],
        cwd=str(base)
    )
    if result.returncode != 0:
        print(f"\nFailed at: {script}")
        sys.exit(1)

print("\n\nAll data collection complete!")
print("Files saved:")
print("  data/synthetic_patients/patients.json")
print("  data/raw/medications.json")
print("  data/raw/interactions.json")
