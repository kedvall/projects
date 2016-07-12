/********************************************************************
* Module for testing sleep functionality of Arduino (WITH XBee) 	*
********************************************************************/

#include <Sleep_n0m1.h>
#include <XBee.h>
#include <SoftwareSerial.h>

#define LEDPIN 13
#define XBEE_SLEEP 10

//Define SoftwareSerial TX/RX pins
uint8_t ssRX = 7; //Connect pin 8 to TX of usb-serial device
uint8_t ssTX = 8; //Connect pin 9 to RX of usb-serial device
SoftwareSerial nss(ssRX, ssTX);

uint8_t psCmd[] = {'D', '7'}; //Pin control
uint8_t smCmd[] = {'S', 'M'}; //Sleep mode

unsigned long sleepTime; //Amount of time in MS Arduino should sleep

Sleep sleep;
XBee xbee = XBee();

AtCommandRequest atRequest = AtCommandRequest(psCmd);
AtCommandResponse atResponse = AtCommandResponse();

void setup()
{
	sleepTime = 30000; //Sleep for 30 seconds
	pinMode(9, OUTPUT);
	pinMode(LEDPIN, OUTPUT);
	digitalWrite(XBEE_SLEEP, LOW); //Keep XBee awake

	Serial.begin(9600);
	xbee.begin(Serial);
	nss.begin(9600);

	Serial.println("XBee + Arduino Sleep module sketch starting...");

	//Send XBee pin setup
	sendAtCommand();

	//Set command to sleep mode
	atRequest.setCommand(smCmd);
	sendAtCommand();
}

void loop()
{
  digitalWrite(XBEE_SLEEP, LOW); //Wake XBee up
	delay(100); //Delay for Serial to resume after sleeping
	Serial.println("Executing code routine...");

	//Blink LED 5 times
	for (int i = 0; i < 6; i++)
	{
		digitalWrite(LEDPIN, HIGH);
		delay(500);
		digitalWrite(LEDPIN, LOW);
		delay(500);
	}

	//Go to sleep
	Serial.print("Sleeping for ");
	Serial.print(sleepTime / 1000);
	Serial.println(" seconds...");
	delay(100); //Ensure print completes before sleeping

	//Power off XBee
	digitalWrite(XBEE_SLEEP, HIGH);
	//Power off Arduino
	sleep.pwrDownMode(); //Set sleep mode
	sleep.sleepDelay(sleepTime); //Sleep for specified time
}

void sendAtCommand() {
  nss.println("Sending command to the XBee");

  // send the command
  xbee.send(atRequest);

  // wait up to 5 seconds for the status response
  if (xbee.readPacket(5000)) {
    // got a response!

    // should be an AT command response
    if (xbee.getResponse().getApiId() == AT_COMMAND_RESPONSE) {
      xbee.getResponse().getAtCommandResponse(atResponse);

      if (atResponse.isOk()) {
        nss.print("Command [");
        nss.print(atResponse.getCommand()[0]);
        nss.print(atResponse.getCommand()[1]);
        nss.println("] was successful!");

        if (atResponse.getValueLength() > 0) {
          nss.print("Command value length is ");
          nss.println(atResponse.getValueLength(), DEC);

          nss.print("Command value: ");
          
          for (int i = 0; i < atResponse.getValueLength(); i++) {
            nss.print(atResponse.getValue()[i], HEX);
            nss.print(" ");
          }

          nss.println("");
        }
      } 
      else {
        nss.print("Command return error code: ");
        nss.println(atResponse.getStatus(), HEX);
      }
    } else {
      nss.print("Expected AT response but got ");
      nss.print(xbee.getResponse().getApiId(), HEX);
    }   
  } else {
    // at command failed
    if (xbee.getResponse().isError()) {
      nss.print("Error reading packet.  Error code: ");  
      nss.println(xbee.getResponse().getErrorCode());
    } 
    else {
      nss.print("No response from radio");  
    }
  }
}