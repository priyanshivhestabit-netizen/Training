import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_classif, RFE
from sklearn.ensemble import RandomForestClassifier

def select_features(X_train, y_train, top_n=15):
    # Method 1: Correlation threshold
    corr = X_train.corr().abs()
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    to_drop_corr = [c for c in upper.columns if any(upper[c] > 0.9)]
    print(f"High-corr columns to drop: {to_drop_corr}")
    
    # Method 2: Mutual information
    mi = mutual_info_classif(X_train, y_train, random_state=42)
    mi_series = pd.Series(mi, index=X_train.columns).sort_values(ascending=False)
    
    # Method 3: RFE with Random Forest
    rf = RandomForestClassifier(n_estimators=50, random_state=42)
    rfe = RFE(rf, n_features_to_select=top_n)
    rfe.fit(X_train, y_train)
    rfe_features = X_train.columns[rfe.support_].tolist()
    
    # Plot MI
    mi_series.head(top_n).plot(kind="bar", figsize=(10,4))
    plt.title("Top features by mutual information")
    plt.tight_layout()
    plt.savefig("src/logs/feature_importance.png")
    plt.show()
    
    return rfe_features

if __name__ == "__main__":
    X_train = pd.read_csv("src/data/processed/X_train.csv")
    y_train = pd.read_csv("src/data/processed/y_train.csv").squeeze()
    selected = select_features(X_train, y_train)
    print("Selected features:", selected)