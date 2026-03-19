import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR/"src"/"data"/"processed"/"final.csv"

def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

def create_features(df):

    # 1. tenure_groups => customer duration bucket
    df["tenure_group"] = pd.cut(
        df["tenure"],
        bins = [0,12,24,48,72],
        labels = ["0-1yr","1-2yr","2-4yr","4-6yr"]
    )

    # 2. average monthly spend
    df["avg_monthly_spend"] = df["TotalCharges"] / (df["tenure"] + 1)

    # 3. change ratio
    df["change_ratio"] = df["MonthlyCharges"] / (df["TotalCharges"] + 1)

    # 4. long term customer
    df["is_long_term"] = (df["tenure"] > 24).astype(int)

    # 5. internet flag
    df["has_internet"] = (df["InternetService"] != "No").astype(int)

    # 6. automatic payment
    df["auto_payment"] = df["PaymentMethod"].str.contains("automatic").astype(int)

    # 7. senior flag
    df["senior_flag"] = df["SeniorCitizen"]

    # 8. family flag
    df["family_customer"] = (
        (df["Partner"] == "Yes") | (df["Dependents"] == "Yes")
    ).astype(int)

    # 9. service count
    services = [
        "PhoneService",
        "InternetService"
    ]

    df["service_count"] = df[services].apply(
        lambda x: (x!="No").sum(),axis=1
    )

    return df

def encode_categorical(df):

    cat_cols = df.select_dtypes(include="object").columns

    le = LabelEncoder()

    for col in cat_cols:
        if(col!="customerID"):
            df[col] = le.fit_transform(df[col].astype(str))
    return df

def split_data(df):

    X = df.drop(["Churn","customerID"],axis=1)
    y = df["Churn"]

    return train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

def main():
    df = load_data()
    df = create_features(df)
    df=encode_categorical(df)

    X_train, X_test, y_train ,y_test = split_data(df)

    print("Train shape:", X_train.shape)
    print("Test shape:", X_test.shape)

    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    main()

