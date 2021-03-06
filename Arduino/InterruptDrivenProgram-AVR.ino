//From: http://www.engblaze.com/we-interrupt-this-program-to-bring-you-a-tutorial-on-arduino-interrupts/

#include <avr/interrupt.h>
volatile int myInterruptVar;

void setup(void)
{
	pinMode(2, INPUT);
	pinMode(13, OUTPUT);
	digitalWrite(2, HIGH);	//Enable pullup resistor

	sei();					//Enable global interrupts
	EIMSK |= (1 << INT0);	//Enable external interrupt INT0
	EICRA |= (1 << ISC01);	//Trigger INT0 on falling edge
}

void loop(void)
{

}

//Interrupt Service Routine attached to INT0 vector
ISR(INT0_vect)
{
	digitalWrite(13, !digitalRead(13)); //Toggle LED on pin 13
}