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

// Plan list containing {frequency, start time, end time} entries
int planList[][3] = {
  {146.83, 0, 75},
  {146.83, 150, 224},
  {146.83, 452, 527},
  {146.83, 754, 829},
  {146.83, 904, 979},
  {783.99, 1206, 1281},
  {196.00, 1809, 1884},
  {196.00, 2411, 2486},
  {164.81, 2863, 2938},
  {130.81, 3315, 3390},
  {174.61, 3768, 3843},
  {196.00, 4070, 4145},
  {185.00, 4372, 4447},
  {174.61, 4522, 4597},
  {164.81, 4825, 4899},
  {261.63, 4975, 5050},
  {329.63, 5200, 5277},
  {349.23, 5427, 5502},
  {293.66, 5729, 5804},
  {329.63, 5879, 5954},
  {261.63, 6181, 6256},
  {220.00, 6481, 6556},
  {246.94, 6634, 6709},
  {196.00, 6784, 6859},
  {196.00, 7236, 7311},
  {164.81, 7688, 7763},
  {130.81, 8140, 8215},
  {174.61, 8593, 8668},
  {196.00, 8895, 8970},
  {185.00, 9195, 9270},
  {174.61, 9347, 9422},
  {164.81, 9647, 9722},
  {261.63, 9799, 9875},
  {329.63, 10025, 10100},
  {349.23, 10252, 10327},
  {293.66, 10552, 10627},
  {329.63, 10704, 10779},
  {261.63, 11004, 11079},
  {220.00, 11306, 11381},
  {246.94, 11456, 11531},
  {196.00, 11609, 11684},
  {130.81, 12061, 12136},
  {783.99, 12361, 12436},
  {196.00, 12513, 12588},
  {698.46, 12663, 12738},
  {622.25, 12813, 12888},
  {261.63, 12965, 13040},
  {659.26, 13115, 13190},
  {174.61, 13265, 13340},
  {415.30, 13418, 13493},
  {440.00, 13568, 13643},
  {261.63, 13718, 13793},
  {261.63, 13870, 13945},
  {440.00, 14020, 14095},
  {174.61, 14170, 14245},
  {587.33, 14320, 14397},
  {130.81, 14472, 14547},
  {783.99, 14772, 14850},
  {164.81, 14924, 15000},
  {698.46, 15075, 15149},
  {622.25, 15225, 15302},
  {196.00, 15377, 15452},
  {261.63, 15527, 15602},
  {1046.50, 15829, 15904},
  {1046.50, 16129, 16206},
  {1046.50, 16281, 16356},
  {196.00, 16581, 16659},
  {130.81, 16884, 16959},
  {783.99, 17186, 17261},
  {196.00, 17336, 17411},
  {698.46, 17486, 17563},
  {622.25, 17638, 17713},
  {261.63, 17788, 17863},
  {659.26, 17938, 18015},
  {174.61, 18090, 18165},
  {415.30, 18240, 18315},
  {440.00, 18390, 18468},
  {261.63, 18543, 18618},
  {261.63, 18693, 18768},
  {440.00, 18843, 18920},
  {174.61, 18995, 19070},
  {587.33, 19145, 19220},
  {130.81, 19295, 19372},
  {207.65, 19597, 19672},
  {233.08, 20050, 20125},
  {523.25, 20502, 20577},
  {196.00, 20954, 21029},
  {196.00, 21104, 21181},
  {130.81, 21406, 21481},
  {130.81, 21709, 21784},
  {783.99, 22009, 22086},
  {196.00, 22161, 22236},
  {698.46, 22311, 22386},
  {622.25, 22461, 22538},
  {261.63, 22613, 22688},
  {659.26, 22763, 22838},
  {174.61, 22913, 22990},
  {415.30, 23065, 23140},
  {440.00, 23215, 23290},
  {261.63, 23365, 23443},
  {261.63, 23518, 23593},
  {440.00, 23668, 23743},
  {174.61, 23818, 23895},
  {587.33, 23970, 24045},
  {130.81, 24120, 24195},
  {783.99, 24422, 24497},
  {164.81, 24572, 24647},
  {698.46, 24722, 24799},
  {622.25, 24875, 24950},
  {196.00, 25025, 25099},
  {261.63, 25174, 25252},
  {1046.50, 25477, 25552},
  {1046.50, 25779, 25854},
  {1046.50, 25929, 26004},
  {196.00, 26231, 26306},
  {130.81, 26531, 26609},
  {783.99, 26834, 26909},
  {196.00, 26984, 27061},
  {698.46, 27136, 27211},
  {622.25, 27286, 27361},
  {261.63, 27436, 27513},
  {659.26, 27588, 27663},
  {174.61, 27738, 27813},
  {415.30, 27888, 27965},
  {440.00, 28040, 28115},
  {261.63, 28190, 28265},
  {261.63, 28340, 28415},
  {440.00, 28493, 28568},
  {174.61, 28643, 28718},
  {587.33, 28793, 28868},
  {130.81, 28945, 29020},
  {207.65, 29245, 29320},
  {233.08, 29697, 29772},
  {261.63, 30150, 30224},
  {196.00, 30602, 30677},
  {196.00, 30754, 30829},
  {130.81, 31054, 31129},
  {103.83, 31356, 31431},
  {523.25, 31506, 31581},
  {155.56, 31809, 31884},
  {523.25, 32111, 32186},
  {207.65, 32261, 32336},
  {196.00, 32563, 32638},
  {523.25, 32713, 32788},
  {130.81, 33015, 33090},
  {392.00, 33165, 33240},
  {98.00, 33468, 33543},
  {103.83, 33768, 33843},
  {523.25, 33920, 33995},
  {155.56, 34220, 34295},
  {523.25, 34522, 34597},
  {207.65, 34672, 34747},
  {659.26, 34824, 34900},
  {196.00, 34975, 35050},
  {130.81, 35427, 35502},
  {98.00, 35879, 35954},
  {103.83, 36181, 36256},
  {523.25, 36331, 36406},
  {155.56, 36634, 36709},
  {523.25, 36934, 37009},
  {207.65, 37086, 37161},
  {196.00, 37386, 37461},
  {523.25, 37538, 37613},
  {130.81, 37838, 37913},
  {392.00, 37990, 38065},
  {98.00, 38290, 38365},
  {146.83, 38593, 38668},
  {146.83, 38743, 38818},
  {146.83, 39045, 39120},
  {146.83, 39347, 39422},
  {146.83, 39497, 39572},
  {783.99, 39800, 39875},
  {196.00, 40402, 40477},
  {196.00, 41004, 41079},
  {164.81, 41456, 41531},
  {130.81, 41909, 41984},
  {174.61, 42361, 42436},
  {196.00, 42663, 42738},
  {185.00, 42963, 43040},
  {174.61, 43115, 43190},
  {164.81, 43415, 43493},
  {261.63, 43568, 43643},
  {329.63, 43793, 43868},
  {349.23, 44020, 44095},
  {293.66, 44320, 44397},
  {329.63, 44472, 44547},
  {261.63, 44772, 44849},
  {220.00, 45074, 45150},
  {246.94, 45224, 45302},
  {196.00, 45377, 45452},
  {196.00, 45829, 45904},
  {164.81, 46281, 46356},
  {130.81, 46734, 46809},
  {174.61, 47186, 47261},
  {196.00, 47486, 47563},
  {185.00, 47788, 47863},
  {174.61, 47938, 48015},
  {164.81, 48240, 48315},
  {261.63, 48390, 48468},
  {329.63, 48618, 48693},
  {349.23, 48843, 48920},
  {293.66, 49145, 49220},
  {329.63, 49295, 49372},
  {261.63, 49597, 49672},
  {220.00, 49900, 49974},
  {246.94, 50050, 50125},
  {196.00, 50199, 50277},
  {130.81, 50652, 50729},
  {523.25, 50804, 50879},
  {185.00, 51104, 51181},
  {196.00, 51256, 51331},
  {261.63, 51556, 51634},
  {174.61, 51859, 51934},
  {698.46, 52009, 52086},
  {174.61, 52161, 52236},
  {698.46, 52311, 52386},
  {261.63, 52461, 52538},
  {261.63, 52613, 52688},
  {174.61, 52763, 52838},
  {146.83, 53065, 53140},
  {880.00, 53215, 53290},
  {880.00, 53443, 53518},
  {174.61, 53518, 53593},
  {196.00, 53668, 53743},
  {783.99, 53818, 53895},
  {246.94, 53970, 54045},
  {698.46, 54045, 54120},
  {196.00, 54270, 54347},
  {523.25, 54422, 54497},
  {196.00, 54572, 54647},
  {440.00, 54722, 54800},
  {261.63, 54875, 54949},
  {261.63, 55025, 55099},
};


