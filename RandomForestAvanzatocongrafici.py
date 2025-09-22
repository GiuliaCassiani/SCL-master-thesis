import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, max_error

# === PARAMETERS ===
csv_path = "dati_traiettorie_volano.csv"
output_dir = "rf_plots"
os.makedirs(output_dir, exist_ok=True)

# === 1. Load dataset ===
df = pd.read_csv(csv_path)
X = df[["altezza_robot_cm", "inclinazione_gradi", "pwm_motori"]]
y = df["x_atterraggio_cm"]

# === 2. Train/Test split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# === 3. Train Random Forest ===
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# === 4. Evaluation ===
y_pred_test = model.predict(X_test)
y_pred_all = model.predict(X)

mse = mean_squared_error(y_test, y_pred_test)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred_test)
r2 = r2_score(y_test, y_pred_test)
maxerr = max_error(y_test, y_pred_test)

print("\n RANDOM FOREST PERFORMANCE:")
print(f"  MAE:  {mae:.2f} cm")
print(f"️  RMSE: {rmse:.2f} cm")
print(f"  MSE:  {mse:.2f} cm²")
print(f"️  R²:   {r2:.3f}")
print(f"  Max error: {maxerr:.2f} cm")

print("\n Example predictions (test set):")
for i in range(5):
    print(f"Real: {y_test.values[i]:.1f} cm | Predicted: {y_pred_test[i]:.1f} cm")

# === 5. Save model and results ===
df["predicted_cm"] = y_pred_all
df["abs_error_cm"] = np.abs(df["x_atterraggio_cm"] - df["predicted_cm"])

joblib.dump(model, "random_forest_model.pkl")
df.to_csv("rf_results_full.csv", index=False)
print("\n Model saved as 'random_forest_model.pkl'")
print(" Full predictions saved to 'rf_results_full.csv'")

# === 6. PLOTS ===

# 1. Real vs Predicted
plt.figure(figsize=(6,6))
plt.scatter(df["x_atterraggio_cm"], df["predicted_cm"], alpha=0.7)
plt.plot([df["x_atterraggio_cm"].min(), df["x_atterraggio_cm"].max()],
         [df["x_atterraggio_cm"].min(), df["x_atterraggio_cm"].max()],
         'r--', label="Ideal")
plt.xlabel("Real X [cm]")
plt.ylabel("Predicted X [cm]")
plt.title("Real vs Predicted")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(f"{output_dir}/real_vs_predicted.png")
plt.close()

# 2. Error vs PWM
plt.figure(figsize=(7,5))
plt.scatter(df["pwm_motori"], df["abs_error_cm"], alpha=0.7)
plt.xlabel("Motor PWM")
plt.ylabel("Absolute Error [cm]")
plt.title("Error vs PWM")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{output_dir}/error_vs_pwm.png")
plt.close()

# 3. Error distribution
plt.figure(figsize=(7,5))
sns.histplot(df["abs_error_cm"], bins=20, kde=True)
plt.xlabel("Absolute Error [cm]")
plt.title("Error Distribution")
plt.tight_layout()
plt.savefig(f"{output_dir}/error_distribution.png")
plt.close()

# 4. Boxplot Error by Angle
plt.figure(figsize=(8,5))
sns.boxplot(data=df, x="inclinazione_gradi", y="abs_error_cm")
plt.xlabel("Elevation Angle [°]")
plt.ylabel("Absolute Error [cm]")
plt.title("Error by Angle")
plt.tight_layout()
plt.savefig(f"{output_dir}/boxplot_error_angle.png")
plt.close()

# 5. Feature importance
importances = model.feature_importances_
feature_names = X.columns
plt.figure(figsize=(6,4))
sns.barplot(x=importances, y=feature_names)
plt.title("Feature Importance")
plt.xlabel("Importance")
plt.tight_layout()
plt.savefig(f"{output_dir}/feature_importance.png")
plt.close()

print(f"\n Plots saved to folder: {output_dir}")