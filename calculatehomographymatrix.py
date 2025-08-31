# === calcola_omografia.py ===
import cv2
import numpy as np

image_path = "frame_foglio.jpg"  # Frame con foglio ben visibile
output_file = "homography_matrix.npy"

# === Carica immagine ===
img = cv2.imread(image_path)
img_resized = cv2.resize(img, (960, 540))  # Riduci per visualizzazione
scale_x = img.shape[1] / 960
scale_y = img.shape[0] / 540
clone = img_resized.copy()
points = []

# === Clicca 4 punti ===
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            real_x = int(x * scale_x)
            real_y = int(y * scale_y)
            points.append([real_x, real_y])
            cv2.circle(clone, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow("Seleziona 4 punti (in senso orario)", clone)

cv2.imshow("Seleziona 4 punti (in senso orario)", clone)
cv2.setMouseCallback("Seleziona 4 punti (in senso orario)", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

if len(points) != 4:
    print("[ERRORE] Devi selezionare esattamente 4 punti.")
    exit()

pts_pixel = np.array(points, dtype=np.float32)

# === Inserisci coordinate reali corrispondenti in cm ===
# Esempio: foglio A4 orizzontale 30x21 cm (modifica se serve)
pts_real = np.array([
    [0, 21],     # angolo in alto a sinistra
    [30, 21],    # angolo in alto a destra
    [30, 0],   # in basso a destra
    [0, 0]     # in basso a sinistra
], dtype=np.float32)

# === Calcola omografia ===
H, _ = cv2.findHomography(pts_pixel, pts_real)
np.save(output_file, H)

print("[✅] Matrice omografica salvata in:", output_file)