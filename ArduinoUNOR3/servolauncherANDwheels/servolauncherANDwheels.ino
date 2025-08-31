#include <Servo.h>

// Oggetti Servo
Servo esc1;
Servo esc2;
Servo servoLauncher;  // Servo Parallax per il lancio

// Angoli launcher
const int angle_Charge_deg = 185;
const int angle_Release_deg = 125;

void setup() {
  // Attacca i pin
  esc1.attach(2);
  esc2.attach(3);
  servoLauncher.attach(9); // Collega il servo Parallax al pin 10

  // 0. Posizione iniziale del launcher (carica)
  servoLauncher.write(angle_Charge_deg);
  delay(500);

  // 1. Arma gli ESC a 1000 µs (minimo)
  esc1.writeMicroseconds(1000);
  esc2.writeMicroseconds(1000);
  delay(5000); // Tempo per arming (sicurezza)

  // 2. Avvia le ruote a velocità media
  esc1.writeMicroseconds(1200);
  esc2.writeMicroseconds(1200);

  // 3. Aspetta 2 secondi prima del lancio
  delay(3000);

  // 4. Aziona il servo launcher per il lancio
  servoLauncher.write(angle_Release_deg); // Lancio
  delay(500);                             // Attendi il movimento
  servoLauncher.write(angle_Charge_deg);  // Ritorna in carica
  delay(500);

  // 5. Ferma le ruote
  esc1.writeMicroseconds(1000);
  esc2.writeMicroseconds(1000);
}

void loop() {
  // Nulla qui, esecuzione una tantum
}
