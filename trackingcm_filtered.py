import cv2
import numpy as np
import matplotlib.pyplot as plt

# === PARAMETRI ===
video_path = "lancio_due.avi"
scala_cm_per_px = 1.0325  # << INSERISCI QUI LA TUA SCALA (cm/px)

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

# === Filtro su velocità iniziale/finale ===
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

# === Filtro su cambi di direzione ===
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

# === Filtro finale: volano si ferma ===
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

# === Conversione da pixel a cm, con origine mobile ===
def converti_pixel_in_cm_relativo(traiettoria_px, scala_cm_per_px):
    px = np.array(traiettoria_px, dtype=np.float32)
    origine = px[0]
    px_shifted = px - origine
    cm = px_shifted * scala_cm_per_px
    return cm

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

# === Applica i filtri e converti in cm ===
if len(trajectory_px) > 10:
    traj = np.array(trajectory_px)

    # Filtro velocità iniziale/finale
    traj_v = filtra_traiettoria_basata_su_velocita(traj)

    # Filtro cambi di direzione
    traj_d = filtra_cambio_direzione(traj_v)

    # Conversione a cm
    traj_cm = converti_pixel_in_cm_relativo(traj_d, scala_cm_per_px)

    # Filtro finale: fase di arresto
    traj_cm_finale = filtra_fase_finale(traj_cm)

    # === Visualizzazione finale ===
    X = traj_cm_finale[:, 0]
    Y = traj_cm_finale[:, 1]

    plt.figure(figsize=(8, 5))
    plt.plot(X, Y, 'ro-', label="Volano (in cm)")
    plt.scatter(0, 0, c='green', label='Inizio')
    plt.scatter(X[-1], Y[-1], c='black', label='Fine filtrata')
    plt.xlabel("X [cm]")
    plt.ylabel("Z [cm]")
    plt.title("Traiettoria del volano (coordinate reali)")
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
else:
    print("[INFO] Nessuna traiettoria utile rilevata.")