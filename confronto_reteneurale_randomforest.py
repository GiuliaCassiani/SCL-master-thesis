import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset
df = pd.read_csv("dati_traiettorie_volano.csv")
X = df[["altezza_robot_cm", "inclinazione_gradi", "pwm_motori"]].values
y = df["x_atterraggio_cm"].values

# Split and scale
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Neural Network
mlp = MLPRegressor(hidden_layer_sizes=(32, 32), max_iter=5000, random_state=42)
mlp.fit(X_train_scaled, y_train)
y_pred_nn = mlp.predict(X_test_scaled)

# Load trained Random Forest model
rf = joblib.load("random_forest_model.pkl")
y_pred_rf = rf.predict(X_test)

# Evaluation metrics
mse_nn = mean_squared_error(y_test, y_pred_nn)
r2_nn = r2_score(y_test, y_pred_nn)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print("\nModel Comparison:")
print(f"Random Forest → MSE: {mse_rf:.2f}, R²: {r2_rf:.3f}")
print(f"Neural Network → MSE: {mse_nn:.2f}, R²: {r2_nn:.3f}")

# Plot predictions
plt.figure(figsize=(8, 6))
plt.plot(y_test, y_pred_rf, 'go', label="Random Forest", alpha=0.6)
plt.plot(y_test, y_pred_nn, 'b^', label="Neural Network", alpha=0.6)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--', label="Ideal")

plt.xlabel("Actual X [cm]")
plt.ylabel("Predicted X [cm]")
plt.title("Prediction Comparison: RF vs NN")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("rf_plots/rf_vs_nn_comparison.png")
plt.show()