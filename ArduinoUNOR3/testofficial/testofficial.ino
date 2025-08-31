#include <Servo.h>

// Oggetti Servo
Servo esc1;
Servo esc2;
Servo servoFS90R;        // Servo FS90R (rotazione continua)
Servo servoLauncher;     // Servo Parallax per il lancio
Servo servoTilt;         // Servo per inclinazione

// Angoli launcher
const int angle_Charge_deg = 45;
const int angle_Release_deg = 145;

// Angoli inclinazione
const int tiltCenter_deg = 0;
const int tiltMax_deg = 12;

void setup() {
  // === Arma gli ESC a 1000 µs ===
  esc1.attach(2);
  esc2.attach(3);
  esc1.writeMicroseconds(1000);
  esc2.writeMicroseconds(1000);
  delay(5000); // Sicurezza

  // === 1. Avvia le ruote (ESC) ===
  esc1.writeMicroseconds(1260);
  esc2.writeMicroseconds(1260);
  delay(1000);

  // === 2. Avvia FS90R per 800ms ===
  servoFS90R.attach(4);
  servoFS90R.write(0);     // Ruota orario
  delay(800);
  servoFS90R.write(90);    // Stop
  delay(200);
  servoFS90R.detach();
  delay(1000);

  // === 3. Inclina a 15° ===
  servoTilt.attach(6);
  servoTilt.write(tiltMax_deg);
  delay(1000);
  servoTilt.detach();

  // === 4. Muove launcher avanti e indietro ===
  servoLauncher.attach(9);
  servoLauncher.write(angle_Release_deg);
  delay(500);
  servoLauncher.write(angle_Charge_deg);
  delay(300);
  servoLauncher.detach();
  delay(1000);

  // === 5. Ferma gli ESC ===
  esc1.writeMicroseconds(1000);
  esc2.writeMicroseconds(1000);
  esc1.detach();
  esc2.detach();
  delay(1000);

  // === 6. Riporta Tilt a 0° ===
  servoTilt.attach(6);
  servoTilt.write(tiltCenter_deg);
  delay(500);
  servoTilt.detach();
}

void loop() {
  // Nulla qui
}
