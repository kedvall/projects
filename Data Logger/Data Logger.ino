/****************************************************************
* Data Logger.ino - Fully Featured data logging program 		*
* Written by Kanyon Edvall 										*
* 																*
* Records data from temperature sensors and transmits it 		*
* wirelessly back to upload hub 								*
****************************************************************/

//Included libraries
#include <Sensirion.h>
#include <Wire.h> //RTClib needs this
#include <SPI.h>
#include <SD.h>
#include <Sleep_n0m1.h>

#define ENDEBUG 0 //Variable to determine whether to print debug statements. 1 = TRUE, 0 = FALSE

//Pin Setup
const int chipSelect = 4;
const uint8_t clockPin1 = 2;
const uint8_t clockPin2 = 4;
const uint8_t clockPin3 = 6;
const uint8_t dataPin1 = 3;
const uint8_t dataPin2 = 5;
const uint8_t dataPin3 = 7;

#define XBEE_SLEEP 9

//Objects and vars
Sensirion Sensor1 = Sensirion(dataPin1, clockPin1);
Sensirion Sensor2 = Sensirion(dataPin2, clockPin2);
Sensirion Sensor3 = Sensirion(dataPin3, clockPin3);
RTC_DS1307 rtc; //For real time clock module
DateTime now; //Var to store time stamp
Sleep sleep;
unsigned long sleepTime; //Amount of time in MS Arduino should sleep

//Create struct to store data to be transmitted
struct dataPacket
{
  //Sensirion variable setup:
  float temp1;
  float humid1;
  float dew1;

  float temp2;
  float humid2;
  float dew2;

  float temp3;
  float humid3;
  float dew3;

  long unsigned int reads = 0;
} sensor;


///////////////////////////////////////////////////////////////////////
// Initial Setup:                                                    //
//   Start and set RTC Module, check for error                       //
//   Starts serial communication at 9600 baud (default for Xbees)    //
//   Set columns for output text file                                //
///////////////////////////////////////////////////////////////////////
void setup()
{
  pinMode(XBEE_SLEEP, OUTPUT);
  digitalWrite(XBEE_SLEEP, LOW);

  sleepTime = 900000; //Sleep for 15 minutes, change to something like 7 sec (7000ms) for testing

  //Start serial communication at 9600 baud
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  //Check if RTC started
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while(1);
  }

  //Ensure RTC is running and adjust time
  if (! rtc.isrunning()) {
    Serial.println("RTC is NOT running!");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  Serial.print("Initializing SD card...");

  //Check if card is present and can be initialized
  if (!SD.begin(chipSelect))
  {
    Serial.println("Card failed to initialize or is not present");
    return;
  }
  Serial.println("Card successfully initialized");
  Serial.println("");

  Serial.println("Recording Data:");
  setupCol();
}


///////////////////////////////////////////////////////////////////////
// Main Loop:                                                        //
//   Reads temperature and humidity from sensors                     //
//   Saves readings to SD card and transmits it wirelessly           //
///////////////////////////////////////////////////////////////////////
void loop()
{
  delay(100); //Delay for Serial to resume after sleeping

  //Reset variables for sensors 
  sensor.temp1 = -40;
  sensor.temp2 = -40;
  sensor.temp3 = -40;
  sensor.humidity1 = -1;
  sensor.humidity2 = -1;
  sensor.humidity3 = -1;

  //Get current time from system
  now = rtc.now();

  //Read RH gauges with 1s delay in between each read
  Sensor1.measure(&sensor.temp1, &sensor.humid1, &sensor.dew1);
  delay(1000);
  Sensor2.measure(&sensor.temp2, &sensor.humid2, &sensor.dew2);
  delay(1000);
  Sensor3.measure(&sensor.temp3, &sensor.humid3, &sensor.dew3);
  delay(500);
  //Increment packets
  sensor.reads++;

  //Make string for assembling data to a log
  String dataString = "";
  //Append to string
  dataString += String(now.unixtime());
  dataString += "|";
  dataString += String(now.month(), DEC);
  dataString += "/";
  dataString += String(now.day(), DEC);
  dataString += "/";
  dataString += String(now.year(), DEC);
  dataString += "|";
  dataString += String(now.hour(), DEC);
  dataString += ":";
  dataString += String(now.minute(), DEC);
  dataString += ":";
  dataString += String(now.second(), DEC);
  dataString += "|";
  dataString += String(sensor.temp1);
  dataString += "|";
  dataString += String(sensor.temp2);
  dataString += "|";
  dataString += String(sensor.temp3);
  dataString += "|";
  dataString += String(sensor.humid1);
  dataString += "|";
  dataString += String(sensor.humid2);
  dataString += "|";
  dataString += String(sensor.humid3);
  dataString += "|";
  dataString += String(sensor.packets);

  //Write to card
  File dataFile = SD.open("datalog.txt", FILE_WRITE);

  //Check if file is available and write to it, otherwise throw an error
  if (dataFile) 
  {
    dataFile.println(dataString);
    dataFile.close();
    //Also print to serial
    Serial.println(dataString);
  } 
  else
    Serial.println("Error opening datalog.txt");
  delay(500); //Ensure write finishes and file closes



  //Go to sleep
  if (ENDEBUG)
  {
    Serial.print("Sleeping for ");
    Serial.print(sleepTime / 1000);
    Serial.println(" seconds...");
    delay(100); //Ensure print completes before sleeping
  }
  digitalWrite(XBEE_SLEEP, HIGH);
  //Power off Arduino
  sleep.pwrDownMode(); //Set sleep mode
  sleep.sleepDelay(sleepTime); //Sleep for specified time  
}


void transmit()
{
	unsigned long bufSize = sizeof(sensor);
	char pBuffer[uBufSize];

	memcpy(pBuffer, &sensor, bufSize);

	for (unsigned int i = 0; i < bufSize; i++)
		Serial.print(pBuffer[i])
	delay(500);
}


void setupCol()
{
  //Make string for assembling column text
  String dataString = "";
  //Append to string
  dataString += "Unix Time";
  dataString += "|";
  dataString += "Standard Time";
  dataString += "|";
  dataString += "S1 Temp";
  dataString += "|";
  dataString += "S2 Temp";
  dataString += "|";
  dataString += "S3 Temp";
  dataString += "|";
  dataString += "S1 Humid";
  dataString += "|";
  dataString += "S2 Humid";
  dataString += "|";
  dataString += "S3 Humid";
  dataString += "|";
  dataString += "Packets Sent\n";
  dataString += "---------------------------------------------------------------------------------------";

  //Write to card
  File dataFile = SD.open("datalog.txt", FILE_WRITE);

  //Check if file is available and write to it, otherwise throw an error
  if (dataFile) 
  {
    dataFile.println(dataString);
    dataFile.close();
    //Also print to serial
    Serial.println(dataString);
  }
  else
    Serial.println("Error opening datalog.txt");
  delay(500); //Ensure write finishes and file closes
}