import pandas as pd
import matplotlib.pyplot as plt

# === Carica dataset ===
df = pd.read_csv("dati_traiettorie_volano.csv")

# === Crea chiave testuale per etichette ===
df["label"] = df.apply(
    lambda row: f"P{row['pwm_motori']} T{row['inclinazione_gradi']} H{row['altezza_robot_cm']}",
    axis=1
)

# === Plot ===
plt.figure(figsize=(10, 7))

# Scatter: colore = angolo, size = altezza
scatter = plt.scatter(
    df["pwm_motori"],
    df["x_atterraggio_cm"],
    c=df["inclinazione_gradi"],
    s=df["altezza_robot_cm"] * 1.5,  # dimensione proporzionale all’altezza
    cmap="viridis",
    alpha=0.85,
    edgecolor='k'
)

# Etichette su ogni punto
for i, row in df.iterrows():
    plt.text(
        row["pwm_motori"] + 2,  # leggera distanza sull'asse X
        row["x_atterraggio_cm"] + 2,
        row["label"],
        fontsize=8,
        alpha=0.9
    )

# Colorbar e dettagli
cbar = plt.colorbar(scatter)
cbar.set_label("Inclinazione [°]", fontsize=11)

plt.title("PWM vs Distanza finale (colore = angolo, dimensione = altezza)", fontsize=13)
plt.xlabel("PWM motori", fontsize=11)
plt.ylabel("X atterraggio [cm]", fontsize=11)
plt.grid(True)
plt.tight_layout()
plt.show()