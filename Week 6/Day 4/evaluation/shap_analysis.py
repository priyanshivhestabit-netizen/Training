import pandas as pd
import pickle
import shap
import matplotlib.pyplot as plt

X_test = pd.read_csv("src/data/processed/X_test.csv")
y_test = pd.read_csv("src/data/processed/y_test.csv").squeeze()

with open("src/models/best_model.pkl", "rb") as f:
    model = pickle.load(f)

# SHAP explainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Summary plot
shap.summary_plot(shap_values, X_test, show=False)
plt.tight_layout()
plt.savefig("src/evaluation/shap_summary.png", bbox_inches="tight")
plt.show()

# Feature importance bar chart
shap.summary_plot(shap_values, X_test, plot_type="bar", show=False)
plt.tight_layout()
plt.savefig("src/evaluation/shap_importance.png", bbox_inches="tight")
plt.show()

print("SHAP analysis saved.")