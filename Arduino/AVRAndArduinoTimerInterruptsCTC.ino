//From: http://www.engblaze.com/microcontroller-tutorial-avr-and-arduino-timer-interrupts/

//avr-libc library includes
#include <avr/io.h>
#include <avr/interrupt.h>

#define LEDPIN 2

void setup()
{
	pinMode(LEDPIN, OUTPUT);

	cli(); //Disable global interrupts
	TCCR1A = 0; //Set entire TCCR1A register to 0
	TCCR1B = 0; //Same for TCCR1B

	//Set compare match register to desired timer count
	OCR1A = 15624;
	//Turn on CTC mode:
	TCCR1B |= (1 << WGM12);
	//Set CS10 and CS12 bits for 1024 prescaler:
	TCCR1B |= (1 << CS10);
	TCCR1B |= (1 << CS12);
	//Enable timer compare interrupt:
	TIMSK1 |= (1 << OCIE1A);
	sei(); //Enable global interrupts
}

ISR(TIMER1_COMPA_vect)
{
	digitalWrite(LEDPIN, !digitalRead(LEDPIN));
}

void loop()
{

}