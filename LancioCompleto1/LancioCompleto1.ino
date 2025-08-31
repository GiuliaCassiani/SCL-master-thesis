#include <Servo.h>

// Oggetti Servo
Servo esc1;
Servo esc2;
Servo servoFS90R;        // Servo FS90R (rotazione continua)
Servo servoLauncher;     // Servo Parallax per il lancio
Servo servoTilt;         // Servo per inclinazione

// Angoli launcher
const int angle_Charge_deg = 45;
const int angle_Release_deg = 135;

// Angoli inclinazione
const int tiltCenter_deg = 0;
const int tiltMax_deg = 10;

void setup() {
  // Attacca i pin
  esc1.attach(2);
  esc2.attach(3);
  servoTilt.attach(6);  // Servo inclinazione
  servoLauncher.attach(9);  // Servo Parallax
  

  // 0. Posizione iniziale
  servoLauncher.write(angle_Charge_deg); // posizione di carica
  servoTilt.write(tiltCenter_deg);       // posizione centrale
  delay(500);

  // 1. Arma gli ESC a 1000 µs
  esc1.writeMicroseconds(1000);
  esc2.writeMicroseconds(1000);
  delay(5000); // Sicurezza

  // 2. Avvia le ruote
  esc1.writeMicroseconds(1150);
  esc2.writeMicroseconds(1150);

  // 3. Dopo 1s → inclina a 10°
  delay(1000);
  servoTilt.write(tiltMax_deg);

  // 4. Dopo altri 2s → attiva FS90R per 550ms
  delay(2000);
  servoFS90R.attach(9); // FS90R collegato al pin 9
  servoFS90R.write(0); // Rotazione in un senso
  delay(800);
  servoFS90R.write(90); // Stop

  // 5. Dopo altri 3s → muove launcher 45→115→45
  delay(3000);
  servoLauncher.write(angle_Release_deg);
  delay(500);
  servoLauncher.write(angle_Charge_deg);

  // 6. Dopo 1s → spegne le ruote
  delay(1000);
  esc1.writeMicroseconds(1000);
  esc2.writeMicroseconds(1000);

  // 7. Dopo 2s → torna a inclinazione 0°
  delay(2000);
  servoTilt.write(tiltCenter_deg);
}

void loop() {
  // Nulla qui
}
