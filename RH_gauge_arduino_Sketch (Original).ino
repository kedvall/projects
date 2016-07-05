#include <Arduino.h>
#include <Sensirion.h>
#include <Wire.h>         // this #include still required because the RTClib depends on it
#include "RTClib.h"
#include "SD.h"
#include <SPI.h>
#include "LowPower.h"


  
const int chipSelect=10; // For SD Cards



const uint8_t dataPin1  =  3;  //BLACK EVEN // WHITE ODD
const uint8_t clockPin1 =  2;

const uint8_t dataPin2  =  5;
const uint8_t clockPin2 =  4;

const uint8_t dataPin3  =  7;
const uint8_t clockPin3 =  6;


float temperature1;
float humidity1;
float dewpoint1;

float temperature2;
float humidity2;
float dewpoint2;

float temperature3;
float humidity3;
float dewpoint3;

Sensirion tempSensor1 = Sensirion(dataPin1, clockPin1);
Sensirion tempSensor2 = Sensirion(dataPin2, clockPin2);
Sensirion tempSensor3 = Sensirion(dataPin3, clockPin3);








RTC_DS1307 rtc;

 File mySensorData;

 void error(char *str)
 {
  Serial.print("error: ");
  Serial.println(str);

  while(1);
  }
  
void setup () {
  
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
 
  }
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);
  pinMode(A3, INPUT_PULLUP);
  pinMode(A4, INPUT_PULLUP);
pinMode(dataPin1, INPUT_PULLUP);
 pinMode(dataPin2, INPUT_PULLUP);
  pinMode(dataPin3, INPUT_PULLUP);

    pinMode(13, OUTPUT); 
  delay(50);  



    Serial.begin(9600);
    // following line sets the RTC to the date & time this sketch was compiled
//    rtc.begin(DateTime(F(__DATE__), F(__TIME__)));
    // This line sets the RTC with an explicit date & time, for example to set
    // January 21, 2014 at 3am you would call:
     rtc.adjust(DateTime(2015, 11, 25, 11, 59, 00));

    //pinMode(10,OUTPUT);
    //digitalWrite(10, HIGH);
    SD.begin(chipSelect);
    mySensorData= SD.open("ArdData.txt",FILE_WRITE);

    mySensorData.print("Year");
    mySensorData.print(",");
    mySensorData.print("Month");
    mySensorData.print(",");
    mySensorData.print("Day");
    mySensorData.print(",");
    mySensorData.print("Hour");
    mySensorData.print(",");
    mySensorData.print("Minute");
    mySensorData.print(",");
    mySensorData.print("Second");
    mySensorData.print(",");
    mySensorData.print("Line 1");
    mySensorData.print(",");
    mySensorData.print("Line 2");
    mySensorData.print(",");
    mySensorData.print("Line 3");
    mySensorData.print(",");
    mySensorData.print("Line 4");
    mySensorData.print(",");
    mySensorData.print("Line 5");
    mySensorData.print(",");
    mySensorData.print("Temp 1");
    mySensorData.print(",");
    mySensorData.print("Temp 2");
    mySensorData.print(",");
    mySensorData.print("Temp 3");
    mySensorData.print(",");
    mySensorData.print("Hum 1");
    mySensorData.print(",");
    mySensorData.print("Hum 2");
    mySensorData.print(",");
    mySensorData.print("Hum 3");
    mySensorData.println();

    mySensorData.close();
}
 

int i =0;





void loop () {

if(i > 0) {

digitalWrite(13,HIGH);
Serial.println ("Measuring");
 
// DO ALL MEASUREMENTS



  mySensorData= SD.open("ArdData.txt",FILE_WRITE);

  

if(mySensorData) {
    
    // Potentiometer Reading
   int L1 = digitalRead(A0);
   int L2 = digitalRead(A1);
   int L3 = digitalRead(A2);
   int L4 = digitalRead(A3);
   int L5 = digitalRead(A4);
    
    DateTime now = rtc.now();
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
   
    Serial.print(" seconds since 1970: ");
    Serial.println(now.unixtime());
   
  
    Serial.println();

    mySensorData.print(now.year(), DEC);
    mySensorData.print(",");
    mySensorData.print(now.month(), DEC);
    mySensorData.print(",");
    mySensorData.print(now.day(), DEC);
    mySensorData.print(",");
    mySensorData.print(now.hour(), DEC);
    mySensorData.print(",");
    mySensorData.print(now.minute(), DEC);
    mySensorData.print(",");
    mySensorData.print(now.second(), DEC);
    mySensorData.print(",");
    mySensorData.print(L1);
    mySensorData.print(",");
    mySensorData.print(L2);
    mySensorData.print(",");
    mySensorData.print(L3);
    mySensorData.print(",");
    mySensorData.print(L4);
    mySensorData.print(",");
    mySensorData.print(L5);
    mySensorData.print(",");
    




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
    
    // RH gauge SURU
tempSensor1.measure(&temperature1, &humidity1, &dewpoint1);
  delay (1000);
  tempSensor2.measure(&temperature2, &humidity2, &dewpoint2);
  delay (1000);
  tempSensor3.measure(&temperature3, &humidity3, &dewpoint3);
  delay (1000);
  
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
    mySensorData.print(temperature1);
    mySensorData.print(",");
    mySensorData.print(temperature2);
    mySensorData.print(",");
    mySensorData.print(temperature3);
    mySensorData.print(",");
    mySensorData.print(humidity1);
    mySensorData.print(",");
    mySensorData.print(humidity2);
    mySensorData.print(",");
    mySensorData.print(humidity3);
    mySensorData.println();
  delay(2500);  

temperature1 = -40;
temperature2 = -40;
temperature3 = -40;

humidity1 = 0;
humidity2 = 0;
humidity3 = 0;
//RH gauge END





    
    delay(900);
  mySensorData.close();
  
  } // if mysensordata wala loop

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


