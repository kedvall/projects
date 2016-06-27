/**********************************************************************
*                                                                     *
* Data Logging Software for Illinois Tollway Concrete Testing         *
* Written by Kanyon Edvall and Sachindra Dahal                        *
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
#define ENABLEDEBUG 0 //Default is 0, set 1 to enable (Disables XBee communication)

///////////////////////////////////////////////////////////////////////
// Initial Setup:                                                    //
//   Start and set RTC Module, check for error                       //
//   Starts serial communication at 9600 baud (default for Xbees)    //
//   Set columns for output text file                                //
///////////////////////////////////////////////////////////////////////
void setup()
{ 
  //Setup pinout (all disabled temporarily)
  DDRD &= B00000011;
  DDRB = B00000000;
  PORTD |= B11111100;
  PORTB |= B11111111;

  //Check RTC started correctly, display error if not
  if (!rtc.begin() && ENABLEDEBUG)
    Serial.println("Couldn't find RTC");
 
  //Pin mode for potentiometers
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);
  pinMode(A3, INPUT_PULLUP);
  pinMode(A4, INPUT_PULLUP);
  //For LED
  pinMode(LEDPIN, OUTPUT);

  // initialize Timer1
  cli();          // disable global interrupts
  TCCR1A = 0;     // set entire TCCR1A register to 0
  TCCR1B = 0;     // same for TCCR1B

  // set compare match register to desired timer count:
  OCR1A = 15624;
  // turn on CTC mode:
  TCCR1B |= (1 << WGM12);
  // Set CS10 and CS12 bits for 1024 prescaler:
  TCCR1B |= (1 << CS10);
  TCCR1B |= (1 << CS12);
  // enable timer compare interrupt:
  TIMSK1 |= (1 << OCIE1A);
  // enable global interrupts:
  sei();
  
  //Start serial communication at 9600 baud
  Serial.begin(9600);

  //Set RTC to date & time this sketch was compiled
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  lastRead = now.unixtime() - 900;

  //Initialize SD card
  SD.begin(CS);

  //Set up columns for output text file
  InitColSetup();
} //End of setup function

///////////////////////////////////////////////////////////////////////
// Main Loop:                                                        //
//   Reads temperature and humidity from sensors                     //
//   Saves readings to SD card and transmits it wirelessly           //
///////////////////////////////////////////////////////////////////////
void loop() 
{
  //Read from sensors:
  ReadData();

  //Record measurements:
  RecordData();

  //Transmit sensor data over serial
  if (ENABLEDEBUG)
    PrintDebug();
  else
    PrintVars();
  
  //Reset variables for sensors
  //Are you sure this is necessary?
  sensor.temperature1 = -40;
  sensor.temperature2 = -40;
  sensor.temperature3 = -40;

  sensor.humidity1 = 0;
  sensor.humidity2 = 0;
  sensor.humidity3 = 0;

  //Power down
  if (ENABLEDEBUG)
    Serial.println ("Sleeping");
  sleepNow(); //Power down Arduino
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
  //Reset read counter
  lastRead = now.unixtime();

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
  delay (1000);
  tempSensor2.measure(&sensor.temperature2, &sensor.humidity2, &sensor.dewpoint2);
  delay (1000);
  tempSensor3.measure(&sensor.temperature3, &sensor.humidity3, &sensor.dewpoint3);
  delay (1000);
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
// Function: sleepNow                                                //
// Forces Arduino to enter low power state                           //
///////////////////////////////////////////////////////////////////////
void sleepNow(void)
{
  // Set pin 2 as interrupt and attach handler:
  attachInterrupt(0, pinInterrupt, LOW);
  delay(100);

  // Choose our preferred sleep mode:
  set_sleep_mode(SLEEP_MODE_IDLE);

  // Set sleep enable (SE) bit:
  sleep_enable();

  // Put the device to sleep:
  digitalWrite(13,LOW);   // turn LED off to indicate sleep
  sleep_mode();

  // Upon waking up, sketch continues from this point.
  sleep_disable();
  digitalWrite(13,HIGH);   // turn LED on to indicate awake
}

///////////////////////////////////////////////////////////////////////
// Function: pinInterrupt                                            //
// Disables interrupt to prevent accidental firing                   //
///////////////////////////////////////////////////////////////////////
void pinInterrupt(void)
{
  detachInterrupt(0);
}

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

///////////////////////////////////////////////////////////////////////
// Interrupt Service Routine: TIMER1_COMPA_vect                      //
// Increment number of seconds each timer overflow until 15 minutes  //
///////////////////////////////////////////////////////////////////////
ISR(TIMER1_COMPA_vect)
{
  seconds++;
  if (seconds >= 900)
  {
      seconds = 0;
      loop();
  }
}