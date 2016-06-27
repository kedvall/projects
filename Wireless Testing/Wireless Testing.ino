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
#define LEDPIN 13 //Pin for built in LED
#define MAXSAMPLES 10 //Number of samples to take each reading
#define PRINTDELAY 1000 //Delay between sending H and L to toggle LED (in milliseconds)
//Functionality Selection: Set 1 for transmitting mode, 0 for receiving mode
#define MODESELECT 1 //Defualt is 1 (transmitting mode)

//Variables
int serialData; //Variable to store incoming serial data
int sample; //Current sample number 
float sum; //Sum of current samples

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
    pinMode(LEDPIN, OUTPUT); //Set LED pin to output
} //End of setup function

///////////////////////////////////////////////////////////////////////
// Main control loop:                                                //
//   If MODESELECT is set to 1 (transmit mode):                      //
//     Send 'H', wait for delay specified above, then send 'L'       //
//   If MODESELECT is set to 0 (receive mode):                       //
//     Check incoming Serial data for 'H' or 'L'. If either is       //
//     received, toggle LED state respectively                       //
///////////////////////////////////////////////////////////////////////
void loop()
{
  if (MODESELECT) //Mode is set to transmitting
  {
    Serial.print('H'); //Print H over serial (toggle LED on)
    delay(PRINTDELAY); //Wait for specified delay

    Serial.print('L'); //Print L over serial (toggle LED off)
    delay(PRINTDELAY); //Wait again for specified delay

    Serial.print(ReadVoltage());
    delay(PRINTDELAY);
  }
  
  else //Mode is set to receiving
  {
    //Check for incoming serial data
    if (Serial.available() > 0) 
    {
      //Read oldest byte in the serial buffer and store it as int (ASCII is converted)
      serialData = Serial.read();
      //If it's an H, turn on the LED:
      if (serialData == 'H' || serialData == 'h')
        digitalWrite(LEDPIN, HIGH);
      //If it's an L, turn off the LED:
      else if (serialData == 'L' || serialData == 'l')
        digitalWrite(LEDPIN, LOW);
      //If it's anything else (voltage reading, print it)
      else
      {
        Serial.print('Voltage: ');
        Serial.print(serialData);
      }
    }
  }
} //End of main loop

///////////////////////////////////////////////////////////////////////
// Function: ReadVoltage                                             //
// Sample voltage readings of battery and return voltage             //
///////////////////////////////////////////////////////////////////////
float ReadVoltage()
{
  for (sample = 0; sample < MAXSAMPLES; sample++)
  {
    sum += analogRead(A2);
    delay(10);
  }
  sum = 0;

  return (sum / MAXSAMPLES);

  /* 
  Not sure the point of this code. You can add it back in if you need it
  voltage = ((float)sum / (float)NUM_SAMPLES * 5.18) / 1024.0;
  Serial.print(voltage * 5.99);
  */
}