//Xbee receiver
//This example code is in the Public Domain

int sentDat;
int i;

void setup() 
{
  Serial.begin(9600);   
  pinMode(2, OUTPUT);
  Serial.write("Up");

  while (i < 6)
  {
    digitalWrite(2, HIGH);
    delay(100);
    digitalWrite(2, LOW);
    delay(100);
    i++;
  }
}

void loop() 
{
  if (Serial.available() > 0) 
  {
  	sentDat = Serial.read(); 

  	if(sentDat == 'h')
    {
      Serial.write('h');
      //activate the pumpkin for one second and then stop
  	  digitalWrite(2, HIGH);
      delay(1000);
      digitalWrite(2, LOW);
  	}

    if(sentDat == 'b')
    {
      Serial.write('b');
      digitalWrite(2, HIGH);
      delay(100);
      digitalWrite(2, LOW);
      delay(100);
      digitalWrite(2, HIGH);
      delay(100);
      digitalWrite(2, LOW);
      delay(100);
      digitalWrite(2, HIGH);
      delay(100);
      digitalWrite(2, LOW);
      delay(100);
      digitalWrite(2, HIGH);
      delay(100);
      digitalWrite(2, LOW);
      delay(100);
    }
  }
} 
