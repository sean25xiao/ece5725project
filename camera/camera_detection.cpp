#include "cv.h"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/video/video.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/imgcodecs/imgcodecs.hpp"
#include <iostream>
#include <stdio.h>

using namespace cv;
using namespace std;

#define RESIZE_WIDTH 64*4
#define RESIZE_HEIGHT 48*4
#define RESIZE_TEMP_WIDTH 64
#define RESIZE_TEMP_HEIGHT 48
#define KERNEL_WIDTH 3
#define KERNEL_HEIGHT 3
#define SIGMAX 15
#define SIGMAY 15
#define LAP_DEPTH 3
#define DETECT_THRESHOLD 0.41

Mat process_resize (Mat* frame)
{
    Mat after_resize_frame;
    
    resize(*frame, after_resize_frame, Size(RESIZE_WIDTH, RESIZE_HEIGHT));    
    return after_resize_frame;
}

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

Mat process_ncc (Mat* frame, Mat* temp, Mat* original_frame)
{
    Mat after_ncc_frame;
    double minValue, maxValue;
    Point minLocation, maxLocation, matchLocation;
    
    int after_ncc_frame_cols = (*frame).cols - (*temp).cols + 1;
    int after_ncc_frame_rows = (*frame).rows - (*temp).rows + 1;
    after_ncc_frame.create(after_ncc_frame_rows, after_ncc_frame_cols, CV_32FC1);
    
    matchTemplate(*frame, *temp, after_ncc_frame, CV_TM_CCORR_NORMED);
    //normalize(after_ncc_frame, after_ncc_frame, 0, 1, NORM_MINMAX, -1, Mat());
    
    minMaxLoc(after_ncc_frame, &minValue, &maxValue, &minLocation, &maxLocation, Mat());
    matchLocation = maxLocation;
    if (maxValue > DETECT_THRESHOLD)
    {
       rectangle(after_ncc_frame, matchLocation, Point(matchLocation.x + (*temp).cols, matchLocation.y + (*temp).rows), Scalar::all(0), 2, 8, 0);
       rectangle((*original_frame), matchLocation, Point(matchLocation.x + (*temp).cols, matchLocation.y + (*temp).rows), Scalar::all(0), 2, 8, 0);
       system("cd /home/pi/Desktop/ece5725project/camera | ./a.out &");
       cout << "maxValue is " << maxValue << endl;

    }
    //imshow("resized_frame", (*original_frame));
    
    return after_ncc_frame;
}

int main(int argc, char *argv[])
{
   VideoCapture capture;
   capture.open(0);    
   Mat original_frame;
   Mat blurred_frame;
   Mat laplacian_frame;
   Mat result_frame;
   Mat resized_frame;
   Mat temp1; 
   Mat resized_temp1;
   Mat blurred_temp1;
   Mat laplacian_temp1;
   
   const char* test_window = "Template Image";
   namedWindow(test_window, CV_WINDOW_AUTOSIZE);
   
   temp1 = imread("/home/pi/Desktop/ece5725project/camera/stop_sign_4.jpg");
   resize(temp1, resized_temp1, Size(RESIZE_TEMP_WIDTH, RESIZE_TEMP_HEIGHT));
   blurred_temp1 = process_blur(&resized_temp1);
   laplacian_temp1 = process_laplacian(&blurred_temp1);
   //imshow("tmpelate", laplacian_temp1);
   
   
   while (1)
   {
      capture >> original_frame;
      if(original_frame.empty())
        break;
      
      resized_frame = process_resize(&original_frame);      
      //blurred_frame = process_blur(&resized_frame);      
      laplacian_frame = process_laplacian(&resized_frame);
      result_frame = process_ncc(&laplacian_frame, &laplacian_temp1, &resized_frame);
      
      //imshow("result_frame", result_frame);
      imshow("resized frame", resized_frame);
      imshow("original frame", original_frame);
      imshow("laplacian_frame", laplacian_frame);
      imshow("result frame", result_frame);
      waitKey(1);
    }
    capture.release();
    return 0;
}  
