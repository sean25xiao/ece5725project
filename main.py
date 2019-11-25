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
            tmp={'speed':1}
            left_motor.update(tmp)
            print("now the values are",left_motor.values())
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