int planListSize = sizeof(planList) / sizeof(planList[0]);

void setup() {
  // Set maximum speed and acceleration for all motors
  motor1.setMaxSpeed(1000);
  motor1.setAcceleration(600);
  motor2.setMaxSpeed(1000);
  motor2.setAcceleration(600);
  motor3.setMaxSpeed(1000);
  motor3.setAcceleration(600);
}

void loop() {
  int counter = 0;

  for (int i = 0; i < planListSize; i++) {
    int pitch = planList[i][0];
    unsigned long startTime = planList[i][1];
    unsigned long endTime = planList[i][2];
    unsigned long nextStartTime = (i + 1 < planListSize) ? planList[i + 1][1] : 0;
    note(pitch, startTime, endTime, counter);

    // Calculate pause duration based on the gap to the next note
    if (nextStartTime > endTime) {
      unsigned long restDuration = nextStartTime - endTime;
      pause(restDuration);
    }

    counter++;
  }
  pause(500); // Pause before restarting the loop
}

void note(int pitch, unsigned long startTime, unsigned long endTime, unsigned int counter) {
  unsigned long duration = endTime - startTime;
  startMillis = millis();

  // Depending on which motor's turn it is
  switch (counter % 3){
    case 0:
      motor1.setSpeed(pitch);
      break;
    case 1:
      motor2.setSpeed(pitch);
      break;
    case 2:
      motor3.setSpeed(pitch);
      break;
  }

  // Run motors for the specified duration
  while ((currentMillis = millis()) - startMillis < duration) {
    // Continuously run the motors
    switch (counter % 3){
      case 0:
        motor1.runSpeed();
        break;
      case 1:
        motor2.runSpeed();
        break;
      case 2:
        motor3.runSpeed();
        break;
    }
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