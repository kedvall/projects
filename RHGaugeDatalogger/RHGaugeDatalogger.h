/**********************************************************************
*                                                                     *
* Header file for RHGuageDatalogger.ino                               *
* Written by Kanyon Edvall				                              *
*                                                                     *
* This header file cleans up variable declaration for the main sketch *
*                                                                     *
**********************************************************************/
//Includes
#include <Arduino.h>
#include <Sensirion.h>
#include <Wire.h> //RTClib depends on this
#include <RTClib.h>
#include <SD.h>
#include <SPI.h>
#include <Sleep_n0m1.h>
#include <XBee.h>

//Defines
//#define CS 4 //Chip Select for SD cards (Default is pin 4 for Wireless SD Shield)
#define LEDPIN 13 //Built in LED for status display
#define XBEE_SLEEP 9 //Arduino (NOT XBee) pin to use for controlling XBee sleep
#define TIME 0b100001 //Time 

//Set up pins for sensor reading
const uint8_t clockPin1 = 2;
const uint8_t clockPin2 = 4;
const uint8_t clockPin3 = 6;

const uint8_t dataPin1 = 3;
const uint8_t dataPin2 = 5;
const uint8_t dataPin3 = 7;

//Other variables:
char xBeePin7[] = "D7";
char xBeeSleepMode[] = "SM";
unsigned long sleepTime; //Time in MS for Arduino to sleep
DateTime now; //Var to store timestamp

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
} sensor;

//Initializations:
//Variables to reference three Sensirion sensors
Sensirion Sensor1 = Sensirion(dataPin1, clockPin1);
Sensirion Sensor2 = Sensirion(dataPin2, clockPin2);
Sensirion Sensor3 = Sensirion(dataPin3, clockPin3);

RTC_DS1307 rtc; //For real time clock module

//File sdCard; //To write recorded data to SD Card

Sleep sleep; //Sleep for Sleep_n0m1 library

XBee radio; //For XBee library