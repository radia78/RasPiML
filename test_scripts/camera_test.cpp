#include <opencv2/opencv.hpp>
#include <iostream>
#define VIDHEIGHT 320
#define VIDWIDTH 320

using namespace cv;
using namespace std;

int main()
{
    VideoCapture cap(0); // Open the default video camera
    
    // if you can't open the video camera, then print error
    if (cap.isOpened() == false)
    {
        cout << "Cannot open the video camera" << endl;
        cin.get();
    }   
    
    // set the video resolution
    cap.set(CAP_PROP_FRAME_WIDTH, VIDWIDTH);
    cap.set(CAP_PROP_FRAME_HEIGHT, VIDHEIGHT);
    
    cout << "Resolution of the video: " << VIDWIDTH << " x " << VIDHEIGHT;
    
    string window_name = "My camera feed";
    namedWindow(window_name);
    
    // Infinite loop on the camera feed, unless we press something
    while (true)
    {
        Mat frame; // initialize the frame object
        bool bSuccess = cap.read(frame); // indicate if we can capture frame
        
        // if not we disconnect and break the camera feed loop
        if (bSuccess == false)
        {
            cout << "Video camera is disconnected" << endl;
            cin.get();
            break;
        }
    
        imshow(window_name, frame); // show the frame at the window
        
        if (waitKey(10) == 27) // wait for 10 ms and the esc key to break loop
        {
            cout << "Esc key is pressed by user. Stopping video" << endl;
            break;
        }
    }
    
    return 0;
}
