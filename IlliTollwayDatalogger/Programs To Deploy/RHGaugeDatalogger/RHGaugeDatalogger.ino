/**********************************************************************
*                                                                     *
* Data Logging Software for Illinois Tollway Concrete Testing         *
* Written by Kanyon Edvall                                            *
*                                                                     *
* This program uses the Sensirion library to record temperature and   *
*   humidity of concrete at three heights. Each recording is written  *
*   to an on board SD card and transmitted wirelessly over serial.    *
*                                                                     *
* A real time clock module is used to time stamp all recorded data    *
*                                                                     *
**********************************************************************/
#include "RHGaugeDatalogger.h"

//Serial Debugging (Note that XBee uses serial print statements to communicate)
#define ENABLEDEBUG 1 //Default is 0, set 1 to enable (Disables XBee communication)

///////////////////////////////////////////////////////////////////////
// Initial Setup:                                                    //
//   Start and set RTC Module, check for error                       //
//   Starts serial communication at 9600 baud (default for Xbees)    //
//   Set columns for output text file                                //
///////////////////////////////////////////////////////////////////////
void setup()
{  
  sleepTime = 60000; //Time to sleep in MS DEFAULT 900000 (15min), for to testing

  //Pin mode for potentiometers
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);
  pinMode(A3, INPUT_PULLUP);
  pinMode(A4, INPUT_PULLUP);
  //LED pin
  pinMode(LEDPIN, OUTPUT);
 
  Serial.begin(9600); //Start serial communication at 9600 baud

  //Radio setup
  pinMode(XBEE_SLEEP, OUTPUT);
  digitalWrite(XBEE_SLEEP, LOW); //Set pin LOW to keep radio awake (HIGH puts radio to sleep)
  radio.setSerial(Serial); //Sets which serial the radio should use

  if (atCommand(xBeePin7, 1) && ENABLEDEBUG) 
    Serial.println("atCommand D7 failed with parameter 1"); //Set XBee (NOT Arduino) pin 7 off
  if (atCommand(xBeeSleepMode, 1) && ENABLEDEBUG)
    Serial.println("atCommand SM (Sleep Mode) failed with parameter 1"); //Set XBee sleep mode controlled by XBee (NOT Arduino) pin 9

  //Check RTC started correctly, display error if not
  if (!rtc.begin() && ENABLEDEBUG)
    Serial.println("Couldn't find RTC");

  rtc.adjust(DateTime(F(__DATE__), F(__TIME__))); //Set RTC to date & time this sketch was compiled

  SD.begin(CS); //Initialize SD card

  InitColSetup(); //Set up columns for output text file
} //End of setup function

///////////////////////////////////////////////////////////////////////
// Main Loop:                                                        //
//   Reads temperature and humidity from sensors                     //
//   Saves readings to SD card and transmits it wirelessly           //
///////////////////////////////////////////////////////////////////////
void loop() 
{
  if (ENABLEDEBUG)
    digitalWrite(LEDPIN, HIGH); //Turn on status LED
  digitalWrite(XBEE_SLEEP, LOW); //Set pin LOW to wake radio
  delay(1000); //Delay to allow serial output and radio to initialize after wake up

  //Reset variables for sensors 
  sensor.temperature1 = -40;
  sensor.temperature2 = -40;
  sensor.temperature3 = -40;

  sensor.humidity1 = -1;
  sensor.humidity2 = -1;
  sensor.humidity3 = -1;

  ReadData(); //Read from sensors

  RecordData(); //Record measurements

  //Transmit sensor data over serial
  if (ENABLEDEBUG)
    PrintDebug();
  else
    PrintVars();
  delay(1000); //Wait 1 second for serial print to complete

  //Enter low power state for sleepTime
  if (ENABLEDEBUG)
    digitalWrite(LEDPIN, LOW); //Turn off status LED
  digitalWrite(XBEE_SLEEP, HIGH); //Set pin HIGH to sleep radio
  sleep.pwrDownMode(); //Set sleep mode
  sleep.sleepDelay(sleepTime); //Sleep for specified time
} //End of main loop

