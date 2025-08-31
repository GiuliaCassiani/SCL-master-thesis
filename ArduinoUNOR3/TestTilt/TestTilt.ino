#include <Servo.h>

Servo servoTilt;

void setup() {
  servoTilt.attach(6);
  servoTilt.write(20); // prova inizialmente con 0 gradi
}

void loop() {
}
