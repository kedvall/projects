/************************************************************************
* Module for testing sleep functionality of Arduino (without XBee)		*
************************************************************************/

#include <Sleep_m0m1.h>

Sleep sleep;
unsigned long sleepTime; //Var to stop amount of time in MS Arduino should sleep

void setup()
{
	sleepTime = 30000; //Sleep for 30 seconds
	pinMode(13, OUTPUT);
	Serial.begin(9600);
	Serial.print("Sleep module sketch starting...");
}

void loop()
{
	delay(100); //Delay for Serial to resume after sleeping
	Serial.println("Executing code routine...")

	//Blink LED 5 times
	for (i = 0; i < 6; i++)
	{
		digitalWrite(13, HIGH);
		delay(500);
		digitalWrite(13, LOW);
		delay(500);
	}

	//Go to sleep
	Serial.print("Sleeping for ");
	Serial.print(sleepTime / 1000);
	Serial.print(" seconds...");
	delay(100); //Ensure print completes before sleeping
	sleep.pwrDownMode(); //Set sleep mode
	sleep.sleepDelay(sleepTime); //Sleep for specified time
}