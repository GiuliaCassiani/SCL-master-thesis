import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

# === PARAMETRI VIDEO ===
video_path = "lancio_due.avi"
scala_cm_per_px = 1.1063  # <--- INSERISCI la scala (cm/px)

# === INPUT MANUALI PER QUESTO LANCIO ===
altezza_robot_cm = 95           # <--- altezza robot da terra (es: 80 cm)
inclinazione_gradi = 5         # <--- angolo in gradi
pwm_motori = 1260               # <--- PWM motori

# === Background Subtractor ===
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)

def detect_motion(frame):
    mask = fgbg.apply(frame)
    mask = cv2.medianBlur(mask, 5)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = [c for c in contours if 50 < cv2.contourArea(c) < 2000]
    if candidates:
        c = max(candidates, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return (cx, cy)
    return None

def filtra_traiettoria_basata_su_velocita(punti, soglia_min=5, soglia_max=80, finestra=3):
    punti = np.array(punti)
    if len(punti) < finestra + 2:
        return punti
    diffs = np.linalg.norm(np.diff(punti, axis=0), axis=1)
    start_idx = 0
    for i in range(len(diffs) - finestra):
        if np.all((diffs[i:i+finestra] > soglia_min) & (diffs[i:i+finestra] < soglia_max)):
            start_idx = i
            break
    end_idx = len(punti)
    for i in range(len(diffs) - finestra, 0, -1):
        if np.all((diffs[i-finestra:i] > soglia_min) & (diffs[i-finestra:i] < soglia_max)):
            end_idx = i + 1
            break
    return punti[start_idx:end_idx]

def filtra_cambio_direzione(punti, angolo_max_deg=45):
    punti = np.array(punti)
    if len(punti) < 3:
        return punti
    filtrati = [punti[0]]
    for i in range(1, len(punti) - 1):
        v1 = punti[i] - punti[i - 1]
        v2 = punti[i + 1] - punti[i]
        if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
            continue
        cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angolo = np.arccos(np.clip(cos_theta, -1.0, 1.0)) * 180 / np.pi
        if angolo < angolo_max_deg:
            filtrati.append(punti[i])
    filtrati.append(punti[-1])
    return np.array(filtrati)

def filtra_fase_finale(punti_cm, soglia_vel=5.0, finestra=4):
    punti_cm = np.array(punti_cm)
    if len(punti_cm) < finestra + 2:
        return punti_cm
    vels = np.linalg.norm(np.diff(punti_cm, axis=0), axis=1)
    fine_idx = len(punti_cm)
    for i in range(len(vels) - finestra, 0, -1):
        if np.all(vels[i:i+finestra] > soglia_vel):
            fine_idx = i + finestra
            break
    return punti_cm[:fine_idx]

def converti_pixel_in_cm_relativo(traiettoria_px, scala_cm_per_px, altezza_robot_cm):
    px = np.array(traiettoria_px, dtype=np.float32)
    origine = px[0]
    delta = px - origine
    cm_x = delta[:, 0] * scala_cm_per_px
    cm_z = -delta[:, 1] * scala_cm_per_px + altezza_robot_cm  # Z verso l’alto da terra
    return np.stack([cm_x, cm_z], axis=1)

# === Tracking ===
cap = cv2.VideoCapture(video_path)
trajectory_px = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    pt = detect_motion(frame)
    if pt:
        trajectory_px.append(pt)
        cv2.circle(frame, pt, 6, (0, 0, 255), -1)
    cv2.imshow("Tracking", cv2.resize(frame, (640, 360)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# === Applica filtri e conversione ===
if len(trajectory_px) > 10:
    traj = np.array(trajectory_px)
    traj_v = filtra_traiettoria_basata_su_velocita(traj)
    traj_d = filtra_cambio_direzione(traj_v)
    traj_cm = converti_pixel_in_cm_relativo(traj_d, scala_cm_per_px, altezza_robot_cm)
    traj_cm_finale = filtra_fase_finale(traj_cm)

    # === Estrai punto finale e salva CSV
    x_finale_cm = traj_cm_finale[-1][0]
    dati_lancio = [altezza_robot_cm, inclinazione_gradi, pwm_motori, round(x_finale_cm, 2)]

    dataset_file = "traiettorie_volano.csv"
    prima_scrittura = not os.path.exists(dataset_file)

    with open(dataset_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        if prima_scrittura:
            writer.writerow(["altezza_robot_cm", "inclinazione_gradi", "pwm_motori", "x_atterraggio_cm"])
        writer.writerow(dati_lancio)

    print(f"[✅] Dati salvati nel dataset: {dataset_file}")

    # === Salva traiettoria in .npy ===
    os.makedirs("traiettorie_npy", exist_ok=True)
    nome_traiettoria = f"traiettorie_npy/H{altezza_robot_cm}_T{inclinazione_gradi}_PWM{pwm_motori}.npy"
    np.save(nome_traiettoria, traj_cm_finale)
    print(f"[💾] Traiettoria salvata in: {nome_traiettoria}")

    # === Salva grafico su file ===
    os.makedirs("grafici", exist_ok=True)
    X = traj_cm_finale[:, 0]
    Z = traj_cm_finale[:, 1]

    plt.figure(figsize=(8, 5))
    plt.plot(X, Z, 'ro-', label="Volano (in cm)")
    plt.scatter(0, altezza_robot_cm, c='green', label='Inizio')
    plt.scatter(X[-1], Z[-1], c='black', label='Fine')
    plt.xlabel("X [cm]")
    plt.ylabel("Z [cm] (da terra)")
    plt.title("Traiettoria volano (riferita al pavimento)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    nome_grafico = f"grafici/traiettoria_pwm{pwm_motori}_h{altezza_robot_cm}_theta{inclinazione_gradi}.png"
    plt.savefig(nome_grafico)
    plt.close()
    print(f"[📷] Grafico salvato in: {nome_grafico}")

else:
    print("[INFO] Nessuna traiettoria utile rilevata.")