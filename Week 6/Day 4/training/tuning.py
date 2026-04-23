import pandas as pd
import optuna
import pickle, json
import xgboost as xgb
from sklearn.model_selection import cross_val_score

X_train = pd.read_csv("src/data/processed/X_train.csv")
y_train = pd.read_csv("src/data/processed/y_train.csv").squeeze()

def objective(trial):
    params = {
        "n_estimators":     trial.suggest_int("n_estimators", 50, 300),
        "max_depth":        trial.suggest_int("max_depth", 3, 9),
        "learning_rate":    trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        "subsample":        trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
        "reg_alpha":        trial.suggest_float("reg_alpha", 1e-4, 10.0, log=True),
        "reg_lambda":       trial.suggest_float("reg_lambda", 1e-4, 10.0, log=True),
        "use_label_encoder": False,
        "eval_metric": "logloss",
        "random_state": 42,
    }
    model = xgb.XGBClassifier(**params)
    score = cross_val_score(model, X_train, y_train, cv=3, scoring="roc_auc").mean()
    return score

if __name__ == "__main__":
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=30, show_progress_bar=True)
    
    print("Best params:", study.best_params)
    print("Best AUC:", study.best_value)
    
    # Save best tuned model
    best_model = xgb.XGBClassifier(**study.best_params,
                                    use_label_encoder=False, eval_metric="logloss")
    best_model.fit(X_train, y_train)
    with open("src/models/best_model.pkl", "wb") as f:
        pickle.dump(best_model, f)
    
    with open("src/tuning/results.json", "w") as f:
        json.dump({"best_params": study.best_params, "best_auc": study.best_value}, f, indent=2)