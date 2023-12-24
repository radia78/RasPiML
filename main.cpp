#include <iostream>
#include <wiringPi.h>
#include <softPwm.h>

#define SERVO 7

float getPwm(float angle);

int main()
{
    float relative_angle, total_angle = 90.0;

    wiringPiSetup(); // Initialize the wiring pi with direct mapping
    softPwmCreate(SERVO, 0, 100); // Initialize the softpwm on GPIO pin 7 with value zero on 50hz

    for (int i = 1; i <= 10; i++)
    {
        // Enter the relative angle
        std::cout << "Enter the relative angle: ";
        std::cin >> relative_angle;

        // Add the relative angle and reset if its maxing out
        if (total_angle <= 0 || total_angle >= 180)
        {
            total_angle = 90.0;
        }
        else
        {
            total_angle += relative_angle;
        }

        // Move the servo based on the total angle
        softPwmWrite(SERVO, getPwm(total_angle));
        delay(500);
        softPwmWrite(SERVO, 0);
    }

    // Reset servo
    softPwmWrite(SERVO, 14);
    softPwmWrite(SERVO, 0);
    delay(1000);

    return 0;
}

float getPwm(float angle){return angle/9 + 4;}

