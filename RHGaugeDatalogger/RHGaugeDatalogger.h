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
#include "SD.h"
#include <SPI.h>
#include <Sleep_n0m1.h>
#include <XBee.h>

//Defines
#define CS 4 //Chip Select for SD cards (Default is pin 4 for Wireless SD Shield)
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
unsigned long sleepTime;
DateTime now;

//Create struct to store data to be transmitted
struct dataPacket
{
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

	//Potentiometer variables
	int L1;
	int L2;
	int L3;
	int L4;
	int L5;
} sensor;

//Initializations:
//Variables to reference three Sensirion sensors
Sensirion tempSensor1 = Sensirion(dataPin1, clockPin1);
Sensirion tempSensor2 = Sensirion(dataPin2, clockPin2);
Sensirion tempSensor3 = Sensirion(dataPin3, clockPin3);

RTC_DS1307 rtc; //For real time clock module

File sdCard; //To write recorded data to SD Card

Sleep sleep; //Sleep for Sleep_n0m1 library

XBee radio; //For XBee library