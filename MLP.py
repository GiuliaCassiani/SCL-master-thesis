# === addestra_rete.py (versione migliorata) ===

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# === Carica dataset ===
df = pd.read_csv("dati_traiettorie_volano.csv")
X = df[["altezza_robot_cm", "inclinazione_gradi", "pwm_motori"]].values
y = df["x_atterraggio_cm"].values

# === Train/test split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# === Normalizzazione ===
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# === Definisci rete ottimizzata ===
model = MLPRegressor(
    hidden_layer_sizes=(16, 16),
    activation='relu',
    solver='adam',
    learning_rate_init=0.001,
    max_iter=5000,
    random_state=42,
    early_stopping=True,
    n_iter_no_change=30,
    verbose=True  # stampa i progressi
)

model.fit(X_train_scaled, y_train)

# === Valutazione ===
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\n✅ Rete addestrata con successo")
print(f"MSE: {mse:.2f} cm²")
print(f"R² (coeff. determinazione): {r2:.3f}")

# === Esempi di predizione ===
print("\n🎯 Esempi (reale vs predetto):")
for i in range(5):
    print(f"Reale: {y_test[i]:.1f} cm | Predetto: {y_pred[i]:.1f} cm")

# === Salva modello e scaler ===
joblib.dump(model, "modello_volano.pkl")
joblib.dump(scaler, "scaler_volano.pkl")
print("\n💾 Modello salvato in 'modello_volano.pkl'")
print("💾 Scaler salvato in 'scaler_volano.pkl'")