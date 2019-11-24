include "cv.h"
#include "highgui.h"

using namespace cv;
using namespace std;

int main(int argc, char** argv) {
    cvNamedWindow("win");

    CvCapture* capture = cvCreateCameraCapture(0);
    IplImage* frame;

    while(1) {
        frame = cvQueryFrame(capture);
        if(!frame) {break};
        cvShowImage("win", frame);

        char c = cvWaitKey(50);
        if(c==27) break;
    }

    cvReleaseCapture(&capture);
    cvDestroyWindow("win");
    return 0;
}
