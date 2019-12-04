import time
from threading import Thread
import RPi.GPIO as GPIO
from RpiMotorLib import rpi_dc_lib      #import motor board libarary
import sys,os

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

def left_motor_thread():
      global l
      global exit_flag
      global modes
      rpi_dc_lib.TB6612FNGDc.standby(Standby, True)
      MotorOne = rpi_dc_lib.TB6612FNGDc(AI1 ,AI2 ,PWA ,Freq,True, "motor_one")    # Motorssetup
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
                              print("forward duty cycle of 20")
                        elif(left_motor["speed"]==2):
                              MotorOne.forward(40)
                              print("forward duty cycle of 40")
                        elif(left_motor["speed"]==3):
                              MotorOne.forward(60)
                              print("forward duty cycle of 60")
                        elif(left_motor["speed"]==4):
                              MotorOne.forward(80)
                              print("forward duty cycle of 80")
                        elif(left_motor["speed"]==5):
                              MotorOne.forward(100)
                              print("forward duty cycle of 100")
                    elif(left_motor["mode"]==2):                                   #backward
                        if (left_motor["speed"]==1):
                              MotorOne.backward(20)
                              print("backward duty cycle of 20")
                        elif(left_motor["speed"]==2):
                              MotorOne.backward(40)
                              print("backward duty cycle of 40")
                        elif(left_motor["speed"]==3):
                              MotorOne.backward(60)
                              print("backward duty cycle of 60")
                        elif(left_motor["speed"]==4):
                              MotorOne.backward(80)
                              print("backward duty cycle of 80")
                        elif(left_motor["speed"]==5):
                              MotorOne.backward(100)
                              print("backward duty cycle of 100")
                    elif(left_motor["mode"]==0):
                        MotorOne.stop(0)
                else:
                    print("in mode 2(left)")
            else:
                  quit()

def right_motor_thread():
      global r
      global exit_flag
      global modes
      MotorTwo = rpi_dc_lib.TB6612FNGDc(BI1 ,BI2 ,PWB ,Freq ,True, "motor_two")   #Motorsetup
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
                              print("forward duty cycle of 20")
                        elif(right_motor["speed"]==2):
                              MotorTwo.forward(40)
                              print("forward duty cycle of 40")
                        elif(right_motor["speed"]==3):
                              MotorTwo.forward(60)
                              print("forward duty cycle of 60")
                        elif(right_motor["speed"]==4):
                              MotorTwo.forward(80)
                              print("forward duty cycle of 80")
                        elif(right_motor["speed"]==5):
                              MotorTwo.forward(100)
                              print("forward duty cycle of 100")
                    elif(right_motor["mode"]==2):                                   #backward
                        if (right_motor["speed"]==1):
                              MotorTwo.backward(20)
                              print("backward duty cycle of 20")
                        elif(right_motor["speed"]==2):
                              MotorTwo.backward(40)
                              print("backward duty cycle of 40")
                        elif(right_motor["speed"]==3):
                              MotorTwo.backward(60)
                              print("backward duty cycle of 60")
                        elif(right_motor["speed"]==4):
                              MotorTwo.backward(80)
                              print("backward duty cycle of 80")
                        elif(right_motor["speed"]==5):
                              MotorTwo.backward(100)
                              print("backward duty cycle of 100")
                     elif(right_motor["mode"]==0):
                        MotorTwo.stop(0)
                else:
                    print("in mode 2(right)")
            else:
                  quit()

def keyboard_pressed():
      global l
      global r
      global exit_flag
      global modes
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
            if (left_motor.get("speed")<=0):     #if at minimum speed
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

key_pressed.start()
left_control.start()
right_control.start()
