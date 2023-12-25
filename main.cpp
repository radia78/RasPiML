#include <opencv2/opencv.hpp>
#include <iostream>
#include <wiringPi.h>
#include <softPwm.h>

#define SERVO 7 // define macro SERVO to be the pin on the board

using namespace cv; // namespace for opencv module
using namespace std; // namespace for iostream

float getPwm(float angle);
void setupCamera(int vidWidth, int vidHeight);

int main()
{
    // 1. Camera feed is opened and outputs some image array
    // 2. Image array is fed into ML model and converts to relative angle
    // 3. Relative angle is then used to move servo motor
    
    float relative_angle, total_angle = 90.0;
    int vidWidth = 224, int vidHeight = 224;

    wiringPiSetup(); // Initialize the wiring pi with direct mapping
    softPwmCreate(SERVO, 0, 100); // Initialize the softpwm on GPIO pin 7 with value zero on 50hz
    
    // setup the camera feed
    setupCamera(vidWidth, vidHeight);
    
    // infinite loop on the camera feed, unless we press something
    while (true)
    {
        // 1. open the camera feed and capture the image array
        Mat frame; // initialize the frame object
        bool bSuccess = cap.read(frame); // indicate if we can capture frame
        
        // if not we disconnect and break the camera feed loop
        if (bSuccess == false)
        {
            cout << "Video camera is disconnected" << endl;
            cin.get();
            break;
        }
        
        // 2. ML model is gonna get the frame and convert to relative angle
        
        // 3. move the servo based on relative angle
        total_angle += relative_angle;
        // if the total_angle maxes out, reset to 90
        if (total_angle <= 0 || total_angle >= 180)
            total_angle = 90;
            
        // move the servo based on the total angle
        softPwmWrite(SERVO, getPwm(total_angle));
        delay(500);
        softPwmWrite(SERVO, 0)
        
        /* THIS WHOLE SECTION IS GOING TO BE REVISED SINCE WE MIGHT
         * NOT USE A CAMERA FEED WINDOW FOR THIS TO OPERATE */
         
        imshow(window_name, frame); // show the frame at the window
        
        if (waitKey(10) == 27) // wait for 10 ms and the esc key to break loop
        {
            cout << "Esc key is pressed by user. Stopping video" << endl;
            break;
        }
    }
    
    // reset servo
    softPwmWrite(SERVO, 14);
    softPwmWrite(SERVO, 0);
    delay(1000);

    return 0;
}

// function to convert angle to pwm
float getPwm(float angle){return angle/9 + 4;}

// function to setup the camera
void setupCamera(int vidWidth, int vidHeight)
{
    VideoCapture cap(0); // open the default video camera
    
    // if you can't open the video camera, then print error
    if (cap.isOpened() == false)
    {
        cout << "Cannot open the video camera" << endl;
        cin.get();
    }   
    
    // set the video resolution
    cap.set(CAP_PROP_FRAME_WIDTH, vidWidth);
    cap.set(CAP_PROP_FRAME_HEIGHT, vidHeight);
    
    cout << "Resolution of the video: " << vidWidth << " x " << vidHeight;
    
    string window_name = "My camera feed";
    namedWindow(window_name);
}
