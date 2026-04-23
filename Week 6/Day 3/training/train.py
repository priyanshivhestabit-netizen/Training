import pandas as pd
import numpy as np
import json, pickle, os
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import (accuracy_score, precision_score, recall_score,f1_score, roc_auc_score, ConfusionMatrixDisplay)
import xgboost as xgb

def evaluate(model, X, y):
    preds = model.predict(X)
    proba = model.predict_proba(X)[:,1]
    return {
        "accuracy":  round(accuracy_score(y, preds), 4),
        "precision": round(precision_score(y, preds, zero_division=0), 4),
        "recall":    round(recall_score(y, preds, zero_division=0), 4),
        "f1":        round(f1_score(y, preds, zero_division=0), 4),
        "roc_auc":   round(roc_auc_score(y, proba), 4),
    }

def train_all():
    X_train = pd.read_csv("src/data/processed/X_train.csv")
    X_test  = pd.read_csv("src/data/processed/X_test.csv")
    y_train = pd.read_csv("src/data/processed/y_train.csv").squeeze()
    y_test  = pd.read_csv("src/data/processed/y_test.csv").squeeze()
    neg = (y_train == 0).sum()
    pos = (y_train == 1).sum()
    scale = round(neg / pos, 2)
    print(f"Class ratio — No Churn: {neg}, Churn: {pos}, scale_pos_weight: {scale}")

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, C=1.0, class_weight="balanced"),

        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced"),

        "XGBoost": xgb.XGBClassifier(n_estimators=100, use_label_encoder=False, eval_metric="logloss", random_state=42, scale_pos_weight=scale),

        "NeuralNet": MLPClassifier(hidden_layer_sizes=(64,32), max_iter=300, random_state=42),
    }
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    all_metrics = {}
    best_name, best_auc = None, 0
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        cv_results = cross_validate(model, X_train, y_train, cv=cv,
                                    scoring=["accuracy","f1","roc_auc"], return_train_score=True)
        model.fit(X_train, y_train)
        test_metrics = evaluate(model, X_test, y_test)
        
        all_metrics[name] = {
            "cv_accuracy_mean": round(cv_results["test_accuracy"].mean(), 4),
            "cv_f1_mean":       round(cv_results["test_f1"].mean(), 4),
            "cv_roc_auc_mean":  round(cv_results["test_roc_auc"].mean(), 4),
            "test": test_metrics,
        }
        print(f"  Test AUC: {test_metrics['roc_auc']}")
        
        if test_metrics["roc_auc"] > best_auc:
            best_auc = test_metrics["roc_auc"]
            best_name = name
            best_model = model
    
    # Save best model
    os.makedirs("models", exist_ok=True)
    with open("src/models/best_model.pkl", "wb") as f:
        pickle.dump(best_model, f)
    
    # Save metrics
    os.makedirs("evaluation", exist_ok=True)
    with open("src/evaluation/metrics.json", "w") as f:
        json.dump(all_metrics, f, indent=2)
    
    # Confusion matrix for best model
    ConfusionMatrixDisplay.from_estimator(best_model, X_test, y_test)
    plt.title(f"Confusion matrix — {best_name}")
    plt.savefig("src/evaluation/confusion_matrix.png")
    plt.show()
    
    print(f"\nBest model: {best_name} (AUC={best_auc})")
    return best_model, best_name

if __name__ == "__main__":
    train_all()