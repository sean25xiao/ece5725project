import time
from threading import Thread
import RPi.GPIO as GPIO
from RpiMotorLib import rpi_dc_lib      #import motor board libarary

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

#define motor GPIO pins and duty cycle
PWA = 12
AI1 = 18
AI2 = 19
#PWB = 18
#BI1 = 23
#BI2 = 24
Standby = 25

Freq = 50
# end of define GPIO pins

def left_motor_thread():
     if (exit_flag==0):
           print("START")
           rpi_dc_lib.TB6612FNGDc.standby(Standby, True)
           print("motorone tests")
           #print(" TEST: testing motor 1")
           MotorOne = rpi_dc_lib.TB6612FNGDc(AI1 ,AI2 ,PWA ,Freq,True, "motor_one")    # Motorssetup
           print("1. motor forward")
           MotorOne.forward(100)
           time.sleep(3)
     else:
          exit()

def keyboard_pressed():
    print("checking keyboard")
    while True:
        ch=getchar()
        if(ch=='w'):
            print("w is detected")
            left_motor["mode"]=1               #mode 1=forward
            right_motor["mode"]=1              #mode 1=forward
            print("now the left values are",left_motor.values())
            print("now the right values are",right_motor.values())
        elif(ch=='x'):
            print("x is detected")
            left_motor["mode"]=2               #mode 2=backward
            right_motor['mode']=2              #mode 2=backweard
            print("now the left values are",left_motor.values())
            print("now the right values are",right_motor.values())
        elif(ch=='a'):
            print("a is detected")
        elif(ch=='d'):
            print("d is detected")
        elif(ch=='i'):
            print("i is detected")
            left_tmp=left_motor.get("speed")+4
            right_tmp=right_motor.get("speed")+4
            left_motor["speed"]=left_tmp
            right_motor["speed"]=right_tmp
        elif(ch=='j'):
            print("j is detected")
            left_tmp=left_motor.get("speed")-4
            right_tmp=right_motor.get("speed")-4
            left_motor["speed"]=left_tmp
            right_motor["speed"]=right_tmp
        elif(ch=='s'):                         #stop mode set to 0
            print("s is detected")
            left_motor["speed"]=0
            left_motor["mode"]=0
            right_motor["speed"]=0
            right_motor["mode"]=0
        elif(ch=='c'):
            print("exit the program")
            exit_flag=1
            exit()
        else:
            print("not w")

#key_pressed = Thread(target=keyboard_pressed, args=(i,))
print("start of the program")
key_pressed = Thread(target=keyboard_pressed)
t1=Thread(target=left_motor_thread)
print("creat 2 threads")
key_pressed.start()
t1.start()
