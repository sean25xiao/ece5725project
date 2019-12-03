import numpy as np
import cv2 

cap      = cv2.VideoCapture(0)
size     = (64*4, 48*4)
size_tmp = (32, 64)
ncc_threshold = 0.35

template = cv2.imread('/home/pi/Desktop/ece5725project/camera/red_light.jpg', 1)
resized_template = cv2.resize(template, size_tmp, interpolation=cv2.INTER_AREA)
laplacian_template = cv2.Laplacian(resized_template, cv2.CV_8U)
w_tmp, h_tmp = laplacian_template.shape[:-1]
cv2.imshow('template', laplacian_template)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here

    # Display the resulting frame
    resized_frame = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    laplacian_frame = cv2.Laplacian(resized_frame, cv2.CV_8U)
    #cv2.imshow('template', laplacian_template)
    result_frame = cv2.matchTemplate(laplacian_frame, laplacian_template, cv2.TM_CCORR_NORMED)
    
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_frame)
    print(max_val)
    if (max_val > ncc_threshold):
		top_left = max_loc
		bottom_right = (top_left[0] + h_tmp, top_left[1] + w_tmp)
		cv2.rectangle(resized_frame, top_left, bottom_right, 255, 2)
    
    cv2.imshow('laplacian_frame', laplacian_frame)
    cv2.imshow('resized_frame', resized_frame)

    
    if cv2.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
