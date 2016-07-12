/************************************************************************
* Module for testing ability of Arduino to sent AT Commands to XBee		  *
************************************************************************/

#include <XBee.h>
#include <SoftwareSerial.h>

//Define SoftwareSerial TX/RX pins
uint8_t ssRX = 8; //Connect pin 8 to TX of usb-serial device
uint8_t ssTX = 9; //Connect pin 9 to RX of usb-serial device
SoftwareSerial nss(ssRX, ssTX);

XBee xbee = XBee();

uint8_t shCmd[] = {'S', 'H'}; //Serial high
uint8_t slCmd[] = {'S', 'L'}; //Serial low
uint8_t assocCmd[] = {'A', 'I'}; //Association status

AtCommandRequest atRequest = AtCommandRequest(shCmd);
AtCommandResponse atResponse = AtCommandResponse();

void setup()
{
	Serial.begin(9600);
	xbee.begin(Serial);
	nss.begin(9600);
  nss.println("Hello word!");
}

void loop()
{
	//Send SH
  atRequest.setCommand(shCmd);
	sendAtCommand();

	//Set command to SL
	atRequest.setCommand(slCmd);
	sendAtCommand();

	//Set command to AI
	atRequest.setCommand(assocCmd);
	sendAtCommand();

	delay(1000); //Wait a second and start over
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