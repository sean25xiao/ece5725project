import time
from threading import Thread
import RPi.GPIO as GPIO
from RpiMotorLib import rpi_dc_lib      #import motor board libarary
import sys,os
import numpy as np
import cv2 
import subprocess
#from .start_cv import start_cv
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#import object_detection

#This grtchar code is from github repo, however with a problem that can not
#catch ctrl+C signal
def getchar():
   #Returns a single character from standard input
   import tty, termios, sys
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   return ch

#define global varibles
global exit_flag
exit_flag=0
global left_motor
left_motor={'speed':0,'mode':0}
global right_motor
right_motor={'speed':0,'mode':0}
global sleeptime
sleeptime=0.05           #50ms
global turnsleep
turnsleep=0.5
global l
l=0
global r
r=0
global modes
modes=0
global ncc_result
ncc_result = 0
global straight_line_speed
straight_line_speed = 25
global turning_speed
turning_speed = 100
global cv_flag
cv_flag = 0
#define motor GPIO pins and duty cycle
PWA = 12
AI1 = 18
AI2 = 19
PWB = 13
BI1 = 22
BI2 = 23
Standby = 25
Freq = 50
# end of define GPIO pins

#define another set of GPIO pins
PWA_2=4 
AI1_2=5
AI2_2=6
PWB_2=24
BI1_2=20
BI2_2=21
Standby_2=27
Freq_2=50

global cv_process
cv_process = subprocess.Popen(["./start_cv.sh"])

def web_data_thread():
      global left_motor
      global right_motor
      global l
      global r
      FIFO_PATH = '/home/pi/Desktop/ece5725project/web_control_fifo'
      while True:
            with open(FIFO_PATH, 'r') as fifo:
                  print("FIFO opened!")
                  while True:
                        data = fifo.read()
                        if len(data) == 0:
                              print("write closed")
                              break
                        else:
                              print('Read: "{0}"'.format(data))
                              if   (data == 'w'):
                                    left_motor["mode"] = 0
                                    right_motor["mode"] = 0
                                    time.sleep(0.5)
                                    left_motor["mode"] = 1
                                    right_motor["mode"] = 1
                              elif (data == 's'):
                                    left_motor["mode"] = 0
                                    right_motor["mode"] = 0
                              elif (data == 'x'):
                                    left_motor["mode"] = 0
                                    right_motor["mode"] = 0
                                    time.sleep(0.5)
                                    left_motor["mode"] = 2
                                    right_motor["mode"] = 2
                              elif (data == 'i'):
                                    left_motor["speed"] =  left_motor["speed"] + 1
                                    right_motor["speed"] = right_motor["speed"] + 1
                              elif (data == 'j'):
                                    left_motor["speed"] =  left_motor["speed"] - 1
                                    right_motor["speed"] = right_motor["speed"] - 1
                              elif (data == 'a'):
                                    l = 1
                              elif (data == 'd'):
                                    r = 1

def cv_data_thread():
      global cv_flag
      #global left_motor
      FIFO_PATH_CV = '/home/pi/Desktop/ece5725project/cv_fifo'
      #cmd = 'cd /home/pi/Desktop/ece5725project/camera | ./camera_detection'
      #subprocess.run(["cd /home/pi/Desktop/ece5725project/camera/"])
      #subprocess.run(["./start_cv.sh"])
      #exec('start_cv')
      while True:
            with open(FIFO_PATH_CV, 'r') as fifo_cv:
                  print("FIFO opened!")
                  while True:
                        data_cv = fifo_cv.read()
                        if len(data_cv) == 0:
                              print("write closed")
                              break
                        else:
                              print('Read: "{0}"'.format(data_cv))
                              print("where are youuuuuuu")
                              #left_motor["mode"] = 0
                              cv_flag = 1
                              time.sleep(1)
                              cv_flag = 0
                              time.sleep(6)


def camera_part_thread():
      global modes
      while True:
            if (modes==2):
            #ncc_result=object_detection.object_detect()
            #print("ncc_result is ", ncc_result)
                  cap      = cv2.VideoCapture(0)
                  size     = (64*4, 48*4)
                  size_tmp = (32, 64)
                  ncc_threshold = 0.35
                  return_value = 0
      
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
                              return_value = 1
                  
                        #cv2.imshow('laplacian_frame', laplacian_frame)
                        cv2.imshow('resized_frame', resized_frame)
            
                        if cv2.waitKey(1) == ord('q'):
                              break
                  # When everything done, release the capture
                  cap.release()
                  cv2.destroyAllWindows()

