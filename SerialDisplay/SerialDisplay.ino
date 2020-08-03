
// include the library code:
#include <LiquidCrystal.h>

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
int backLight = 10;    // pin 13 will control the backlight

// set variables for button
int buttonState = 0;
int lastButtonState = 0;
bool toggle = true;


void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // initialize the serial communications:
  Serial.begin(115200);
  pinMode(backLight, OUTPUT);
  digitalWrite(backLight, HIGH); // turn backlight on. Replace 'HIGH' with 'LOW' to turn it off.
  // set the intitial state of the button 
  buttonState = digitalRead(A0);
}


void loop()
{
 // print to serial loop
 int charcount;
 boolean secondline;
 if (Serial.available()) {
   delay(100);
   lcd.clear();
   charcount = 0;
   secondline = false;
   while (Serial.available() > 0) {
     if (charcount > 15 && secondline == false ) {
       lcd.setCursor(0,1);
       secondline = true;
     }
     lcd.write(Serial.read());
     charcount++;
   }
 }
 // button loop
 buttonState = digitalRead(A0) ;
 if (buttonState != lastButtonState) {
  if (lastButtonState == 0) {
   if (toggle == true) {
    toggle = false;
    digitalWrite(backLight, HIGH);
   }
   else {
    toggle = true;
    digitalWrite(backLight, LOW);
   }
  }
 }
 lastButtonState = buttonState;
}
