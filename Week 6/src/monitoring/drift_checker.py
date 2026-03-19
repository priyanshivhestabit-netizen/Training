import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

def check_drift(reference_path, new_path, threshold=0.05):
    ref = pd.read_csv(reference_path)
    new = pd.read_csv(new_path)
    
    drift_report = {}
    for col in ref.select_dtypes(include=np.number).columns:
        if col in new.columns:
            stat, p_value = ks_2samp(ref[col].dropna(), new[col].dropna())
            drift_report[col] = {
                "ks_statistic": round(stat, 4),
                "p_value": round(p_value, 4),
                "drift_detected": p_value < threshold
            }
    
    drifted = [k for k, v in drift_report.items() if v["drift_detected"]]
    print(f"Drift detected in {len(drifted)} features: {drifted}")
    return drift_report

if __name__ == "__main__":
    report = check_drift("data/processed/X_train.csv", "data/processed/X_test.csv") 