import cv2

# === PARAMETRI ===
camera_id = 0  # cambia se hai più webcam
output_file = "nono_lancio.avi"
frame_width = 640
frame_height = 360
fps = 30

cap = cv2.VideoCapture(camera_id)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
cap.set(cv2.CAP_PROP_FPS, fps)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

print("[INFO] Registrazione avviata. Premi 'q' per terminare.")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)
    cv2.imshow("Registrazione", cv2.resize(frame, (frame_width, frame_height)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
print(f"[✅] Registrazione terminata. Salvato in: {output_file}")