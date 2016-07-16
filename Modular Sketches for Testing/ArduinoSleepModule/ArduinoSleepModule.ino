/************************************************************************
* Module for testing sleep functionality of Arduino (without XBee)      *
************************************************************************/
#include <SPI.h>
#include <avr/sleep.h>
#include <avr/power.h>
#include <avr/wdt.h>

// Data logging configuration.
#define LOGGING_FREQ_SECONDS   30      // Seconds to wait before a new sensor reading is logged.

#define SENSOR_PIN             4        // Analog pin to read sensor values from (for example

                                                   
#define MAX_SLEEP_ITERATIONS   LOGGING_FREQ_SECONDS / 8  // Number of times to sleep (for 8 seconds) before
                                                         // a sensor reading is taken and sent to the server.
                                                         // Don't change this unless you also change the 
                                                         // watchdog timer configuration.

int sleepIterations = 0;
volatile bool watchdogActivated = false;

// Define watchdog timer interrupt.
ISR(WDT_vect)
{
  // Set the watchdog activated flag.
  // Note that you shouldn't do much work inside an interrupt handler.
  watchdogActivated = true;
}

// Put the Arduino to sleep.
void sleep()
{
  // Set sleep to full power down.  Only external interrupts or 
  // the watchdog timer can wake the CPU!
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);

  // Turn off the ADC while asleep.
  power_adc_disable();

  // Enable sleep and enter sleep mode.
  sleep_mode();

  // CPU is now asleep and program execution completely halts!
  // Once awake, execution will resume at this point.
  
  // When awake, disable sleep mode and turn on all devices.
  sleep_disable();
  power_all_enable();
}

void setup()
{
  Serial.begin(9600);

  // Note that the default behavior of resetting the Arduino
  // with the watchdog will be disabled.
  
  // This next section of code is timing critical, so interrupts are disabled.
  // See more details of how to change the watchdog in the ATmega328P datasheet
  // around page 50, Watchdog Timer.
  noInterrupts();
  
  // Set the watchdog reset bit in the MCU status register to 0.
  MCUSR &= ~(1<<WDRF);
  
  // Set WDCE and WDE bits in the watchdog control register.
  WDTCSR |= (1<<WDCE) | (1<<WDE);

  // Set watchdog clock prescaler bits to a value of 8 seconds.
  WDTCSR = (1<<WDP0) | (1<<WDP3);
  
  // Enable watchdog as interrupt only (no reset).
  WDTCSR |= (1<<WDIE);
  
  // Enable interrupts again.
  interrupts();

  //sleepTime = 7000; //Sleep for 7 seconds
  pinMode(13, OUTPUT);


  Serial.println("Sleep module sketch starting...");
  delay(500);
}

void loop()
{
  Serial.println("Loop");
  delay(500);
    // Don't do anything unless the watchdog timer interrupt has fired.
  if (watchdogActivated)
  {
    watchdogActivated = false;
    // Increase the count of sleep iterations and take a sensor
    // reading once the max number of iterations has been hit.
    digitalWrite(13, HIGH);
    delay(1000);
    digitalWrite(13, LOW);
    sleepIterations += 1;
    if (sleepIterations >= MAX_SLEEP_ITERATIONS) {
      // Reset the number of sleep iterations.
      Serial.println("Reset");
      sleepIterations = 0;
    }
  }
  
  // Go to sleep!
  //Serial.println("Sleeping...");
  sleep();
}


/*
  delay(100); //Delay for Serial to resume after sleeping
  Serial.println("Executing code routine...");

  //Blink LED 5 times
  for (int i = 0; i < 6; i++)
  {
    Serial.print("Blinking ");
    Serial.print(5 - i);
    Serial.println(" more times");
    digitalWrite(13, HIGH);
    delay(500);
    digitalWrite(13, LOW);
    delay(500);
  }

  //Go to sleep
  Serial.print("Sleeping for ");
  Serial.print(sleepTime / 1000);
  Serial.println(" seconds...");
  delay(100); //Ensure print completes before sleeping

  sleep();
}

*/