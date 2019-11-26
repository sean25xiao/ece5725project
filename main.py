import time
from threading import Thread

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


def count(num):
     if (exit_flag==0):
         num+=1
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
t1=Thread(target=count,args=(1,))
print("creat 2 threads")
key_pressed.start()
t1.start()
