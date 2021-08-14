// Anurag Nag Adoni 
#include <stdio.h>
#include <string.h>
#include <SparkFun_TB6612.h>

using namespace std;
int datafromUser = 0;
String incomingByte;
int ledState = LOW;  
unsigned long previousMillis = 0;  
const long interval = 1000;
const int ledPin =  LED_BUILTIN;

 #define AIN1 3
#define BIN1 7
#define AIN2 4
#define BIN2 8
#define PWMA 5
#define PWMB 6
#define STBY 9

const int offsetA = 1;
const int offsetB = 1;

Motor motor1 = Motor(AIN1, AIN2, PWMA, offsetA, STBY);
Motor motor2 = Motor(BIN1, BIN2, PWMB, offsetB, STBY);

void setup() {
  Serial.begin(9600);
  pinMode( LED_BUILTIN , OUTPUT );
}

void loop() {
   //brake(motor1,motor2);
   unsigned long currentMillis = millis();
   if (currentMillis - previousMillis >= interval) {
    // save the last time you blinked the LED
    previousMillis = currentMillis;
   }
  
  if(Serial.available()> 0){
    //incomingByte = Serial.read();
    datafromUser = Serial.read();
  }
 
    if(datafromUser == '1'){
       
       motor1.drive(255);
       digitalWrite(LED_BUILTIN, HIGH);
       motor2.brake();
       
        
    }
    else if(datafromUser == '0'){
       
       motor2.drive(255);
       digitalWrite(LED_BUILTIN, LOW);
       motor1.brake();
    }
    else{
      
    }

}
