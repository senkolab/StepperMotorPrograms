import RPi.GPIO as GPIO 
import time
import sys

GPIO.setmode(GPIO.BOARD)
control_pins = [31,33,35,37]
#control_pins = [7,11,13,15] #first set of gpio pins
control_pins2 = [29,31,33,35] #second set of gpio pins

checka=False #used to turn on/off
checkb=False #used to turn on/off
tickera=0 #used to count number of units
tickerb=0 #used to count number of units
esttsd=515.000000 #estimated threesixtydegrees in units of full halfstep_seq runs

degreeto=sys.argv[1] #takes degrees

for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)

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

unitsto=(esttsd/360.000)*float(degreeto) #turns given degree change into units to be used

storage=open("stormir.txt","r")

start_pos=storage.read()
storage.closed


holder=open("stor.txt","w")

while checka==False:
  for halfstep in range(8):
    for pin in range(4):
      GPIO.output(control_pins[pin], halfstep_seq_ccw[halfstep][pin])
    time.sleep(0.001)
  holder.seek(0)
  holder.write(str(tickera))
  tickera+=1
  if tickera>unitsto:
    print("Done")
    checka=True
holder.close()

GPIO.cleanup()