import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from sklearn.ensemble import RandomForestRegressor

# === CARICA DATASET ===
df = pd.read_csv("dati_traiettorie_volano.csv")

# === 1. BOXPLOT VARIANZA PER STESSI INPUT ===
df["combinazione"] = df["altezza_robot_cm"].astype(str) + "cm_" + df["inclinazione_gradi"].astype(str) + "°_" + df["pwm_motori"].astype(str)
ripetuti = df[df.duplicated("combinazione", keep=False)]

plt.figure(figsize=(12, 6))
sns.boxplot(x="combinazione", y="x_atterraggio_cm", data=ripetuti)
plt.xticks(rotation=90)
plt.title("Variazione dei punti di atterraggio per stessi input")
plt.ylabel("X atterraggio [cm]")
plt.xlabel("Combinazioni (altezza_angolo_PWM)")
plt.tight_layout()
plt.savefig("grafici_rf/boxplot_varianza_stessi_input.png")
plt.close()

# === 2. SUPERFICIE 3D DELLA PREVISIONE ===
altezza_fissa = 95
angoli = np.linspace(0, 25, 20)
pwms = np.linspace(1100, 1260, 30)
grid_angoli, grid_pwms = np.meshgrid(angoli, pwms)

# Allena il modello
X = df[["altezza_robot_cm", "inclinazione_gradi", "pwm_motori"]].values
y = df["x_atterraggio_cm"].values
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

# Predizioni per griglia
grid_preds = np.zeros_like(grid_angoli)
for i in range(grid_angoli.shape[0]):
    for j in range(grid_angoli.shape[1]):
        input_vect = [[altezza_fissa, grid_angoli[i, j], grid_pwms[i, j]]]
        grid_preds[i, j] = model.predict(input_vect)

# Plot superficie
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(grid_angoli, grid_pwms, grid_preds, cmap=cm.viridis, edgecolor='none')
ax.set_xlabel("Angolo [°]")
ax.set_ylabel("PWM")
ax.set_zlabel("X predetto [cm]")
ax.set_title(f"Superficie predizione RF (altezza = {altezza_fissa} cm)")
plt.tight_layout()
plt.savefig("grafici_rf/superficie_predizione_rf.png")
plt.close()