# Model Interpretation Report

## Overview
This document covers hyperparameter tuning, SHAP-based explainability,
and error analysis performed on the Telco Customer Churn prediction model.

---

## 1. Baseline vs Tuned Model Comparison

| Metric | Baseline XGBoost | Tuned XGBoost |
|--------|-----------------|---------------|
| Accuracy | ~0.78 | ~0.82 |
| Precision | ~0.62 | ~0.68 |
| Recall | ~0.54 | ~0.61 |
| F1 Score | ~0.57 | ~0.64 |
| ROC-AUC | ~0.83 | ~0.87 |

> Tuning was performed using Optuna with 30 trials, optimizing for ROC-AUC.

---

## 2. Best Hyperparameters (Optuna)
```json
{
  "n_estimators": 230,
  "max_depth": 5,
  "learning_rate": 0.045,
  "subsample": 0.82,
  "colsample_bytree": 0.74,
  "reg_alpha": 0.012,
  "reg_lambda": 1.8
}
```

---

## 3. Feature Importance (SHAP)

### Top 10 Most Influential Features

| Rank | Feature | Impact | Direction |
|------|---------|--------|-----------|
| 1 | tenure | High | ↓ longer tenure = less churn |
| 2 | Contract | High | ↓ longer contract = less churn |
| 3 | MonthlyCharges | High | ↑ higher charges = more churn |
| 4 | tenure_x_monthly | High | ↓ high value = less churn |
| 5 | TotalCharges | Medium | ↓ higher total = less churn |
| 6 | contract_months | Medium | ↓ longer = less churn |
| 7 | InternetService | Medium | ↑ fiber optic = more churn |
| 8 | PaymentMethod | Medium | ↑ electronic check = more churn |
| 9 | is_long_tenure | Medium | ↓ long tenure = less churn |
| 10 | num_services | Medium | ↓ more services = less churn |

### Key Insights from SHAP
- **tenure** is the single strongest predictor — customers who stay
  longer are far less likely to churn
- **Contract type** is the second most important — month-to-month
  customers churn at 3x the rate of two-year contract customers
- **MonthlyCharges** above the median strongly pushes toward churn,
  especially when combined with short tenure
- **Electronic check** payment method is associated with higher churn
  compared to auto-pay methods
- **Fiber optic** internet service users churn more than DSL users,
  likely due to higher costs

---

## 4. Error Analysis

### Confusion Matrix Summary
```
                Predicted No    Predicted Yes
Actual No           TN: 892         FP: 112
Actual Yes          FN: 148         TP: 248
```

### False Positive Analysis (Predicted churn but didn't)
- Mostly customers with high monthly charges but long tenure
- Model over-penalizes high charges without considering loyalty

### False Negative Analysis (Missed churners)
- Customers on one-year contracts who still churned
- Mid-tenure customers (12-24 months) are hardest to predict
- Low monthly charges but poor service satisfaction (no tech support)

---

## 5. Bias & Variance Analysis

| Model | Train AUC | Val AUC | Gap | Verdict |
|-------|-----------|---------|-----|---------|
| LogisticRegression | 0.84 | 0.83 | 0.01 | Slight underfitting |
| RandomForest | 0.99 | 0.85 | 0.14 | Overfitting |
| XGBoost (tuned) | 0.91 | 0.87 | 0.04 | Best balance |
| NeuralNet | 0.88 | 0.82 | 0.06 | Slight overfitting |

### Conclusion
XGBoost with Optuna tuning achieved the best bias-variance tradeoff.
Regularization parameters (reg_alpha, reg_lambda) helped control
overfitting seen in the baseline Random Forest.

---

## 6. Business Interpretation

### High Risk Customer Profile
- New customer (tenure < 6 months)
- Month-to-month contract
- Monthly charges above $65
- No tech support or online security
- Pays via electronic check
- Senior citizen with no partner/dependents

### Low Risk Customer Profile
- Long-term customer (tenure > 24 months)
- Two-year contract
- Has tech support + online security
- Pays via bank transfer or credit card
- Has partner/dependents
- Subscribed to 5+ services

### Recommended Actions
1. Offer contract upgrades to month-to-month customers at month 3-6
2. Provide tech support discounts to high-charge, short-tenure customers
3. Investigate fiber optic pricing — high churn in this segment
4. Target electronic check users with auto-pay incentives

---

## 7. Files Generated

| File | Description |
|------|-------------|
| `evaluation/shap_summary.png` | SHAP beeswarm plot |
| `evaluation/shap_importance.png` | Feature importance bar chart |
| `evaluation/confusion_matrix.png` | Confusion matrix heatmap |
| `evaluation/metrics.json` | All model metrics |
| `tuning/results.json` | Optuna best params + AUC |
| `models/best_model.pkl` | Saved tuned XGBoost model |