def left_motor_thread():
      global l
      global exit_flag
      global modes
      rpi_dc_lib.TB6612FNGDc.standby(Standby, True)
      rpi_dc_lib.TB6612FNGDc.standby(Standby_2, True)
      
      MotorOne = rpi_dc_lib.TB6612FNGDc(AI1 ,AI2 ,PWA ,Freq,True, "motor_one")    # Motorssetup
      MotorThree=rpi_dc_lib.TB6612FNGDc(AI1_2 ,AI2_2 ,PWA_2 ,Freq_2,True, "motor_three") 
      while True:
            if (exit_flag==0):
                if (modes==0):
                    if (l==1):
                        MotorOne.stop(0)
                        print("turn left(left)")
                        time.sleep(turnsleep)
                        print("turn finished")
                        l=0
                    elif (left_motor["mode"]==1):                                  #forward
                        if (left_motor["speed"]==1):
                              MotorOne.forward(20)
                              MotorThree.forward(20)
                              print("forward duty cycle of 20")
                        elif(left_motor["speed"]==2):
                              MotorOne.forward(40)
                              MotorThree.forward(40)
                              print("forward duty cycle of 40")
                        elif(left_motor["speed"]==3):
                              MotorOne.forward(60)
                              MotorThree.forward(60)
                              print("forward duty cycle of 60")
                        elif(left_motor["speed"]==4):
                              MotorOne.forward(80)
                              MotorThree.forward(80)
                              print("forward duty cycle of 80")
                        elif(left_motor["speed"]==5):
                              MotorOne.forward(100)
                              print("forward duty cycle of 100")
                    elif(left_motor["mode"]==2):                                   #backward
                        if (left_motor["speed"]==1):
                              MotorOne.backward(20)
                              MotorThree.backward(20)
                              print("backward duty cycle of 20")
                        elif(left_motor["speed"]==2):
                              MotorOne.backward(40)
                              MotorThree.backward(40)
                              print("backward duty cycle of 40")
                        elif(left_motor["speed"]==3):
                              MotorOne.backward(60)
                              MotorThree.backward(60)
                              print("backward duty cycle of 60")
                        elif(left_motor["speed"]==4):
                              MotorOne.backward(80)
                              MotorThree.backward(80)
                              print("backward duty cycle of 80")
                        elif(left_motor["speed"]==5):
                              MotorOne.backward(100)
                              MotorThree.backward(100)
                              print("backward duty cycle of 100")
                    elif(left_motor["mode"]==0):
                        MotorOne.stop(0)
                        MotorThree.stop(0)
                else:
                    print("in mode 2(right)")
                    if (cv_flag==0):
                    #MotorFour.stop(0)
                        a=GPIO.input(17)
                        b=GPIO.input(16)
                        if (a==0):
                              if (b==0):
                                    MotorOne.forward(straight_line_speed)
                                    MotorThree.forward(straight_line_speed)
                              else:
                                    MotorOne.forward(turning_speed)
                                    MotorThree.forward(turning_speed)
                        elif(a==1):
                              MotorOne.stop(0)
                              MotorThree.stop(0)
                              #MotorFour.stop(0)
                    else:
                          MotorOne.stop(0)
                          MotorThree.stop(0)
                          time.sleep(3)
                    
            else:
                  quit()

def right_motor_thread():
      global r
      global exit_flag
      global modes
      MotorTwo = rpi_dc_lib.TB6612FNGDc(BI1 ,BI2 ,PWB ,Freq ,True, "motor_two")   #Motorsetup
      MotorFour = rpi_dc_lib.TB6612FNGDc(BI1_2,BI2_2 ,PWB_2,Freq_2 ,True, "motor_four")   #Motorsetup
      while True:
            if (exit_flag==0):
                if(modes==0):
                    if (r==1):
                        MotorTwo.stop(0)
                        print("turn right(right)")
                        time.sleep(turnsleep)
                        print("turn finished")
                        r=0
                    elif (right_motor["mode"]==1):                                  #forward
                        if (right_motor["speed"]==1):
                              MotorTwo.forward(20)
                              MotorFour.forward(20)
                              print("forward duty cycle of 20")
                        elif(right_motor["speed"]==2):
                              MotorTwo.forward(40)
                              MotorFour.forward(40)
                              print("forward duty cycle of 40")
                        elif(right_motor["speed"]==3):
                              MotorTwo.forward(60)
                              MotorFour.forward(60)
                              print("forward duty cycle of 60")
                        elif(right_motor["speed"]==4):
                              MotorTwo.forward(80)
                              MotorFour.forward(80)
                              print("forward duty cycle of 80")
                        elif(right_motor["speed"]==5):
                              MotorTwo.forward(100)
                              MotorFour.forward(100)
                              print("forward duty cycle of 100")
                    elif(right_motor["mode"]==2):                                   #backward
                        if (right_motor["speed"]==1):
                              MotorTwo.backward(20)
                              MotorFour.backward(20)
                              print("backward duty cycle of 20")
                        elif(right_motor["speed"]==2):
                              MotorTwo.backward(40)
                              MotorFour.backward(40)
                              print("backward duty cycle of 40")
                        elif(right_motor["speed"]==3):
                              MotorTwo.backward(60)
                              MotorFour.backward(60)
                              print("backward duty cycle of 60")
                        elif(right_motor["speed"]==4):
                              MotorTwo.backward(80)
                              MotorFour.backward(80)
                              print("backward duty cycle of 80")
                        elif(right_motor["speed"]==5):
                              MotorTwo.backward(100)
                              MotorFour.backward(100)
                              print("backward duty cycle of 100")
                    elif(right_motor["mode"]==0):
                        MotorTwo.stop(0)
                        MotorFour.stop(0)
                else:
                      if (cv_flag==0):
                            print("in mode 2(right)")
                            #MotorFour.stop(0)
                            a=GPIO.input(17)
                            b=GPIO.input(16)
                            if (b==0):
                                  if (a==0):
                                        MotorTwo.forward(straight_line_speed)
                                        MotorFour.forward(straight_line_speed)
                                  else:
                                        MotorTwo.forward(turning_speed)
                                        MotorFour.forward(turning_speed)
                            elif(b==1):
                                  MotorTwo.stop(0)
                                  MotorFour.stop(0)
                  
                      else:
                            MotorTwo.stop(0)
                            MotorFour.stop(0)
                            time.sleep(3)
            else:
                  quit()

