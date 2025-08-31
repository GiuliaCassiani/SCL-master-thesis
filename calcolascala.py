# Inserisci la distanza reale tra i riferimenti
L_reale_cm = 666    # <-- MODIFICA QUI con la tua misura
dx_pixel = 602.03   # <-- MODIFICA QUI con il valore che hai ottenuto cliccando

scala_cm_per_px = L_reale_cm / dx_pixel
print(f"[✅] Scala cm/px: {scala_cm_per_px:.4f}")