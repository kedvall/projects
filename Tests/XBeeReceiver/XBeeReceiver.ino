//declace a String to hold what we're inputting
String incomingString = "";

void setup() {
	//Setup pin 8 for LED
	pinMode(8, OUTPUT);
	digitalWrite(8, LOW);

	//initialise Serial communication on 9600 baud
	Serial.begin(9600);
	while(!Serial);
	Serial.println("HW Ready!");
}

void loop () {
	// Check if there's incoming serial data.
	if (Serial.available() > 0) {
		char ch = Serial.read();
    
	// show the byte on serial monitor
	Serial.print(ch);

	if (ch == 'h')
		digitalWrite(8, HIGH);

	if (ch == 'l')
		digitalWrite(8, LOW);

	Serial.flush();
	}
}
