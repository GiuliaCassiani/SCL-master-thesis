#include <Servo.h>
Servo servoLeft;
Servo servoRight;
void setup() {
  // Connect digital pins to servo
 servoLeft.attach(7);
 servoRight.attach(8);
 // Initial position
 servoLeft.write(60);
 servoRight.write(120);
 delay(1000);
}

void loop() {
  // Go to 180°
  servoLeft.write(180);
  servoRight.write(180);
  delay(1000);

  // Back to initial position
 servoLeft.write(60);
 servoRight.write(120);
 delay(1000);

}
