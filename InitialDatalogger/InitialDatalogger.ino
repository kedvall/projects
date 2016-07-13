/************************************************************************
* Basic sketch designed to ensure data is correctly recorded to SD card *
* 	before a more advanced sketch is implemented						            *
************************************************************************/
//Libraries to include:
#include <Sensirion.h>
#include <Wire.h> //RTClib depends on this
#include <RTClib.h>
#include <SPI.h>
#include <SD.h>

//Pin Setup:
const int chipSelect = 4;
const uint8_t clockPin1 = 2;
const uint8_t clockPin2 = 4;
const uint8_t clockPin3 = 6;
const uint8_t dataPin1 = 3;
const uint8_t dataPin2 = 5;
const uint8_t dataPin3 = 7;

//Objects
Sensirion Sensor1 = Sensirion(dataPin1, clockPin1);
Sensirion Sensor2 = Sensirion(dataPin2, clockPin2);
Sensirion Sensor3 = Sensirion(dataPin3, clockPin3);
RTC_DS1307 rtc; //For real time clock module
DateTime now; //Var to store time stamp

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

  long unsigned int packets = 0;
} sensor;

///////////////////////////////////////////////////////////////////////
// Initial Setup:                                                    //
//   Start and set RTC Module, check for error                       //
//   Starts serial communication at 9600 baud (default for Xbees)    //
//   Set columns for output text file                                //
///////////////////////////////////////////////////////////////////////
void setup()
{
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

  Serial.print ("Initializing SD card...");

  //Check if card is present and can be initialized
  if (!SD.begin(chipSelect))
  {
    Serial.println("Card failed to initialize or is not present");
    return;
  }
  Serial.println("Card successfully initialized");

  Serial.println("");
  Serial.println("Recording Data:");
}

void loop()
{
  //Reset variables for sensors 
  sensor.temp1 = -40;
  sensor.temp2 = -40;
  sensor.temp3 = -40;

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
  sensor.packets++;

  //Make string for assembling data to a log
  String dataString = "";
  //Append to string
  dataString += String(now.unixtime());
  dataString += "\t|\t";
  dataString += String(now.month(), DEC);
  dataString += "/";
  dataString += String(now.day(), DEC);
  dataString += "/";
  dataString += String(now.year(), DEC);
  dataString += "\t|\t";
  dataString += String(now.hour(), DEC);
  dataString += ":";
  dataString += String(now.minute(), DEC);
  dataString += ":";
  dataString += String(now.second(), DEC);
  dataString += "\t|\t";
  dataString += String(sensor.temp1);
  dataString += "\t|\t";
  dataString += String(sensor.temp2);
  dataString += "\t|\t";
  dataString += String(sensor.temp3);
  dataString += "\t|\t";
  dataString += String(sensor.humid1);
  dataString += "\t|\t";
  dataString += String(sensor.humid2);
  dataString += "\t|\t";
  dataString += String(sensor.humid3);
  dataString += "\t|\t";
  dataString += String(sensor.packets);

  //Write to card
  File dataFile = SD.open("datalog.txt", FILE_WRITE);

  //Check if file is available and write to it, otherwise throw an error
  if (dataFile) 
  {
    dataFile.println(dataString);
    dataFile.println("");
    dataFile.close();
    //Also print to serial
    Serial.println(dataString);
    Serial.println("");
  } 
  else
    Serial.println("Error opening datalog.txt");
}

void setupCol()
{
  //Make string for assembling column text
  String dataString = "";
  //Append to string
  dataString += "Unix Time: ";
  dataString += "\t|\t";
  dataString += "Standard Time ";
  dataString += "\t|\t";
  dataString += "S1 Temp: ";
  dataString += "\t|\t";
  dataString += "S2 Temp: ";
  dataString += "\t|\t";
  dataString += "S3 Temp: ";
  dataString += "\t|\t";
  dataString += "S1 Humid: ";
  dataString += "\t|\t";
  dataString += "S2 Humid: ";
  dataString += "\t|\t";
  dataString += "S3 Humid: ";
  dataString += "\t|\t";
  dataString += "Packets Sent: \n";
  dataString += "---------------------------------------------------------------------\n";
}