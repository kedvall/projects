//Sketch for testing sleep mode with wake up on WDT
#include <avr/sleep.h>
#include <avr/power.h>
#include <avr/wdt.h>

#define LED_PIN 13 //Built in LED on pin 13

volatile int flag = 1;

/*********************************************************
 * Name: ISR(WDT_vect)									 *
 * Returns: Nothing										 *
 * Parameters: None 									 *
 * Description: Watchdog Interrupt Service. 			 *
 * 				This is executed when watchdog times out *
 ********************************************************/
 ISR(WDT_vect)
 {
 	if (flag == 0)
 		flag = 1;
 	else
 		Serial.println("WDT Overrun!");
 }

/*********************************************************
* Name: enterSleep 										 *
* Returns: Nothing 										 *
* Parameters: None 										 *
* Description: Enters Arduino into sleep mode 			 *
*********************************************************/
void enterSleep(void)
{
	//Set sleep mode to Power Down (lowest power consumption)
	set_sleep_mode(SLEEP_MODE_PWR_DOWN); 
	//Allow Arduino to enter sleep mode
	sleep_enable();

	//Actually enter sleep mode
	sleep_mode();

	//The program will continue from here after the WDT timeout
	sleep_disable(); //First thing to do is disable sleep

	//Re-enable peripherals
	power_all_enable();
}

/*********************************************************
* Name: setup 											 *
* Returns: Nothing 										 *
* Parameters: None 										 *
* Description: Setup for serial comms and 				 *
* 			   the Watch dog timeout  					 *
*********************************************************/
void setup()
{
	Serial.begin(9600);
	Serial.println("Initializing...");
	delay(100); //Allow for serial print to complete

	pinMode(LED_PIN, OUTPUT);

	//Setup the WatchDog Timer//
	//Clear the reset flag
	MCUSR &= ~(1<<WDRF);

	//To change WDE or prescaler, need to set WDCE (This will allow updates for 4 clock cycles)
	WDTCSR |= (1<<WDCE) | (1<<WDE);

	//Set new watchdog timeout prescaler value
	WDTCSR = 1<<WDP0 | 1<<WDP3; //8.0 seconds

	//Enable the WD interrupt (note no reset)
	WDTCSR |= _BV(WDIE);

	Serial.println("Initialization complete");
	delay(100); //Wait for serial print to complete
}

/*********************************************************
* Name: loop 											 *
* Returns: Nothing 										 *
* Parameters: None 										 *
* Description: Main application loop 					 *
*********************************************************/
void loop()
{
	if (flag == 1)
	{
		digitalWrite(LED_PIN, !digitalRead(LED_PIN)); //Toggle LED
		flag = 0; //Clear flag

		//Re-enter sleep mode
		enterSleep();
	}
}