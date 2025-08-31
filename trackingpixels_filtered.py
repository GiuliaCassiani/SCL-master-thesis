import cv2
import numpy as np
import matplotlib.pyplot as plt

# === Parametri ===
video_path = "video_left.avi"

# === Background Subtractor ===
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)

# === Funzione per rilevare il volano ===
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

# === Funzione per filtrare traiettoria su base velocità ===
def filtra_traiettoria_basata_su_velocita(punti, soglia_min=5, soglia_max=80, finestra=3):
    punti = np.array(punti)
    if len(punti) < finestra + 2:
        return punti

    diffs = np.linalg.norm(np.diff(punti, axis=0), axis=1)

    # Trova inizio valido
    start_idx = 0
    for i in range(len(diffs) - finestra):
        if np.all((diffs[i:i+finestra] > soglia_min) & (diffs[i:i+finestra] < soglia_max)):
            start_idx = i
            break

    # Trova fine valida
    end_idx = len(punti)
    for i in range(len(diffs) - finestra, 0, -1):
        if np.all((diffs[i-finestra:i] > soglia_min) & (diffs[i-finestra:i] < soglia_max)):
            end_idx = i + 1
            break

    return punti[start_idx:end_idx]

# === (Opzionale) Filtro su cambi di direzione ===
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

# === Leggi video e applica tracking ===
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

# === Filtro finale sulla traiettoria ===
if len(trajectory_px) > 10:
    traj = np.array(trajectory_px)

    traj_v = filtra_traiettoria_basata_su_velocita(traj, soglia_min=5, soglia_max=80, finestra=3)
    traj_finale = filtra_cambio_direzione(traj_v, angolo_max_deg=45)  # opzionale

    # === Visualizzazione ===
    X = traj_finale[:, 0]
    Y = traj_finale[:, 1]

    plt.figure(figsize=(8, 5))
    plt.plot(X, Y, 'ro-', label="Volano (filtrato)")
    plt.scatter(X[0], Y[0], c='green', label='Inizio', zorder=5)
    plt.scatter(X[-1], Y[-1], c='black', label='Fine', zorder=5)
    plt.xlabel("Pixel X")
    plt.ylabel("Pixel Y")
    plt.title("Traiettoria del volano (pulita)")
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
else:
    print("[INFO] Nessuna traiettoria utile rilevata.")