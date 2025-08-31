import numpy as np
import matplotlib.pyplot as plt
import os

# === SCALING PARAMETERS ===
x_scaling_factor = 1.10  # adjust if needed

# === Load trajectories ===
folder = "traiettorie_npy"
trajectory_files = sorted([f for f in os.listdir(folder) if f.endswith(".npy")])

trajectories = []
labels = []

for filename in trajectory_files:
    path = os.path.join(folder, filename)
    data = np.load(path)  # array Nx2: [X, Z]

    # === Apply X scaling ===
    data[:, 0] *= x_scaling_factor

    # === Include trajectory up to and including Z <= 0
    z_vals = data[:, 1]
    idx_stop = None

    for i in range(1, len(z_vals)):
        if z_vals[i] <= 0:
            idx_stop = i
            break

    if idx_stop is not None:
        data_cut = data[:idx_stop + 1]  # include point at or just below Z=0
    else:
        data_cut = data  # no contact with ground

    trajectories.append(data_cut)

    # Label from filename
    base = filename.replace(".npy", "")
    labels.append(base.replace("_", ", "))  # example: H95, T20, PWM1200

# === Plot ===
plt.figure(figsize=(10, 6))

for traj, label in zip(trajectories, labels):
    X = traj[:, 0]
    Z = traj[:, 1]
    plt.plot(X, Z, marker='o', label=label)

plt.xlabel("X [cm]")
plt.ylabel("Z [cm]")
plt.title("Comparison of 2D Shuttlecock Trajectories")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()