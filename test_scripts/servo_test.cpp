#include <iostream>
#include <wiringPi.h>
#include <softPwm.h>

#define SERVO 7

using namespace std;

float getPwm(float angle);

int main()
{
	float relative_angle, total_angle = 90.0;
	
	wiringPiSetup(); // Initialize the wiring pi with direct mapping
	softPwmCreate(SERVO, 0, 100); // Initialize the softpwm on GPIO pin 7 with value zero on 50hz

	
	for (int i = 1; i <= 10; i++)
	{
		cout << "Enter the angle: ";
		cin >> relative_angle;
		
		total_angle += relative_angle; // increment the total angle
		// reset the angle if it maxes out
		if (total_angle < 0 || total_angle > 180)
			total_angle = 90; 
				
		// move the servo based on the total angle
		softPwmWrite(SERVO, getPwm(total_angle));
		delay(250);
		softPwmWrite(SERVO, 0);
	}
	
	// reset servo to the middle
    softPwmWrite(SERVO, 14);
    delay(250);
    softPwmWrite(SERVO, 0);
    
    return 0;
}

float getPwm(float angle){return angle/9 + 4;}
