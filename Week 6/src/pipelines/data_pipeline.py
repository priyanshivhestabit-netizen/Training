import pandas as pd 
import numpy as np 
from pathlib import Path 
from sklearn.preprocessing import StandardScaler

RAW_PATH = "src/data/raw/telco_churn.csv"
PROCESSED_PATH = "src/data/processed/final.csv"

def load_data():
    df = pd.read_csv(RAW_PATH)
    return df

# print(load_data().info())

def clean_data(df):
    df = df.drop_duplicates()

    #convert TotalCharges
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"],errors="coerce")

    # fill missing value
    df["TotalCharges"].fillna(df["TotalCharges"].median())

    return df

def remove_outliers(df):

    numeric_cols = df.select_dtypes(include = np.number).columns

    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3-q1

        lower = q1-1.5*iqr
        upper = q3+1.5*iqr

        df = df[(df[col] >= lower) & (df[col] <= upper)]
    return df

def save_processed(df):
    Path("data/processed").mkdir(parents = True, exist_ok=True)
    df.to_csv(PROCESSED_PATH,index=False)

def main():
    df = load_data()
    df = clean_data(df)
    df = remove_outliers(df)

    save_processed(df)

if __name__ =="__main__":
    main()


