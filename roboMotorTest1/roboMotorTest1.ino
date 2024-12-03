#include <AccelStepper.h>

// Define pins for Motor 1, Motor 2, and Motor 3
#define stepPin1 3
#define dirPin1 2
#define stepPin2 5
#define dirPin2 4
#define stepPin3 9
#define dirPin3 8

// Create stepper objects for each motor
AccelStepper motor1(AccelStepper::DRIVER, stepPin1, dirPin1);
AccelStepper motor2(AccelStepper::DRIVER, stepPin2, dirPin2);
AccelStepper motor3(AccelStepper::DRIVER, stepPin3, dirPin3);

unsigned long startMillis;
unsigned long currentMillis;

// A few useful notes
int a = 440;
int b = 494;
int c = 262;
int d = 294;
int e = 330;
int f = 349;
int g = 392;

// Plan list containing {note, start time, end time} entries
int planList[][3] = {
  {c, 0, 400},
  {c, 400, 800},
  {g, 800, 1200},
  {g, 1200, 1600},
  {a, 1600, 2000},
  {a, 2000, 2400},
  {g, 2400, 2800}
};
int planListSize = sizeof(planList) / sizeof(planList[0]);

void setup() {
  // Set maximum speed and acceleration for all motors
  motor1.setMaxSpeed(1000);
  motor1.setAcceleration(500);
  motor2.setMaxSpeed(1000);
  motor2.setAcceleration(600);
  motor3.setMaxSpeed(1000);
  motor3.setAcceleration(600);
}

void loop() {
  for (int i = 0; i < planListSize; i++) {
    int pitch = planList[i][0];
    unsigned long startTime = planList[i][1];
    unsigned long endTime = planList[i][2];
    note(pitch, startTime, endTime);
    if (i < planListSize - 1) {
      pause(200);
    }
  }
  pause(1000); // Pause before restarting the loop
}

void note(int pitch, unsigned long startTime, unsigned long endTime) {
  unsigned long duration = endTime - startTime;
  startMillis = millis();
  // Set different speeds for all motors
  motor1.setSpeed(pitch);
  motor2.setSpeed(pitch);
  motor3.setSpeed(pitch);
  // Run motors for the specified duration
  while ((currentMillis = millis()) - startMillis < duration) {
    // Continuously run the motors
    motor1.runSpeed();
    motor2.runSpeed();
    motor3.runSpeed();
  }
}

void pause(int duration) {
  startMillis = millis();
  // Pause for the specified duration
  while ((currentMillis = millis()) - startMillis < duration) {
    motor1.stop();
    motor2.stop();
    motor3.stop();
  }
  delay(10); // Small delay to ensure motors fully stop
}
