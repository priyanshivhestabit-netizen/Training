import pandas as pd
import json
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from src.features.build_features import main

def encode_remaining_categorical(X):

    le = LabelEncoder()

    for col in X.columns:
        if X[col].dtype == "object" or str(X[col].dtype) == "category":
            X[col] = le.fit_transform(X[col].astype(str))

    return X

def select_features():

    X_train, X_test, y_train, y_test = main()

    # encode categorical columns
    X_train = encode_remaining_categorical(X_train)
    X_test = encode_remaining_categorical(X_test)

    # mutual information
    mi = mutual_info_classif(X_train, y_train)

    mi_scores = pd.Series(mi, index=X_train.columns)

    top_features = mi_scores.sort_values(ascending=False).head(15).index

    X_train = X_train[top_features]
    X_test = X_test[top_features]

    # RFE
    model = RandomForestClassifier()

    rfe = RFE(model,n_features_to_select=10)

    rfe.fit(X_train,y_train)

    selected = X_train.columns[rfe.support_]

    return selected.tolist()

def save_features(feature_list):

    with open("features/feature_list.json","w") as f:
        json.dump(feature_list,f,indent=4)

def main_selector():

    features = select_features()
    save_features(features)
    print("Selected Features:")
    print(features)

if __name__ == "__main__":
    main_selector()
