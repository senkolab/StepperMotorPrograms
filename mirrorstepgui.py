####Don't know if negative degrees work, can't check cuz no stepper motors to test on. 
import RPi.GPIO as GPIO 
import time
import sys

GPIO.setmode(GPIO.BOARD)
control_pins = [7,11,13,15] #first set of gpio pins
control_pins2 = [29,31,33,35] #second set of gpio pins

checka=False #used to turn on/off
tickera=0 #used to count number of units
esttsd=515.000000 #estimated threesixtydegrees in units of full halfstep_seq runs(estimated from stepper motor resetter, might be different)

degreeto=0 #takes degrees

for pin in control_pins:#Setting up pins on raspberry pi
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)

halfstep_seq_ccw = [ #counter clockwise sequence for stepper motor inputs
  [0,0,0,1] ,
  [0,0,1,1],
  [0,0,1,0],
  [0,1,1,0],
  [0,1,0,0],
  [1,1,0,0],
  [1,0,0,0],
  [1,0,0,1]
]

halfstep_seq_cw=[ #clockwise sequence for stepper motor inputs
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

unitsto=(esttsd/360.000)*float(degreeto) #turns given degree change into units of pin activations to be used

while checka==False:
  for halfstep in range(8):
    for pin in range(4):
      GPIO.output(control_pins[pin], halfstep_seq_ccw[halfstep][pin])
    time.sleep(0.001)
  tickera+=1
  if tickera>unitsto:#Checks how many pins have been activated. If more have been activated than calculated on line 42 checka turns true and while loop ends.
    print("Done")
    checka=True

GPIO.cleanup()

top=tk.Tk()
degreesentry=tk.Entry(top,textvariable=degreesto)
degreesentry.pack()
top.mainloop()
