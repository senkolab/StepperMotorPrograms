import RPi.GPIO as GPIO 
import time
import sys
import Tkinter as tk

all_pins=[7,11,13,15,31,33,35,37]
control_pins = [31,33,35,37] #first set of gpio pins
control_pins2 = [7,11,13,15] #second set of gpio pins

esttsd=515.000000 #estimated threesixtydegrees in units of full halfstep_seq runs
#degreeto=sys.argv[1]


halfstep_seq_ccw = [ #counter clockwise sequence
  [0,0,0,1] ,
  [0,0,1,1],
  [0,0,1,0],
  [0,1,1,0],
  [0,1,0,0],
  [1,1,0,0],
  [1,0,0,0],
  [1,0,0,1]
]

halfstep_seq_cw=[ #clockwise sequence
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

def resetcb(pingroup):
  GPIO.setmode(GPIO.BOARD)
  
  for pin in pingroup:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

  checka=False #used to turn on/off
  checkb=False #used to turn on/off
  tickera=0 #used to count number of units
  tickerb=0 #used to count number of units
  storage=open("stor.txt","r")# not actually used

  start_pos=storage.read()
  storage.closed
  holder=open("stor.txt","w")

  while checka==False:##this moves screw forward ##probably could've condensed this to one while loop but didn't have the motors to test and don't want to make changes without testing to make sure they don't break anything
    for halfstep in range(8):#goes through each list of 8 lists.
      for pin in range(4): # goes through each list of 4 pins, if pin is 1 activate, otherwise nothing
        GPIO.output(pingroup[pin], halfstep_seq_ccw[halfstep][pin])#gpio output to pingroup[pin](7,11,13,15, etc) either a 1 or 0 according to halfstep_seq_ccw(1 or 0). Because control board is hooked up to 5V from Rpi a 1 sends 5V
      time.sleep(0.001)
    holder.seek(0)
    holder.write(str(tickera))
    tickera+=1
    if tickera>300:#estimation of how far it needs to extend from how i have it set up, you might have to change this if you move the system around.
      print("Done forward")
      checka=True
  holder.close()

  while checkb==False:#this moves screw backwards
    for halfstep in range(8):
      for pin in range(4):
        GPIO.output(pingroup[pin], halfstep_seq_cw[halfstep][pin])
      time.sleep(0.001)
    tickerb+=1
    if tickerb>=300:
      print("Done backwards")
      checkb=True
  GPIO.cleanup()

top=tk.Tk()
start=tk.Button(top,text="Press to Start",command=lambda : resetcb(control_pins))#button to click to run command to click start button irl
stop=tk.Button(top,text="Press to Stop",command=lambda : resetcb(control_pins2))# button to click to run command to click stop button irl
start.pack()
stop.pack()
top.mainloop()


#unitsto=(esttsd/360.000)*float(degreeto) #turns given degree change into units to be used
