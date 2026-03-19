import pandas as pd
import json
import joblib

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import (cross_val_score, StratifiedKFold)
from sklearn.metrics import (
    accuracy_score, precision_score,
    recall_score, f1_score, roc_auc_score,
    confusion_matrix
)
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

from xgboost import XGBClassifier 

from src.features.build_features import main as build_data
from src.features.feature_selector import encode_remaining_categorical 

# Load selected features
def load_feature_list():
    with open("src/features/feature_list.json","r") as f:
        return json.load(f)
    
#prepare data
def prepare_data():

    X_train, X_test, y_train, y_test = build_data()

    #encode categorical
    X_train = encode_remaining_categorical(X_train)
    X_test = encode_remaining_categorical(X_test)

    selected_features = load_feature_list()

    X_train = X_train[selected_features]
    X_test = X_test[selected_features]

    #scaling data
    scaler=StandardScaler()

    X_train =scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test

#models
def get_models():
    return{
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForest": RandomForestClassifier(
            random_state=40
        ),
        "XGBoost": XGBClassifier(eval_metric="logloss", random_state=42),
        "NeuralNetwork": MLPClassifier(max_iter=500, random_state=42)
    }

#evaluate model
def evaluate_model(model,X_test,y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:,1]

    return {
        "accuracy": accuracy_score(y_test,y_pred),
        "precision": precision_score(y_test,y_pred),
        "recall":recall_score(y_test,y_pred),
        "f1":f1_score(y_test,y_pred),
        "roc_auc": roc_auc_score(y_test,y_proba)
    }

#plot confusion matrix
def plot_confusion(y_test,y_pred):
    cm = confusion_matrix(y_test,y_pred)
    sns.heatmap(cm,annot=True,fmt="d")
    plt.title("Confusion Matrix")
    plt.show()

#train pipeline
def train():
    X_train, X_test, y_train, y_test=prepare_data()

    models = get_models()
    results={}
    best_model=None
    best_score=0

    for name, model in models.items():
        print(f"\nTraining {name}")

        #cross validation
        cv = StratifiedKFold(n_splits=5, shuffle = True, random_state=42)
        cv_scores = cross_val_score(model,X_train,y_train,cv=cv, scoring="f1")

        model.fit(X_train,y_train)

        metrics = evaluate_model(model,X_test, y_test)
        metrics["cv_f1_mean"] = cv_scores.mean()

        results[name]  =metrics
        print(metrics)

        #select best model(based on f1)
        if metrics["f1"]  >best_score:
            best_score = metrics["f1"]
            best_model=model
            best_model_name=name
    print("\nBest Model:",best_model_name)

    #save best model
    joblib.dump(best_model,"src/models/best_model.pkl")

    #save metrics
    with open("src/evaluation/metrics.json","w") as f:
        json.dump(results,f,indent=4)

    #plot confusion metrics
    y_pred = best_model.predict(X_test)
    plot_confusion(y_test,y_pred)

    return results



if __name__=="__main__":
    train()

