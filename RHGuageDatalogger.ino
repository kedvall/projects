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

//Not sure the point of this, check and reformat latter
void error(char *str)
{
  Serial.print("error: ");
  Serial.println(str);

  while(1);
}

//Also not sure this variable's function
int i = 0;

///////////////////////////////////////////////////////////////////////
// Initial Setup:                                                    //
//   Start and set RTC Module, check for error                       //
//   Starts serial communication at 9600 baud (default for Xbees)    //
//   Set columns for output text file                                //
///////////////////////////////////////////////////////////////////////
void setup () 
{ 
  //Check RTC started correctly, display error if not
  if (!rtc.begin())
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
  lastRead = now.unixtime();

  //Initialize SD card
  SD.begin(CS);

  //Set up columns for output text file
  InitColSetup();
} //End of setup function

///////////////////////////////////////////////////////////////////////
// Main Loop:                                                        //
//   Reads temperature and humidity from sensors                     //
//   Saves readings to SD card and transmits it wirelessly           //               //
///////////////////////////////////////////////////////////////////////
void loop () 
{
  if ( (now.unixtime() - lastRead) >= 900) { 
    //15+ minutes have elasped, read sensors

    //Read from sensors:
    ReadData();

    //Record measurements:
    RecordData();

    
      




      Serial.println();

      
      




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
     
      Serial.println();
      
    
    Serial.println("=======================================");
    Serial.print("Temperature 1: ");
    Serial.print(temperature1);
    Serial.print(" C, Humidity 1: ");
    Serial.print(humidity1);
    Serial.print(" %, Dewpoint 1: ");
    Serial.print(dewpoint1);
    Serial.println(" C");
    delay (500);
  Serial.println("-------------------------------------");
    Serial.print("Temperature 2: ");
    Serial.print(temperature2);
    Serial.print(" C, Humidity 2: ");
    Serial.print(humidity2);
    Serial.print(" %, Dewpoint 2: ");
    Serial.print(dewpoint2);
    Serial.println(" C");

  delay (500);
  Serial.println("-------------------------------------");
    Serial.print("Temperature 3: ");
    Serial.print(temperature3);
    Serial.print(" C, Humidity 3: ");
    Serial.print(humidity3);
    Serial.print(" %, Dewpoint 3: ");
    Serial.print(dewpoint3);
    Serial.println(" C");
    
    Serial.println("=======================================");
      
    delay(2500);  

  temperature1 = -40;
  temperature2 = -40;
  temperature3 = -40;

  humidity1 = 0;
  humidity2 = 0;
  humidity3 = 0;
  //RH gauge END





      
      delay(900);
    
    
    } // if sdCard wala loop

  delay (3000);
   i = 0;
  Serial.println ("Sleeping"); 
  Serial.println ("------------");      

  digitalWrite(13,LOW);
  delay (1000);
  digitalWrite (13, HIGH);
  delay (1000);
  digitalWrite(13,LOW);
  delay (1000);
  digitalWrite (13, HIGH);
  delay (1000);
  digitalWrite(13,LOW);
  delay (1000);
  digitalWrite (13, HIGH);
  delay (1000);
  digitalWrite(13,LOW);
  delay (1000);
   }
   else {
          i++;
   //Enter power down state for 8 s with ADC and BOD module disabled
  LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);  
  }// SLEEP Loop

  
  } // void loops

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
  else 
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
  L1 = digitalRead(A0);
  L2 = digitalRead(A1);
  L3 = digitalRead(A2);
  L4 = digitalRead(A3);
  L5 = digitalRead(A4);

  //Read RH guages with 1s delay in between each read
  tempSensor1.measure(&temperature1, &humidity1, &dewpoint1);
  delay (1000);
  tempSensor2.measure(&temperature2, &humidity2, &dewpoint2);
  delay (1000);
  tempSensor3.measure(&temperature3, &humidity3, &dewpoint3);
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
    sdCard.print(L1);
    sdCard.print(",");
    sdCard.print(L2);
    sdCard.print(",");
    sdCard.print(L3);
    sdCard.print(",");
    sdCard.print(L4);
    sdCard.print(",");
    sdCard.print(L5);
    sdCard.print(",");

    //Record RH guage measurements
    sdCard.print(temperature1);
    sdCard.print(",");
    sdCard.print(temperature2);
    sdCard.print(",");
    sdCard.print(temperature3);
    sdCard.print(",");
    sdCard.print(humidity1);
    sdCard.print(",");
    sdCard.print(humidity2);
    sdCard.print(",");
    sdCard.print(humidity3);
    sdCard.println();

    //Wait to ensure corrent write
    delay(250);

    //Close SD card
    sdCard.close();
  }
  else
    Serial.println("Error opening SD card");
} //End of RecordData function

///////////////////////////////////////////////////////////////////////
// Function: TransmitData                                            //
// Transmit all recorded data wirelessly using XBee                  //
///////////////////////////////////////////////////////////////////////
void TransmitData()
{
  Serial.print(now.year(), DEC);
  Serial.print('/');
  Serial.print(now.month(), DEC);
  Serial.print('/');
  Serial.print(now.day(), DEC);
  Serial.print(' ');
  Serial.print(now.hour(), DEC);
  Serial.print(':');
  Serial.print(now.minute(), DEC);
  Serial.print(':');
  Serial.print(now.second(), DEC);
  Serial.println();

}