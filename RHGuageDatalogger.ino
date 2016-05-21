/**********************************************************************
*                                                                     *
* Data Logging Software for Illinois Tollway Concrete Testing         *
* Written by Kanyon Edvall and Sachindra Dahal                        *
*                                                                     *
* This program uses the Sensirion library to record temperature and   *
*   humidity of concrete at three heights. Each recording is written  *
*   to an onboard SD card and transmitted wirelessly over serial.     *
*                                                                     *
* A real time clock module is used to timestamp all recorded data     *
*                                                                     *
**********************************************************************/
//Includes:
#include <Arduino.h>
#include <Sensirion.h>
#include <Wire.h> //RTClib depends on this
#include "RTClib.h"
#include "SD.h"
#include <SPI.h>
#include "LowPower.h"

//Serial Debugging (Note that XBee uses serial print statements to communicate)
#define ENABLEDEBUG 0 //Default is 0, set 1 to enable (Disables XBee communication)

//Not sure the point of this?
void error(char *str)
{
  Serial.print("error: ");
  Serial.println(str);

  while(1);
}

///////////////////////////////////////////////////////////////////////
// Initial Setup:                                                    //
//   Start and set RTC Module, check for error                       //
//   Starts serial communication at 9600 baud (default for Xbees)    //
//   Set columns for output text file                                //
///////////////////////////////////////////////////////////////////////
void setup ()
{ 
  //Check RTC started correctly, display error if not
  if (!rtc.begin() && ENABLEDEBUG)
    Serial.println("Couldn't find RTC");
 
  //Pin mode for potentiometers
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);
  pinMode(A3, INPUT_PULLUP);
  pinMode(A4, INPUT_PULLUP);
  //For LED
  pinMode(LEDPIN, OUTPUT);

  /* Shouldn't be needed, try without this
  pinMode(dataPin1, INPUT_PULLUP);
  pinMode(dataPin2, INPUT_PULLUP);
  pinMode(dataPin3, INPUT_PULLUP); */
  
  //Start serial communication at 9600 baud
  Serial.begin(9600);

  //Set RTC to date & time this sketch was compiled
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  lastRead = now.unixtime() - 900;

  //Initialize SD card
  SD.begin(CS);

  //Set up columns for output text file
  InitColSetup();
} //End of setup function

///////////////////////////////////////////////////////////////////////
// Main Loop:                                                        //
//   Reads temperature and humidity from sensors                     //
//   Saves readings to SD card and transmits it wirelessly           //
///////////////////////////////////////////////////////////////////////
void loop () 
{
  if ( (now.unixtime() - lastRead) >= 900)
  //15+ minutes have elasped, read sensors
  {
    //Read from sensors:
    ReadData();

    //Record measurements:
    RecordData();

    //Transmit sensor data over serial
    if (ENABLEDEBUG)
      PrintDebug();
    else
      Serial.print(packet);
    
    //Reset variables for sensors
    //Are you sure this is necessary?
    temperature1 = -40;
    temperature2 = -40;
    temperature3 = -40;

    humidity1 = 0;
    humidity2 = 0;
    humidity3 = 0;

    //Enter power down state for 8s with ADC and BOD module disabled
    if (ENABLEDEBUG)
      Serial.println ("Sleeping");     
    LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);  
  }
} //End of main loop

///////////////////////////////////////////////////////////////////////
// Function: InitColSetup                                            //
// Set up columns for output text file                               //
///////////////////////////////////////////////////////////////////////
void InitColSetup()
{
  //Open SD card for writing
  sdCard = SD.open("DataLog.txt", FILE_WRITE);
  //Check for correct open before attempting to write
  if (sdCard)
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

    //Close SD card
    sdCard.close();
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
  //Reset read counter
  lastRead = now.unixtime();

  //Get current time from system
  now = rtc.now();

  //Read from potentiometers
  sensor.L1 = digitalRead(A0);
  sensor.L2 = digitalRead(A1);
  sensor.L3 = digitalRead(A2);
  sensor.L4 = digitalRead(A3);
  sensor.L5 = digitalRead(A4);

  //Read RH guages with 1s delay in between each read
  tempSensor1.measure(&sensor.temperature1, &sensor.humidity1, &sensor.dewpoint1);
  delay (1000);
  tempSensor2.measure(&sensor.temperature2, &sensor.humidity2, &sensor.dewpoint2);
  delay (1000);
  tempSensor3.measure(&sensor.temperature3, &sensor.humidity3, &sensor.dewpoint3);
  delay (1000);
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

    //Record RH guage measurements
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
    delay(250);

    //Close SD card
    sdCard.close();
  }
  else if (ENABLEDEBUG)
    Serial.println("Error opening SD card");
} //End of RecordData function

///////////////////////////////////////////////////////////////////////
// Function: PrintDebug                                              //
// Optional debug statements over serial. Set on/off flag above      //
///////////////////////////////////////////////////////////////////////
void PrintDebug()
{
  //These print statements should no longer be needed, just for debugging
  Serial.println();
  Serial.print("=======================================");
  Serial.print(L1);
  Serial.print(',');
  Serial.print(L2);
  Serial.print(',');
  Serial.print(L3);
  Serial.print(',');
  Serial.print(L4);
  Serial.print(',');
  Serial.print(L5);

  Serial.println(); 
  Serial.print("Temperature 1: ");
  Serial.print(temperature1);
  Serial.print(" C, Humidity 1: ");
  Serial.print(humidity1);
  Serial.print(" %, Dewpoint 1: ");
  Serial.print(dewpoint1); 
  Serial.print(" C");

  Serial.println();
  Serial.print("-------------------------------------");
  Serial.print("Temperature 2: ");
  Serial.print(temperature2);
  Serial.print(" C, Humidity 2: ");
  Serial.print(humidity2);
  Serial.print(" %, Dewpoint 2: ");
  Serial.print(dewpoint2);
  Serial.print(" C");

  Serial.println();
  Serial.print("-------------------------------------");
  Serial.print("Temperature 3: ");
  Serial.print(temperature3);
  Serial.print(" C, Humidity 3: ");
  Serial.print(humidity3);
  Serial.print(" %, Dewpoint 3: ");
  Serial.print(dewpoint3);
  Serial.print(" C");
  
  Serial.println("=======================================");
} //End of PrintDebug function