/**********************************************************************
*                                                                     *
* Data Logging Software for Illinois Tollway Concrete Testing         *
* Written by Kanyon Edvall                                            *
*                                                                     *
* This program uses the Sensirion library to record temperature and   *
*   humidity of concrete at three heights. Each recording is written  *
*   to an onboard SD card and transmitted wirelessly over serial.     *
*                                                                     *
* A real time clock module is used to timestamp all recorded data     *
*                                                                     *
**********************************************************************/
#include "RHGaugeDatalogger.h"

//Serial Debugging (Note that XBee uses serial print statements to communicate)
#define ENABLEDEBUG 1 //Default is 0, set 1 to enable (Disables XBee communication)

///////////////////////////////////////////////////////////////////////
// Initial Setup:                                                    //
//   Start and set RTC Module, check for error                       //
//   Starts serial communication at 9600 baud (default for Xbees)    //
//   Set columns for output text file                                //
///////////////////////////////////////////////////////////////////////
void setup()
{  
  /*
  //Setup the Watchdog Timer
  MCUSR &= ~(1<<WDRF); //Clear the reset flag
  WDTCSR |= (1<<WDCE) | (1<<WDE); //To change WDE or prescaler, need to set WDCE (This will allow updates for 4 clock cycles)
  WDTCSR = 1<<WDP0 | 1<<WDP3; //Set new watchdog timeout prescaler value (8.0 seconds timeout)
  WDTCSR |= _BV(WDIE); //Enable the WD interrupt (note no reset)
  */

  //Pin mode for potentiometers
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);
  pinMode(A3, INPUT_PULLUP);
  pinMode(A4, INPUT_PULLUP);
  //For LED
  pinMode(LEDPIN, OUTPUT);
  
  Serial.begin(9600); //Start serial communication at 9600 baud

  //Check RTC started correctly, display error if not
  if (!rtc.begin() && ENABLEDEBUG)
    Serial.println("Couldn't find RTC");

  rtc.adjust(DateTime(F(__DATE__), F(__TIME__))); //Set RTC to date & time this sketch was compiled

  SD.begin(CS); //Initialize SD card

  InitColSetup(); //Set up columns for output text file
} //End of setup function

///////////////////////////////////////////////////////////////////////
// Main Loop:                                                        //
//   Reads temperature and humidity from sensors                     //
//   Saves readings to SD card and transmits it wirelessly           //
///////////////////////////////////////////////////////////////////////
void loop() 
{
  if (ENABLEDEBUG)
    digitalWrite(LEDPIN, HIGH); //Turn on status LED

  //Reset variables for sensors 
  sensor.temperature1 = -40;
  sensor.temperature2 = -40;
  sensor.temperature3 = -40;

  sensor.humidity1 = -1;
  sensor.humidity2 = -1;
  sensor.humidity3 = -1;

  ReadData(); //Read from sensors

  RecordData(); //Record measurements

  //Transmit sensor data over serial
  if (ENABLEDEBUG)
    PrintDebug();
  else
    PrintVars();

  //Sleep for 15 minutes 
  for (sleepCount = 0; sleepCount < 15; sleepCount++) //DEFAULT: < 113, changed to test!
    watchdogEnable(TIME); //8 second interval
} //End of main loop

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
  else if (ENABLEDEBUG)
    Serial.println("Error opening SD card");
} //End of InitColSetup function

