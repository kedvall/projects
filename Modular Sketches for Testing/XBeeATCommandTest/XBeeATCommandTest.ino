#include <SoftwareSerial.h>

SoftwareSerial ss(11, 10); //RX, TX
byte hardwareByte;
byte softwareByte;

void setup()
{
	Serial.begin(9600);
	while (!Serial) { ;} //Wait for port to connect
	Serial.println("HW Serial Up!");
	delay(100);

	ss.begin(9600);
	Serial.println("SS Up!");
}

void loop()
{
	softwareByte = ss.read();

	hardwareByte = Serial.read();

	if (hardwareByte == 'C' || hardwareByte == 'c')
	{
		Serial.println("Sending CC...");
		delay(1500);
		ss.print("+++");
		delay(1500);
		Serial.print("Received ");
		Serial.println(ss.read());

		delay(50);

		ss.print("AT\r");
		Serial.print("Received ");
		Serial.println(ss.read());
	}
	else if (hardwareByte == 'D' || hardwareByte == 'd')
		Serial.println(softwareByte);
	else if (hardwareByte == 'N' || hardwareByte == 'n')
	{
		Serial.println("Setting Node Identifier (TestID)");
		ss.print("ATNI TestID\r");

		Serial.print("Received ");
		while (ss.available() > 0 && ss.read() != 53)
			Serial.println(char(ss.read()));
	}
	else if (hardwareByte == 'Q' || hardwareByte == 'q')
	{
		Serial.println("Querying Node Identifier...");
		ss.print("ATNI\r");

		Serial.print("Received ");
		Serial.println(ss.read());
	}
	else if (hardwareByte == 'S' || hardwareByte == 's')
		Serial.println("S Received");
}