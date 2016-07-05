//From: http://www.engblaze.com/microcontroller-tutorial-avr-and-arduino-timer-interrupts/

//avr-libc library includes
#include <avr/io.h>
#include <avr/interrupt.h>

#define LEDPIN 2

void setup()
{
	pinMode(LEDPIN, OUTPUT);

	//Initialize Timer1
	cli(); //Disable global interrupts
	TCCR1A = 0; //Set entire TCCR1A register to 0
	TCCR1B = 0; //Same for TCCR1B register

	//Enable Timer1 overflow interrupt
	TIMSK1 = (1 << TOIE1);
	//Set CS10 bit so timer runs at clock speed
	TCCR1B |= (1 << CS10);

	//Increase timer resolution
	TCCR1B |= (1 << CS10);
	TCCR1B |= (1 << CS12);

	//Enable global interrupts
	sei();
}

ISR(TIMER1_OVF_vect)
{
	digitalWrite(LEDPIN, !digitalRead(LEDPIN));
}

void loop()
{

}