///////////////////////////////////////////////////////////////////////
// Function: ReadData                                                //
// Take all necessary measurements                                   //
///////////////////////////////////////////////////////////////////////
void ReadData()
{
  //Get current time from system
  now = rtc.now();

  //Read from potentiometers
  sensor.L1 = digitalRead(A0);
  sensor.L2 = digitalRead(A1);
  sensor.L3 = digitalRead(A2);
  sensor.L4 = digitalRead(A3);
  sensor.L5 = digitalRead(A4);

  //Read RH guages with 1s delay in between each read
  tempSensor1.measure(&sensor.temperature1, &sensor.humidity1, &sensor.dewpoint1);
  delay(1000);
  tempSensor2.measure(&sensor.temperature2, &sensor.humidity2, &sensor.dewpoint2);
  delay(1000);
  tempSensor3.measure(&sensor.temperature3, &sensor.humidity3, &sensor.dewpoint3);
  delay(1000);
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
    sdCard.print(sensor.L1);
    sdCard.print(",");
    sdCard.print(sensor.L2);
    sdCard.print(",");
    sdCard.print(sensor.L3);
    sdCard.print(",");
    sdCard.print(sensor.L4);
    sdCard.print(",");
    sdCard.print(sensor.L5);
    sdCard.print(",");

    //Record RH guage measurements
    sdCard.print(sensor.temperature1);
    sdCard.print(",");
    sdCard.print(sensor.temperature2);
    sdCard.print(",");
    sdCard.print(sensor.temperature3);
    sdCard.print(",");
    sdCard.print(sensor.humidity1);
    sdCard.print(",");
    sdCard.print(sensor.humidity2);
    sdCard.print(",");
    sdCard.print(sensor.humidity3);
    sdCard.println();

    //Wait to ensure correct write
    delay(250);

    //Close SD card
    sdCard.close();
  }
  else if (ENABLEDEBUG)
    Serial.println("Error opening SD card");
} //End of RecordData function

///////////////////////////////////////////////////////////////////////
// Function: PrintVars                                               //
// Transmits packet over serial                                      //
///////////////////////////////////////////////////////////////////////
void PrintVars()
{
  unsigned long uBufSize = sizeof(sensor);
  char pBuffer[uBufSize];

  memcpy(pBuffer, &sensor, uBufSize);

  for(int i = 0; i < uBufSize; i++)
    Serial.print(pBuffer[i]);
    
  Serial.println();
} //End of PrintVars function

///////////////////////////////////////////////////////////////////////
// Function: watchdogEnable                                          //
// Configures Watchdog timer for sleeping                            //
///////////////////////////////////////////////////////////////////////
void watchdogEnable(const byte interval)
{
  MCUSR = 0; //Reset flags
  WDTCSR |= 0b00011000; //See docs, set WDCE, WDE
  WDTCSR = 0b01000000 | interval; //Set WDIE and appropriate delay

  wdt_reset();
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_mode(); //Go to sleep and wait for interrupt
} //End of watchdogEnable function

///////////////////////////////////////////////////////////////////////
// Function: ISR(WDT_vect                                            //
// Watchdog Interrupt Service Routine. Executed on watchdog timeout  //
///////////////////////////////////////////////////////////////////////
ISR(WDT_vect)
{
  wdt_disable(); //Disable watchdog
} //End of ISR(WDT_vect)

///////////////////////////////////////////////////////////////////////
// Function: PrintDebug                                              //
// Optional debug statements over serial. Set on/off flag above      //
///////////////////////////////////////////////////////////////////////
void PrintDebug()
{
  //These print statements should no longer be needed, just for debugging
  Serial.println();
  Serial.print("=======================================");
  Serial.print(sensor.L1);
  Serial.print(',');
  Serial.print(sensor.L2);
  Serial.print(',');
  Serial.print(sensor.L3);
  Serial.print(',');
  Serial.print(sensor.L4);
  Serial.print(',');
  Serial.print(sensor.L5);

  Serial.println(); 
  Serial.print("Temperature 1: ");
  Serial.print(sensor.temperature1);
  Serial.print(" C, Humidity 1: ");
  Serial.print(sensor.humidity1);
  Serial.print(" %, Dewpoint 1: ");
  Serial.print(sensor.dewpoint1); 
  Serial.print(" C");

  Serial.println();
  Serial.print("-------------------------------------");
  Serial.print("Temperature 2: ");
  Serial.print(sensor.temperature2);
  Serial.print(" C, Humidity 2: ");
  Serial.print(sensor.humidity2);
  Serial.print(" %, Dewpoint 2: ");
  Serial.print(sensor.dewpoint2);
  Serial.print(" C");

  Serial.println();
  Serial.print("-------------------------------------");
  Serial.print("Temperature 3: ");
  Serial.print(sensor.temperature3);
  Serial.print(" C, Humidity 3: ");
  Serial.print(sensor.humidity3);
  Serial.print(" %, Dewpoint 3: ");
  Serial.print(sensor.dewpoint3);
  Serial.print(" C");
  
  Serial.println("=======================================");
} //End of PrintDebug function