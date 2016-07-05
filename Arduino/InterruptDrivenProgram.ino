//From: http://www.engblaze.com/we-interrupt-this-program-to-bring-you-a-tutorial-on-arduino-interrupts/

#include <avr/interrupt.h>
volatile int myInterruptVar;

void setup(void)
{
	pinMode(2, INPUT);
	pinMode(13, OUTPUT);
	digitalWrite(2, HIGH);	//Enable pullup resistor

	attachInterrupt(0, pin2ISR, FALLING);
}

void loop(void)
{

}

//Interrupt Service Routine attached to INT0 vector
ISR(EXT_INT0_vect)
{
	digitalWrite(13, !digitalRead(13)); //Toggle LED on pin 13
}