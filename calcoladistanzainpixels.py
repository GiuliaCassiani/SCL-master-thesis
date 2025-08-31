import cv2
import numpy as np

img = cv2.imread("frame_riferimento.jpg")
pts = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pts.append((x, y))
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Clicca i due riferimenti", img)

        if len(pts) == 2:
            p1, p2 = np.array(pts[0]), np.array(pts[1])
            dist_px = np.linalg.norm(p1 - p2)
            print(f"[📏] Distanza tra punti (in pixel): {dist_px:.2f}")
            print("Inserisci questa distanza nel prossimo script come 'dx_pixel'.")

cv2.imshow("Clicca i due riferimenti", img)
cv2.setMouseCallback("Clicca i due riferimenti", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()