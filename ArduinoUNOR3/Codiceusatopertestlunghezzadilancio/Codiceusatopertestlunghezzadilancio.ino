#include <Servo.h>

// Oggetti Servo
Servo esc1;
Servo esc2;


void setup() {
  // Attacca tutti i pin
  esc1.attach(2);
  esc2.attach(3);

   // 1. Arm ESC a 1000 µs (MIN)
  esc1.writeMicroseconds(1000);
  esc2.writeMicroseconds(1000);
  delay(5000); // Più sicuro per arming

  // 2. Avvio ESC a 1600 µs
  esc1.writeMicroseconds(1150);
  esc2.writeMicroseconds(1150);

  // 3. Attendi 3 secondi prima di azionare i servo
  delay(3000);

  // 5. Aspetta altri 3 secondi
  delay(3000);

  // 6. Ferma gli ESC
  esc1.writeMicroseconds(1000);
  esc2.writeMicroseconds(1000);
}

void loop() {
  // Niente qui
}