def keyboard_pressed():
      global l
      global r
      global exit_flag
      global modes
      global left_motor
      global right_motor
      global cv_process
      print("checking keyboard")
      while True:
        ch=getchar()
        if(ch=='w'):
            print("w is detected")
            if (left_motor["mode"]==2):
                  left_motor["mode"]=0               #mode 1=forward
                  right_motor["mode"]=0              #mode 1=forward
                  time.sleep(1)
                  left_motor["mode"]=1               #mode 1=forward
                  right_motor["mode"]=1              #mode 1=forward
            else:
                  left_motor["mode"]=1               #mode 1=forward
                  right_motor["mode"]=1              #mode 1=forward
                  print("now the left values are",left_motor.values())
                  print("now the right values are",right_motor.values())
        elif(ch=='x'):
            print("x is detected")
            if (left_motor["mode"]==1):
                  left_motor["mode"]=0               #mode 2=backward
                  right_motor['mode']=0              #mode 2=backweard
                  time.sleep(1)
                  left_motor["mode"]=2               #mode 2=backward
                  right_motor['mode']=2              #mode 2=backweard
            else:
                  left_motor["mode"]=2               #mode 2=backward
                  right_motor['mode']=2              #mode 2=backweard
                  print("now the left values are",left_motor.values())
                  print("now the right values are",right_motor.values())
        elif(ch=='a'):
            print("a is detected")
            l=1
        elif(ch=='d'):
            print("d is detected")
            r=1
        elif(ch=='i'):
            print("i is detected")
            if (left_motor.get("speed")>=5):     #if at maxium speed
                pass
            else:
                left_tmp=left_motor.get("speed")+1
                right_tmp=right_motor.get("speed")+1
                left_motor["speed"]=left_tmp
                right_motor["speed"]=right_tmp
                print("now the left values are",left_motor.values())
                print("now the right values are",right_motor.values())
        elif(ch=='j'):
            print("j is detected")
            if (left_motor.get("speed")<0):     #if at minimum speed
                pass
            else:
                left_tmp=left_motor.get("speed")-1
                right_tmp=right_motor.get("speed")-1
                left_motor["speed"]=left_tmp
                right_motor["speed"]=right_tmp
        elif(ch=='s'):                         #stop mode set to 0
            print("s is detected")
            left_motor["speed"]=0
            left_motor["mode"]=0
            right_motor["speed"]=0
            right_motor["mode"]=0
        elif(ch=='m'):
            print("m is detected")
            if (modes==0):
                modes=1
            else:
                modes=0
                left_motor={'speed':0,'mode':0}                    #initilize motor status
                right_motor={'speed':0,'mode':0}
        elif(ch=='c'):
              print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
              left_motor["speed"]=0
              left_motor["mode"]=0
              right_motor["speed"]=0
              right_motor["mode"]=0
              #MotorOne = rpi_dc_lib.TB6612FNGDc(AI1 ,AI2 ,PWA ,Freq,False, "motor_one")    # Motorssetup
              #MotorTwo = rpi_dc_lib.TB6612FNGDc(BI1 ,BI2 ,PWB ,Freq ,False, "motor_two")
              print("exit the program")
              exit_flag=1
              rpi_dc_lib.TB6612FNGDc.standby(Standby,False)
              GPIO.cleanup()
              print("done!")
              os._exit(1)
        else:
            print("not w")


key_pressed = Thread(target=keyboard_pressed)
left_control= Thread(target=left_motor_thread)
right_control=Thread(target=right_motor_thread)
camera_part=Thread(target=camera_part_thread)
web_data = Thread(target=web_data_thread)
cv_data = Thread(target=cv_data_thread)

key_pressed.start()
left_control.start()
right_control.start()
#camera_part.start()
web_data.start()
cv_data.start()

