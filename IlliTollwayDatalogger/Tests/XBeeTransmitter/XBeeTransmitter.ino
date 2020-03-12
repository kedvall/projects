//Libraries to include:
#include <SPI.h>
#include <SD.h>
//#include <Sleep_n0m1.h>

#define BAUDRATE 9600
//unsigned long sleepTime;
//Sleep sleep;

void setup()
{
	//sleepTime = 7000; //Sleep 7 sec (7000ms) for testing

	//Set XBee sleep control pin as output and pull low to keep radio on
	pinMode(9, OUTPUT);
	digitalWrite(9, LOW);

	//Set data rate for hardware Serial prot
	Serial.begin(BAUDRATE);
	Serial.println("Transmitter1 up");
}

void loop()
{
	//digitalWrite(9, LOW);
  	//delay(500); //Delay for Serial to resume after sleeping

  String toPrint = "";
  toPrint += millis() / 1000;
  toPrint += " seconds, state: ";
  if (millis() < 3000)
    toPrint += "l";
  if (millis() > 3000 && millis() < 6000)
    toPrint += "h";
  if (millis() > 6000 && millis() < 9000)
    toPrint += "l";
  if (millis() > 9000 && millis() < 11000)
    toPrint += "h";
  if (millis() > 11000)
    toPrint += "l";

	//Send via XBee
	Serial.println(toPrint);
	delay(1000);

	//Power off XBee
	//digitalWrite(9, HIGH);

	//Power off Arduino
	//sleep.pwrDownMode(); //Set sleep mode
	//sleep.sleepDelay(sleepTime); //Sleep for specified time  
}
