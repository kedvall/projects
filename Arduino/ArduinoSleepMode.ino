//From: http://www.engblaze.com/hush-little-microprocessor-avr-and-arduino-sleep-mode-basics/

#include <avr/interrupt.h>
#include <avr/power.h>
#include <avr/sleep.h>
#include <avr/io.h>

void setup()
{
	DDRD &= B00000011;		//Set Arduino pins 2 to 7 as inputs, leave 0 & 1 (RX & TX) as is
	DDRB = B00000000;		//Set pins 8 to 13 as inputs
	PORTD |= B11111100;		//Enable pullups on pins 2 to 7, leave pins 0 & 1 alone
	PORTB |= B11111111;		//Enable pullups on pins 8 to 13
	pinMode(13, OUTPUT);	//Set pin 13 as an output so we can use LED to monitor

}

void loop(void)
{
	//Stay awake for 1 second, then sleep
	//LED turns off when sleeping, then back on upon wake
	delay(1000);
	sleepNow();
}

void sleepNow()
{
	//Set pin 2 as interrupt and attach handler:
	attachInterrupt(0, pinInterrupt, LOW);
	delay(100);

	//Choose preferred sleep mode:
	set_sleep_mode(SLEEP_MODE_PWR_DOWN);

	//Set sleep enable (SE) bit:
	sleep_enable();

	//Put the device to sleep:
	digitalWrite(13,LOW); //Turn LED off to indicate sleep
	sleep_mode();

	//Sketch resumes here
	sleep_disable();
	digitalWrite(13,HIGH); //Turn LED on to indicate wake
}

void pinInterrupt(void)
{
	detachInterrupt(0);
}