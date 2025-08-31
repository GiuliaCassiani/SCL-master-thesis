#include <Servo.h>

Servo motorLeft;


// Valore PWM per massima velocità antioraria
const int speedAntiorario = 0;

// Tempo per fare un giro completo (360°) in ms
const int rotazione360_ms = 800;

// Tempo di attesa tra le rotazioni
const int pausa_ms = 3000;

void setup() {
  motorLeft.attach(7);
  

  // Primo giro (360° antiorario)
  motorLeft.write(0);
  
  delay(rotazione360_ms);

  // Stop
  motorLeft.write(90);
  
  delay(pausa_ms);

  // Secondo giro (360° antiorario)
  motorLeft.write(0);
 
  delay(rotazione360_ms);
// Stop
  motorLeft.write(90);
  
  delay(pausa_ms);

  // Secondo giro (360° antiorario)
  motorLeft.write(0);
 
  delay(rotazione360_ms);
  // Stop definitivo
  motorLeft.write(90);
   delay(pausa_ms);
  // Secondo giro (360° antiorario)
  motorLeft.write(0);
 
  delay(rotazione360_ms);
// Stop
  motorLeft.write(90);
  
  delay(pausa_ms);
   // Secondo giro (360° antiorario)
  motorLeft.write(0);
 
  delay(rotazione360_ms);
// Stop
  motorLeft.write(90);
  
  delay(pausa_ms);
   // Secondo giro (360° antiorario)
  motorLeft.write(0);
 
  delay(rotazione360_ms);
// Stop
  motorLeft.write(90);
  
  delay(pausa_ms);
   // Secondo giro (360° antiorario)
  motorLeft.write(0);
 
  delay(rotazione360_ms);
// Stop
  motorLeft.write(90);
  
  delay(pausa_ms);
   // Secondo giro (360° antiorario)
  motorLeft.write(0);
 
  delay(rotazione360_ms);
// Stop
  motorLeft.write(90);
  
  delay(pausa_ms);
   // Secondo giro (360° antiorario)
  motorLeft.write(0);
 
  delay(rotazione360_ms);
// Stop
  motorLeft.write(90);
  
  delay(pausa_ms);
   // Secondo giro (360° antiorario)
  motorLeft.write(0);
 
  delay(rotazione360_ms);
// Stop
  motorLeft.write(90);
  
  delay(pausa_ms);
}

void loop() {
  // Non fare nulla dopo le due rotazioni
}
