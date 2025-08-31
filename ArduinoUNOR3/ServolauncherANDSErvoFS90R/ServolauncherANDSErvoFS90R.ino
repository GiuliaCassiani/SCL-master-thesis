#include <Servo.h>

Servo motorRight;
Servo servoParallax; // Servo standard Parallax #900-00005

// Valore PWM per massima velocità antioraria (FS90R)
const int speedAntiorario = 180;

// Tempo per fare un giro completo (360°) in ms
const int rotazione360_ms = 550;

// Tempo di attesa tra le due sequenze
const int pausa_ms = 3000;

// Attesa prima che il Parallax si muova dopo i motori
const int attesaParallax_ms = 2000;

// Angoli per servo Parallax
const int angoloIniziale = 45;
const int angoloFinale = 115;

void setup() {
  
  motorRight.attach(10);
}

void loop() {
  // ---- Giro dei FS90R ----
 
  motorRight.write(speedAntiorario);
  delay(rotazione360_ms);

  // Ferma i motori

  motorRight.write(90);

  // Aspetta 2 secondi prima di muovere il Parallax
  delay(attesaParallax_ms);

  // ---- Solo ora attacchiamo il Parallax ----
  servoParallax.attach(6);
  servoParallax.write(angoloFinale);
  delay(1000);
  servoParallax.write(angoloIniziale);
  delay(1000);
  servoParallax.detach();  // disattiviamo il servo per evitare interferenze

  // Pausa prima della ripetizione
  delay(pausa_ms);
}


