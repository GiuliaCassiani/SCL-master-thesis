#include <Servo.h>

Servo servoLauncher;  // Servo Parallax #900-00005 collegato al lanciatore

// Angoli da regolare in base al tuo sistema meccanico
const int angle_Charge_deg = 35;   // posizione di carica
const int angle_Release_deg = 135;  // posizione di rilascio

void setup() {
  servoLauncher.attach(9);         // collega il servo al pin digitale 10
  Serial.begin(9600);

  // Porta il servo nella posizione iniziale
  servoLauncher.write(angle_Charge_deg);
  delay(1000);
}

void loop() {
  // Carica il meccanismo
  servoLauncher.write(angle_Charge_deg);
  Serial.println("Carico...");
  delay(1000);  // attende 1 secondo

  // Lancia
  servoLauncher.write(angle_Release_deg);
  Serial.println("Lancio!");
  delay(2000);  // attende 2 secondi per completare il lancio
}