///////////////////////////////////////////////////////////////////////
// Function: InitColSetup                                            //
// Set up columns for output text file                               //
///////////////////////////////////////////////////////////////////////
void InitColSetup()
{
  sdCard = SD.open("DataLog.txt", FILE_WRITE); //Open SD card for writing
  
  if (sdCard) //Check for correct open before attempting to write
  {
    sdCard.print("Year");
    sdCard.print(",");
    sdCard.print("Month");
    sdCard.print(",");
    sdCard.print("Day");
    sdCard.print(",");
    sdCard.print("Hour");
    sdCard.print(",");
    sdCard.print("Minute");
    sdCard.print(",");
    sdCard.print("Second");
    sdCard.print(",");
    sdCard.print("Line 1");
    sdCard.print(",");
    sdCard.print("Line 2");
    sdCard.print(",");
    sdCard.print("Line 3");
    sdCard.print(",");
    sdCard.print("Line 4");
    sdCard.print(",");
    sdCard.print("Line 5");
    sdCard.print(",");
    sdCard.print("Temp 1");
    sdCard.print(",");
    sdCard.print("Temp 2");
    sdCard.print(",");
    sdCard.print("Temp 3");
    sdCard.print(",");
    sdCard.print("Hum 1");
    sdCard.print(",");
    sdCard.print("Hum 2"); 
    sdCard.print(",");
    sdCard.print("Hum 3");
    sdCard.println(); 

    sdCard.close(); //Close SD card
  }
  else if (ENABLEDEBUG)
    Serial.println("Error opening SD card");
} //End of InitColSetup function

///////////////////////////////////////////////////////////////////////
// Function: ReadData                                                //
// Take all necessary measurements                                   //
///////////////////////////////////////////////////////////////////////
void ReadData()
{
  //Get current time from system
  now = rtc.now();

  //Read from potentiometers
  sensor.L1 = digitalRead(A0);
  sensor.L2 = digitalRead(A1);
  sensor.L3 = digitalRead(A2);
  sensor.L4 = digitalRead(A3);
  sensor.L5 = digitalRead(A4);

  //Read RH gauges with 1s delay in between each read
  tempSensor1.measure(&sensor.temperature1, &sensor.humidity1, &sensor.dewpoint1);
  delay(1000);
  tempSensor2.measure(&sensor.temperature2, &sensor.humidity2, &sensor.dewpoint2);
  delay(1000);
  tempSensor3.measure(&sensor.temperature3, &sensor.humidity3, &sensor.dewpoint3);
  delay(1000);
} //End of ReadData Function

///////////////////////////////////////////////////////////////////////
// Function: RecordData                                              //
// Record all read data to text file on SD card                      //
///////////////////////////////////////////////////////////////////////
void RecordData()
{
  //Open SD card for writing
  sdCard = SD.open("DataLog.txt", FILE_WRITE);

  //Ensure card opened for writing correctly
  if(sdCard) 
  {
    //Record current date/time
    sdCard.print(now.year(), DEC);
    sdCard.print(",");
    sdCard.print(now.month(), DEC);
    sdCard.print(",");
    sdCard.print(now.day(), DEC);
    sdCard.print(",");
    sdCard.print(now.hour(), DEC);
    sdCard.print(",");
    sdCard.print(now.minute(), DEC);
    sdCard.print(",");
    sdCard.print(now.second(), DEC);
    sdCard.print(",");

    //Record potentiometers
    sdCard.print(sensor.L1);
    sdCard.print(",");
    sdCard.print(sensor.L2);
    sdCard.print(",");
    sdCard.print(sensor.L3);
    sdCard.print(",");
    sdCard.print(sensor.L4);
    sdCard.print(",");
    sdCard.print(sensor.L5);
    sdCard.print(",");

    //Record RH gauge measurements
    sdCard.print(sensor.temperature1);
    sdCard.print(",");
    sdCard.print(sensor.temperature2);
    sdCard.print(",");
    sdCard.print(sensor.temperature3);
    sdCard.print(",");
    sdCard.print(sensor.humidity1);
    sdCard.print(",");
    sdCard.print(sensor.humidity2);
    sdCard.print(",");
    sdCard.print(sensor.humidity3);
    sdCard.println();

    //Wait to ensure correct write
    delay(500);

    //Close SD card
    sdCard.close();
  }
  else if (ENABLEDEBUG)
    Serial.println("Error opening SD card");
} //End of RecordData function

