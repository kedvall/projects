/**********************************************************************
*                                                                     *
* Header file for RHGuageDatalogger.ino                               *
* Written by Kanyon Edvall				                              *
*                                                                     *
* This header file cleans up variable declaration for the main sketch *
*                                                                     *
**********************************************************************/
//Pins:
const int CS = 4; //Chip Select for SD cards (Default is pin 4 for Wireless SD Shield)

//Set up pins for sensor reading
const uint8_t clockPin1 = 2;
const uint8_t clockPin2 = 4;
const uint8_t clockPin3 = 6;

const uint8_t dataPin1 = 3;
const uint8_t dataPin2 = 5;
const uint8_t dataPin3 = 7;

//Sensirion variable setup:
float temperature1;
float humidity1;
float dewpoint1;

float temperature2;
float humidity2;
float dewpoint2;

float temperature3;
float humidity3;
float dewpoint3;

//Initializations:
//Initialize variables to reference three Sensirion sensors
Sensirion tempSensor1 = Sensirion(dataPin1, clockPin1);
Sensirion tempSensor2 = Sensirion(dataPin2, clockPin2);
Sensirion tempSensor3 = Sensirion(dataPin3, clockPin3);
//Initialize variable to reference real time clock module
RTC_DS1307 rtc;
//Initialize variable to write recorded data to SD Card
File sdCard;