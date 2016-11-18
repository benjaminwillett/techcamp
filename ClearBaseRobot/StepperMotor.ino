/* YourDuino.com Example Software Sketch
   Small Stepper Motor and Driver V1.3 11/30/2013
   http://arduino-direct.com/sunshop/index.php?l=product_detail&p=126
   Shows 4-step sequence, Then 1/2 turn and back different speeds
   terry@yourduino.com */

/*-----( Import needed libraries )-----*/
/*
Example: Connect Arduino Pins 8,9,10,11 to In1,In2,In3,In4

Then software is initialized in 1-3-2-4 sequence:
Stepper small_stepper(STEPS, 8, 10, 9, 11); //Example Software Sketch below.
*/

#define In1 24
#define In2 25
#define In3 26
#define In4 27


#include <Stepper.h>

/*-----( Declare Constants, Pin Numbers )-----*/
//---( Number of steps per revolution of INTERNAL motor in 4-step mode )---
#define STEPS_PER_MOTOR_REVOLUTION 32   

//---( Steps per OUTPUT SHAFT of gear reduction )---
#define STEPS_PER_OUTPUT_REVOLUTION 32 * 64  //2048  

/*-----( Declare objects )-----*/
// create an instance of the stepper class, specifying
// the number of steps of the motor and the pins it's
// attached to

//The pin connections need to be 4 pins connected
// to Motor Driver In1, In2, In3, In4  and then the pins entered
// here in the sequence 1-3-2-4 for proper sequencing
Stepper small_stepper(STEPS_PER_MOTOR_REVOLUTION, In1, In3, In2, In4);


/*-----( Declare Variables )-----*/
int  Steps2Take;
#define MotorSpeed 800
void moveStepper(int rot){
  Steps2Take  =  STEPS_PER_OUTPUT_REVOLUTION / 16;  // Rotate CW 1/16 turn
  if (rot==1){
    Steps2Take=-Steps2Take;
  }  
  small_stepper.setSpeed(MotorSpeed);   
  small_stepper.step(Steps2Take);
}
/*void loop()   //----( LOOP: RUNS CONSTANTLY )----
{
  small_stepper.setSpeed(1);   // SLOWLY Show the 4 step sequence 
  Steps2Take  =  4;  // Rotate CW
  small_stepper.step(Steps2Take);
  delay(2000);

  Steps2Take  =  STEPS_PER_OUTPUT_REVOLUTION / 2;  // Rotate CW 1/2 turn
  small_stepper.setSpeed(800);   
  small_stepper.step(Steps2Take);
  delay(1000);
  
  Steps2Take  =  - STEPS_PER_OUTPUT_REVOLUTION / 2;  // Rotate CCW 1/2 turn  
  small_stepper.setSpeed(800);  // 700 a good max speed??
  small_stepper.step(Steps2Take);
  delay(2000);

}*/
/* --(end main loop )-- */

/* ( THE END ) */
