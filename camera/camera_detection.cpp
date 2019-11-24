#include "cv.h"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/video/video.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/imgcodecs/imgcodecs.hpp"
#include <iostream>
#include <stdio.h>

using namespace cv;
using namespace std;

#define KERNEL_WIDTH 3
#define KERNEL_HEIGHT 3
#define SIGMAX 15
#define SIGMAY 15
#define LAP_DEPTH 3

Mat process_blur (Mat* frame)
{
    Mat after_blur_frame;
    
    GaussianBlur(*frame, after_blur_frame, Size(KERNEL_WIDTH, KERNEL_HEIGHT), SIGMAX, SIGMAY);
    return after_blur_frame;
}

Mat process_laplacian (Mat* frame)
{
    Mat after_dxx_frame;
    Laplacian(*frame, after_dxx_frame, CV_8U, LAP_DEPTH, 1, 0, BORDER_DEFAULT);
    return after_dxx_frame;
}

/*
void process_ncc()
{
        
}  */

int main(int argc, char *argv[])
{
   VideoCapture capture;
   capture.open(0);    
   Mat original_frame;
   Mat blurred_frame;
   Mat result_frame;
   
   while (1)
   {
      capture >> original_frame;
      if(original_frame.empty())
        break;
            
      blurred_frame = process_blur(&original_frame);      
      result_frame = process_laplacian(&blurred_frame);
      
      imshow("camera", result_frame);
      waitKey(1);
    }
}
