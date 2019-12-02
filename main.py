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
global sleeptime
sleeptime=0.05           #50ms
global turnsleep
turnsleep=0.5
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
           MotorOne = rpi_dc_lib.TB6612FNGDc(AI1 ,AI2 ,PWA ,Freq,True, "motor_one")    # Motorssetup
           if (left_motor["mode"]==1):                                                 #forward
               if (left_motor["speed"]==1):
                   MotorOne.forward(20)
                   print("forward duty cycle of 20")
               elif(left_motor["speed"]==2):
                   MotorOne.foward(40)
                   print("forward duty cycle of 40")
               elif(left_motor["speed"]==3):
                   MotorOne.foward(60)
                   print("forward duty cycle of 60")
               elif(left_motor["speed"]==4):
                   MotorOne.forward(80)
                   print("forward duty cycle of 80")
               elif(left_motor["speed"]==5):
                    MotorOne.foward(100)
                    print("forward duty cycle of 100")
           #time.sleep(sleeptime)
           elif(left_motor["mode"]==2):                                         #backward
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
           elif(left_motor["mode"]==3):
               MotorOne.stop(0)
               print("turn left(left)")
               time.sleep(turnsleep)
               print("turn finished")
           elif(left_mode["mode"]==4):
               print("turn right (left)")
           elif(left_mode["mode"]==0):
               MotorOne.stop(0)
               print("stop(left)")
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
            left_motor["mode"]=3               #mode 3=left turn
            right_motor["mode"]=3
        elif(ch=='d'):
            print("d is detected")
            left_motor["mode"]=4               #mode 4=right turn
            right_motor["mode"]=4
        elif(ch=='i'):
            print("i is detected")
            left_tmp=left_motor.get("speed")+1
            right_tmp=right_motor.get("speed")+1
            left_motor["speed"]=left_tmp
            right_motor["speed"]=right_tmp
        elif(ch=='j'):
            print("j is detected")
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
