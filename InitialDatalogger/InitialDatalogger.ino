/************************************************************************
* Basic sketch designed to ensure data is correctly recorded to SD card *
* 	before a more advanced sketch is implemented						            *
************************************************************************/
#include "RHGaugeDatalogger.h"

const int chipSelect = 4;

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
  while (!Serial) { ;} //Wait for serial port to connect

  Serial.print("Initializing SD card");

  //Check if card is present and can be initialized
  if (!SD.begin(chipSelect))
  {
    Serial.println("Card failed to initialize or is not present");
    return;
  }
  Serial.println("Card successfully initialized");
}

void loop()
{
  //Reset variables for sensors 
  sensor.temp1 = -40;
  sensor.temp2 = -40;
  sensor.temp3 = -40;
  sensor.humid1 = -1;
  sensor.humid2 = -1;
  sensor.humid3 = -1;

  //Get current time from system
  now = rtc.now();

  //Read RH gauges with 1s delay in between each read
  Sensor1.measure(&sensor.temp1, &sensor.humid1, &sensor.dew1);
  delay(1000);
  Sensor2.measure(&sensor.temp2, &sensor.humid2, &sensor.dew2);
  delay(1000);
  Sensor3.measure(&sensor.temp3, &sensor.humid3, &sensor.dew3);
  delay(1000);

  //Make string for assembling data to a log
  String dataString = "";
  //Append to string
  dataString += "Time: ";
  dataString += String(now.month(), DEC);
  dataString += "/";
  dataString += String(now.day(), DEC);
  dataString += "/";
  dataString += String(now.year(), DEC);
  dataString += ", ";
  dataString += String(now.hour(), DEC);
  dataString += ":";
  dataString += String(now.minute(), DEC);
  dataString += ":";
  dataString += String(now.second(), DEC);
  dataString += "\nTemperature: ";
  dataString += String(sensor.temp1);
  dataString += ",";
  dataString += String(sensor.temp2);
  dataString += ",";
  dataString += String(sensor.temp3);
  dataString += "\nHumidity: ";
  dataString += String(sensor.humid1);
  dataString += ",";
  dataString += String(sensor.humid2);
  dataString += ",";
  dataString += String(sensor.humid3);

  //Write to card
  File dataFile = SD.open("datalog.txt", FILE_WRITE);
  //Check if file is available and write to it, otherwise throw an error
  if (dataFile) 
  {
    dataFile.println(dataString);
    dataFile.println("");
    dataFile.close();
  } 
  else
    Serial.println("Error opening datalog.txt");
}