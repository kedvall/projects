#include <SoftwareSerial.h>

SoftwareSerial ss(11, 10); //RX, TX
int sentDat;

void setup() 
{
  // initialize serial communication:
  Serial.begin(9600);
  while (!Serial) { ;} // wait for serial port to connect. Needed for native USB port only
  Serial.println("HS up");
  delay(100);

  ss.begin(9600);
  Serial.println("SS up");
  delay(100);
}

void loop()
{
  if (ss.available())
  {
    sentDat = ss.read();

    if (sentDat == 'h')
      Serial.println("Received h");

    if (sentDat == 'b')
      Serial.println("Received b");
  }
}
