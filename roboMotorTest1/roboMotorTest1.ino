// Define pins
const int stepPin = 3; 
const int dirPin = 2; 

// Variables
int coun;
bool dir = 0;
int del;
int tempo = 120;
int oct = 1;

// Note frequencies
int a = 440;
int b = 494;
int c = 262;
int d = 294;
int e = 330;
int f = 349;
int g = 392;

// Note schedule: {note, start time, end time}
int noteSchedule[][3] = {
  {c, 0, 150},
  {c, 150, 300},
  {g, 300, 450},
  {g, 450, 600},
  {a, 600, 750},
  {a, 750, 900},
  {g, 900, 1200}
};
int scheduleSize = sizeof(noteSchedule) / sizeof(noteSchedule[0]);

void setup() {
  // Set pins as outputs
  pinMode(stepPin, OUTPUT); 
  pinMode(dirPin, OUTPUT);
}

void loop() {
  int currentTime = 0;

  // Iterate over the note schedule
  for (int i = 0; i < scheduleSize; i++) {
    int noteFreq = noteSchedule[i][0];
    int startTime = noteSchedule[i][1];
    int endTime = noteSchedule[i][2];
    int noteDuration = endTime - startTime;

    // Wait until the start time
    while (currentTime < startTime) {
      delay(1);
      currentTime++;
    }

    // Play the note
    note(noteFreq, noteDuration);

    // Update the current time
    currentTime += noteDuration;
  }

}

void note(int frequency, long duration) {
  // Calculate delay for note frequency
  del = 1000000 / (frequency * oct);
  dir = !dir;
  digitalWrite(dirPin, dir);

  // Calculate step count
  coun = duration / (2 * del);

  // Generate motor steps
  for (int x = 0; x < coun; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(del);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(del);
  }
}