///////////////////////////////////////////////////////////////////////
// Function: PrintVars                                               //
// Transmits packet over serial                                      //
///////////////////////////////////////////////////////////////////////
void PrintVars()
{
  unsigned long uBufSize = sizeof(sensor);
  char pBuffer[uBufSize];

  memcpy(pBuffer, &sensor, uBufSize);

  for(unsigned int i = 0; i < uBufSize; i++)
    Serial.print(pBuffer[i]);
    
  Serial.println();
} //End of PrintVars function

///////////////////////////////////////////////////////////////////////
// Function: atCommand                                               //
// Function to issue control commands to XBee Radio                  //
///////////////////////////////////////////////////////////////////////
int atCommand( char *command, uint8_t param ) 
{
  // send local AT command
  AtCommandRequest req = AtCommandRequest((uint8_t *) command, (uint8_t *) &param, sizeof(uint8_t));
  radio.send(req);

  // receive response frame
  AtCommandResponse res = AtCommandResponse();
  if(radio.readPacket(500)) {                               // read packet from radio
     if(radio.getResponse().getApiId() == AT_RESPONSE) {    // right type?
       radio.getResponse().getAtCommandResponse(res);
       if(res.isOk()) {                                     // not an error?
         return 0;
       }
     }
  }

  // if we get here, return a failure
  return 1;
} //End of atCommand function

///////////////////////////////////////////////////////////////////////
// Function: PrintDebug                                              //
// Optional debug statements over serial. Set on/off flag above      //
///////////////////////////////////////////////////////////////////////
void PrintDebug()
{
  //These print statements should no longer be needed, just for debugging
  Serial.println();
  Serial.print("=======================================");
  Serial.print(sensor.L1);
  Serial.print(',');
  Serial.print(sensor.L2);
  Serial.print(',');
  Serial.print(sensor.L3);
  Serial.print(',');
  Serial.print(sensor.L4);
  Serial.print(',');
  Serial.print(sensor.L5);

  Serial.println(); 
  Serial.print("Temperature 1: ");
  Serial.print(sensor.temperature1);
  Serial.print(" C, Humidity 1: ");
  Serial.print(sensor.humidity1);
  Serial.print(" %, Dewpoint 1: ");
  Serial.print(sensor.dewpoint1); 
  Serial.print(" C");

  Serial.println();
  Serial.print("-------------------------------------");
  Serial.print("Temperature 2: ");
  Serial.print(sensor.temperature2);
  Serial.print(" C, Humidity 2: ");
  Serial.print(sensor.humidity2);
  Serial.print(" %, Dewpoint 2: ");
  Serial.print(sensor.dewpoint2);
  Serial.print(" C");

  Serial.println();
  Serial.print("-------------------------------------");
  Serial.print("Temperature 3: ");
  Serial.print(sensor.temperature3);
  Serial.print(" C, Humidity 3: ");
  Serial.print(sensor.humidity3);
  Serial.print(" %, Dewpoint 3: ");
  Serial.print(sensor.dewpoint3);
  Serial.print(" C");
  
  Serial.println("=======================================");
} //End of PrintDebug function