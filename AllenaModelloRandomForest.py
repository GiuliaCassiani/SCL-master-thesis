import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt

# === Carica dataset ===
df = pd.read_csv("dati_traiettorie_volano.csv")
X = df[["altezza_robot_cm", "inclinazione_gradi", "pwm_motori"]].values
y = df["x_atterraggio_cm"].values

# === Train/test split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# === Definisci e allena Random Forest ===
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=None,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# === Valutazione ===
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\n🌲 Random Forest addestrata")
print(f"MSE: {mse:.2f} cm²")
print(f"R² (coeff. determinazione): {r2:.3f}")

# === Esempi
print("\n🎯 Esempi (reale vs predetto):")
for i in range(5):
    print(f"Reale: {y_test[i]:.1f} cm | Predetto: {y_pred[i]:.1f} cm")

# === Salva modello
joblib.dump(model, "modello_rf_volano.pkl")
print("\n💾 Modello Random Forest salvato in 'modello_rf_volano.pkl'")

# === (Opzionale) Importanza delle feature
feature_names = ["altezza_cm", "angolo_gradi", "pwm"]
importanze = model.feature_importances_

plt.figure(figsize=(6, 4))
plt.barh(feature_names, importanze)
plt.xlabel("Importanza relativa")
plt.title("Importanza delle variabili (Random Forest)")
plt.tight_layout()
plt.grid(True)
plt.savefig("grafici/importanza_variabili_rf.png")
plt.show()