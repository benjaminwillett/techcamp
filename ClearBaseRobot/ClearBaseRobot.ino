//ultrasonic
const int trig = 22;
const int echo = 23;

#define power 100
//main motor driver
#include <Servo.h>
#include "AdaFruitMotorLib.h"
long PowerL = 0;
long PowerR = 0;


// Declare classes for Servo connectors of the MotorShield.
Servo servo_1;
Servo servo_2;


#define ledPin 53

void setup()
{
  Serial.begin(9600);
  // put your setup code here, to run once:
  InitializeUltrasonic(trig, echo);
  servo_1.attach(SERVO1_PWM);
  servo_2.attach(SERVO2_PWM);
  setupCompass();
  Serial3.begin(115200);  //Bluetooth connection
}

void loop() {
  boolean CorrectDirction[2];
  static long dist[2];
  char State ;
  static int TaskTracker = -1;
  if (TaskTracker < 0) {
    for (int i = 0; i < 3; i++) {
      dist[i] = Seek(i - 1);
      CorrectDirction[i] = (dist[i] > 10) ;
    }
    TaskTracker += 1;

  }
  if (TaskTracker >= 4 ) {
  } else {
  }
  Serial.print("position:");
  Serial.println(TaskTracker);
  //Check bluetooth
  State = ' ';
  if (Serial3.available()) {
    int inByte = Serial3.read();

    State = char(inByte);

  }
  //Check state
  if (State == 's') {
    PowerL = 0;
    PowerR = 0;
    Serial3.print("Stop:");
    Serial3.print(PowerL);
    Serial3.print(",");
    Serial3.println(PowerR);
  } else if (State == 'f') {
    PowerL += 10;
    PowerR += 10;
    Serial3.print("Forward ");
    Serial3.print(PowerL);
    Serial3.print(",");
    Serial3.println(PowerR);
  } else if (State == 'b') {
    PowerL -= 10;
    PowerR -= 10;
    Serial3.print("Backward ");
    Serial3.print(PowerL);
    Serial3.print(",");
    Serial3.println(PowerR);
  } else if (State == 'r') {
    PowerL -= 10;
    PowerR += 10;
    Serial3.print("right ");
    Serial3.print(PowerL);
    Serial3.print(",");
    Serial3.println(PowerR);
  } else if (State == 'l') {
    PowerL += 10;
    PowerR -= 10;
    Serial3.print("left ");
    Serial3.print(PowerL);
    Serial3.print(",");
    Serial3.println(PowerR);
  } else if (State == 'd') {
    Serial3.print("D:");
    for (int i = 0; i < 3; i++) {
      Serial3.print(dist[i]);
      if (i != 2) Serial3.print(",");
      else     Serial3.println("");
    }
  } else if (State == 'p') {
    //  Serial.print("power");
    Serial3.print("P:");
    Serial3.print(PowerL);
    Serial3.print(",");
    Serial3.println(PowerR);
  } else if (State == 'c') {
    //Get bearing
    Serial3.print("C:");
    Serial3.println(GetBearing());
    
  }
  if (TaskTracker < 3) {
    dist[TaskTracker] = Seek(TaskTracker - 1);
    CorrectDirction[TaskTracker] = (dist[TaskTracker] > 10) ;
    //    Serial.print(dist[TaskTracker]);
    //   Serial.print(" ");
    TaskTracker += 1;
  } else {
    dist[1] = Seek(0);
    CorrectDirction[1] = (dist[1] > 10) ;
    TaskTracker = 0;
    //    Serial.print(dist[1]);
    //    Serial.print(" ");
  }

  if ( dist[1] > 10) {
    TwoWheeler(PowerL, PowerR);
    //      Serial3.println("Clear Forward");
  } else {
    TwoWheeler(0, 0);
    //      Serial3.println("Not Clear Stop");
  }


}

