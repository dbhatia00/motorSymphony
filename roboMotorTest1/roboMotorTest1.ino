#include <AccelStepper.h>

// Define pins for Motor 1 and Motor 2
#define stepPin1 3
#define dirPin1 2
#define stepPin2 5
#define dirPin2 4

// A few useful notes
int a = 440;
int b = 494;
int c = 262;
int d = 294;
int e = 330;
int f = 349;
int g = 392;

// Create stepper objects for each motor
AccelStepper motor1(AccelStepper::DRIVER, stepPin1, dirPin1);
AccelStepper motor2(AccelStepper::DRIVER, stepPin2, dirPin2);

unsigned long startMillis;
unsigned long currentMillis;

void setup() {
  // Set maximum speed and acceleration for both motors
  motor1.setMaxSpeed(1000);
  motor1.setAcceleration(500);
  motor2.setMaxSpeed(1000);
  motor2.setAcceleration(600);
}

void loop() {
  note(c, 400);
  pause(200);
  note(c, 400);
  pause(200);
  note(g, 400);
  pause(200);
  note(g, 400);
  pause(200);
  note(a, 400);
  pause(200);
  note(a, 400);
  pause(200);
  note(g, 400);
  pause(1000);
}

void note(int pitch, int duration) {
  startMillis = millis();
  // Set different speeds for both motors
  motor1.setSpeed(pitch);
  motor2.setSpeed(pitch);
  // Run motors for the specified duration
  while ((currentMillis = millis()) - startMillis < duration) {
    // Continuously run the motors
    motor1.runSpeed();
    motor2.runSpeed();
  }
}

void pause(int duration) {
  startMillis = millis();
  // Pause for the specified duration
  while ((currentMillis = millis()) - startMillis < duration) {
    motor1.stop();
    motor2.stop();
  }
  delay(10); // Small delay to ensure motors fully stop
}
