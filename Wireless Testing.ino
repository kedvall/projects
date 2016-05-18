/**********************************************************************
*                                                                     *
* Wireless Communication Test for Xbees                               *
* Written by Kanyon Edvall                                            *
*                                                                     *
* This program tests communication between two Xbees by sending or    *
*   or receiving data. Both sending and reveiving functionality is    *
*   included and can be togged by a variable below.                   *
*                                                                     *
**********************************************************************/
//Defines
#define PRINTDELAY 1000 //Delay between sending H and L to toggle LED (in milliseconds)
//Functionality Selection: Set 1 for transmitting mode, 0 for receiving mode
#define MODESELECT 1 //Defualt is 1 (transmitting mode)

//Variables
const int ledPin = 13; //Pin for built in LED
int serialData; //Variable to store incoming serial data

///////////////////////////////////////////////////////////////////////
// Initial Setup:                                                    //
//   Starts serial communication at 9600 baud (default for Xbees)    //
//   Optionally sets pinMode (if receive functionality is used)      //
///////////////////////////////////////////////////////////////////////
void setup()
{
  //Start serial communication
  Serial.begin(9600);

  if (!MODESELECT)
    pinMode(ledPin, OUTPUT); //Set LED pin to output
} //End of setup function

///////////////////////////////////////////////////////////////////////
// Main control loop:                                                //
//   If MODESELECT is set to 1 (transmit mode):                      //
//     Send 'H', wait for delay specified above, then send 'L'       //
//   If MODESELECT is set to 0 (receive mode):                       //
//     Check incoming Serial data for 'H' or 'L'. If either is       //
//     received, toggle LED state respectively                       //
///////////////////////////////////////////////////////////////////////
void loop() {
  if (MODESELECT) //Mode is set to transmitting
  {
    Serial.print('H'); //Print H over serial (toggle LED on)
    delay(PRINTDELAY); //Wait for specified delay

    Serial.print('L'); //Print L over serial (toggle LED off)
    delay(PRINTDELAY); //Wait again for specified delay
  }
  
  else //Mode is set to receiving
  {
    //Check for incoming serial data
    if (Serial.available() > 0) {
      //Read oldest byte in the serial buffer and store it as int (ASCII is converted)
      serialData = Serial.read();
      //If it's an H, turn on the LED:
      if (incomingByte == 'H' || incomingByte == 'h')
        digitalWrite(ledPin, HIGH);
      //If it's an L, turn off the LED:
      if (incomingByte == 'L' || incomingByte == 'l')
        digitalWrite(ledPin, LOW);
    }
  }
} //End of main loop