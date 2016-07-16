#include <SoftwareSerial.h>

SoftwareSerial ss(11, 10); //RX, TX

void setup()
{
  Serial.begin(9600);
  while (!Serial) { ;} //Wait for port to connect
  delay(100);

  ss.begin(9600);
}

void loop() {
  Serial.println("Sending... ");
  //delay(1500);
  ss.print("+++");
  //delay(1500);

  // read from port 1, send to port 0:
  if (ss.available()) {
    int inByte = ss.read();
    Serial.write(inByte);
  }

  // read from port 0, send to port 1:
  if (Serial.available()) {
    int inByte = Serial.read();
    ss.write(inByte);
  }
}
