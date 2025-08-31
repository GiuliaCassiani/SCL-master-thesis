#include <Servo.h>

// Oggetti Servo
Servo esc1;
Servo esc2;
Servo servoLauncher;     // Servo Parallax per il lancio
Servo servoTilt;         // Servo digitale per inclinazione

// Angoli launcher
const int angle_Charge_deg = 45;
const int angle_Release_deg = 115;

// Angoli inclinazione
const int tiltCenter_deg = 0;
const int tiltMax_deg = 10;  // massimo a +30° 

void setup() {
  // Attacca i pin
  esc1.attach(2);
  esc2.attach(3);
  servoLauncher.attach(10);  // Servo di lancio sul pin 10
  servoTilt.attach(6);       // Servo di inclinazione sul pin 6

  // 0. Posizione iniziale
  servoLauncher.write(angle_Charge_deg); // posizione di carica
  servoTilt.write(tiltCenter_deg);       // posizione centrale
  delay(500);

  // 1. Arma gli ESC a 1000 µs
  esc1.writeMicroseconds(1000);
  esc2.writeMicroseconds(1000);
  delay(5000); // Sicurezza

  // 2. Inclinazione a 20°
  servoTilt.write(tiltMax_deg);
  delay(1000); // Dai tempo al servo

  // 3. Avvia le ruote
  esc1.writeMicroseconds(1150);
  esc2.writeMicroseconds(1150);
  delay(2000); // Attendi 2 sec

  // 4. Lancio
  servoLauncher.write(angle_Release_deg);
  delay(500);
  servoLauncher.write(angle_Charge_deg);
  delay(1000);

  // 5. Riporta inclinazione al centro
  servoTilt.write(tiltCenter_deg);
  delay(500);

  // 6. Ferma le ruote
  esc1.writeMicroseconds(1000);
  esc2.writeMicroseconds(1000);
}

void loop() {
  // Nulla qui
}
