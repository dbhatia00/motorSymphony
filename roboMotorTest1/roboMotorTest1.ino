// defines pins numbers
const int stepPin = 3; 
const int dirPin = 2; 

// here comes a bunch of 'useful' vars; dont mind
int coun;
bool dir=0;
int del;
int a = 440;
int b = 494;
int c = 262;
int d = 294;
int e = 330;
int f = 349;
int g = 392;
int tempo=120;
int oct=1;

void setup() {
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
}
void loop() {
  note(c,150);
  pa(500);
  note(c,150);
  pa(500);
  note(g,150);
  pa(500);
  note(g,150);
  pa(500);
  note(a,150);
  pa(500);
  note(a,150);
  pa(500);
  note(g,300);
  pa(1500);
  
}

void note(int num,long dur) {
  del=1000000/(num*oct);
  dir=!dir;
 digitalWrite(dirPin,dir);
  coun=floor((dur*5*tempo)/del);
  for(int x = 0; x < coun; x++) {
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(del);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(del);
  }

}

void pa(int durp){
  int ker=floor(durp/100)*tempo;
delay(ker);
  
  }
  