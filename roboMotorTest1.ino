const int dirPin = 2;
const int stepPin = 3;
const int stepsPerRevolution = 200;

void setup()
{
	// Start Serial Monitor
	Serial.begin(9600);
	
	// Declare pins as Outputs
	pinMode(stepPin, OUTPUT);
	pinMode(dirPin, OUTPUT);

	Serial.println("Motor setup complete.");
}

void loop()
{
	// Set motor direction clockwise
	digitalWrite(dirPin, HIGH);
	Serial.println("Direction: Clockwise");
	
	// Spin motor slowly
	Serial.println("Starting slow spin.");
	for (int x = 0; x < stepsPerRevolution; x++)
	{
		digitalWrite(stepPin, HIGH);
		delayMicroseconds(2000);
		digitalWrite(stepPin, LOW);
		delayMicroseconds(2000);

		// Optional: print each step for detailed debugging
		// Serial.print("Step: "); Serial.println(x);
	}
	Serial.println("Slow spin complete. Waiting...");

	delay(1000); // Wait a second
	
	// Set motor direction counterclockwise
	digitalWrite(dirPin, LOW);
	Serial.println("Direction: Counterclockwise");

	// Spin motor quickly
	Serial.println("Starting fast spin.");
	for (int x = 0; x < stepsPerRevolution; x++)
	{
		digitalWrite(stepPin, HIGH);
		delayMicroseconds(1000);
		digitalWrite(stepPin, LOW);
		delayMicroseconds(1000);

		// Optional: print each step for detailed debugging
		// Serial.print("Step: "); Serial.println(x);
	}
	Serial.println("Fast spin complete. Waiting...");

	delay(1000); // Wait a second
}
