import cv2
import numpy as np
import matplotlib.pyplot as plt

# === Parametri ===
video_path = "video_left.avi"

# Background subtractor per rilevare movimento
fgbg = cv2.createBackgroundSubtractorMOG2()

# Funzione per rilevare il centroide del volano

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

# === Apertura video ===
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

# === Filtra la traiettoria (rimuove punti iniziali/finali anomali) ===
if len(trajectory_px) > 10:
    traj = np.array(trajectory_px)

    # Calcola distanze tra punti consecutivi
    diffs = np.linalg.norm(np.diff(traj, axis=0), axis=1)
    min_dist = 2
    max_dist = 80
    window = 5

    start_idx = 0
    for i in range(len(diffs) - window):
        if np.all((diffs[i:i+window] > min_dist) & (diffs[i:i+window] < max_dist)):
            start_idx = i
            break

    traj_filtered = traj[start_idx:]

    # === Visualizzazione traiettoria filtrata ===
    X = traj_filtered[:, 0]
    Y = traj_filtered[:, 1]

    plt.figure(figsize=(8, 5))
    plt.plot(X, Y, 'ro-', label="Volano (filtrato)")
    plt.xlabel("Pixel X")
    plt.ylabel("Pixel Y")
    plt.title("Traiettoria del volano (in pixel)")
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
else:
    print("[INFO] Nessuna traiettoria utile rilevata.")