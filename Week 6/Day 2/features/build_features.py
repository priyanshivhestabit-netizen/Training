import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import json, os

def build_features(path="src/data/processed/final.csv"):
    df = pd.read_csv(path)
    

    df["charges_per_month"] = df["TotalCharges"] / (df["tenure"] + 1)
    df["is_long_tenure"] = (df["tenure"] > 24).astype(int)
    df["is_high_monthly"] = (df["MonthlyCharges"] > df["MonthlyCharges"].median()).astype(int)
    df["tenure_sq"] = df["tenure"] ** 2
    df["charges_log"] = np.log1p(df["TotalCharges"])
    df["monthly_log"] = np.log1p(df["MonthlyCharges"])
    df["tenure_x_monthly"] = df["tenure"] * df["MonthlyCharges"]
    
    # Contract length numeric encoding
    contract_map = {"Month-to-month": 1, "One year": 12, "Two year": 24}
    df["contract_months"] = df["Contract"].map(contract_map)
    
    df["has_tech_support"] = (df["TechSupport"] == "Yes").astype(int)
    df["has_online_security"] = (df["OnlineSecurity"] == "Yes").astype(int)
    df["num_services"] = (df[["PhoneService","MultipleLines","InternetService",
                               "OnlineSecurity","OnlineBackup","DeviceProtection",
                               "TechSupport","StreamingTV","StreamingMovies"]] == "Yes").sum(axis=1)
    
   
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    cat_cols = [c for c in cat_cols if c != "customerID"]
    
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
    
    df = df.drop(columns=["customerID"], errors="ignore")
    X = df.drop("Churn", axis=1)
    y = df["Churn"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_sc = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
    X_test_sc  = pd.DataFrame(scaler.transform(X_test),  columns=X_test.columns)
    
    # Save
    os.makedirs("src/data/processed", exist_ok=True)
    X_train_sc.to_csv("src/data/processed/X_train.csv", index=False)
    X_test_sc.to_csv("src/data/processed/X_test.csv", index=False)
    y_train.to_csv("src/data/processed/y_train.csv", index=False)
    y_test.to_csv("src/data/processed/y_test.csv", index=False)
    
    with open("src/features/feature_list.json", "w") as f:
        json.dump(list(X.columns), f, indent=2)
    
    print(f"Features saved. Train shape: {X_train_sc.shape}")
    return X_train_sc, X_test_sc, y_train, y_test

if __name__ == "__main__":
    build_features()