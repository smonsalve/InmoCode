import pigpio
import time
from Tkinter import *
from threading import Thread
import wiringpi2 as wiringpi

gpio = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_GPIO)
gpio.pinMode(17, 1) 

w = Tk()
w.title("Prueba 1")
w.geometry("280x180")
var = StringVar()
var2 = StringVar()

mycolor = ""

class decoder:

   """
   A class to read Wiegand codes 
   """

   def __init__(self, pi, gpio_0, gpio_1, callback, bit_timeout=5):

      self.pi = pi
      self.gpio_0 = gpio_0
      self.gpio_1 = gpio_1

      self.callback = callback

      self.bit_timeout = bit_timeout

      self.in_code = False

      self.pi.set_mode(gpio_0, pigpio.INPUT)
      self.pi.set_mode(gpio_1, pigpio.INPUT)

      self.pi.set_pull_up_down(gpio_0, pigpio.PUD_UP)
      self.pi.set_pull_up_down(gpio_1, pigpio.PUD_UP)

      self.cb_0 = self.pi.callback(gpio_0, pigpio.FALLING_EDGE, self._cb)
      self.cb_1 = self.pi.callback(gpio_1, pigpio.FALLING_EDGE, self._cb)

   def _cb(self, gpio, level, tick):

      """
      Accumulate bits until both gpios 0 and 1 timeout.
      """

      if level < pigpio.TIMEOUT:

         if self.in_code == False:
            self.bits = 1
            self.num = 0

            self.in_code = True
            self.code_timeout = 0
            self.pi.set_watchdog(self.gpio_0, self.bit_timeout)
            self.pi.set_watchdog(self.gpio_1, self.bit_timeout)
         else:
            self.bits += 1
            self.num = self.num << 1

         if gpio == self.gpio_0:
            self.code_timeout = self.code_timeout & 2 # clear gpio 0 timeout
         else:
            self.code_timeout = self.code_timeout & 1 # clear gpio 1 timeout
            self.num = self.num | 1

      else:

         if self.in_code:

            if gpio == self.gpio_0:
               self.code_timeout = self.code_timeout | 1 # timeout gpio 0
            else:
               self.code_timeout = self.code_timeout | 2 # timeout gpio 1

            if self.code_timeout == 3: # both gpios timed out
               self.pi.set_watchdog(self.gpio_0, 0)
               self.pi.set_watchdog(self.gpio_1, 0)
               self.in_code = False
               self.callback(self.bits, self.num)

   def cancel(self):

      """
      Cancel the Wiegand decoder.
      """

      self.cb_0.cancel()
      self.cb_1.cancel()

def callback(bits, value):
   #print("bits={} value={}".format(bits, value))
   value1 = ((value >> 17) & 0xFF)
   value2 = ((value >> 1) & 0xFFFF)
   #print("Facility code = %s" %value1)
   #print("User code = %s" %value2)
   var.set("Facility code: "+str(value1))
   var2.set("User code: "+str(value2))
   #print bin(value)

def color(r, v, a):
   global mycolor
   mycolor = "#%02x%02x%02x" % (r, v, a)
   return mycolor
   
def encender():
   gpio.digitalWrite(17, 1)
            
def apagar():
   gpio.digitalWrite(17, 0)
   
def salir():
    wieg.cancel()
    w.quit()
 
def ejecutar(f):
   w.after(200,f)

      
imagen = PhotoImage(file="/home/pi/logo.gif")
lb = Label(w, image=imagen, width=280, height=180, anchor="c")
lb.pack()
lb.place(x=0, y=0)

bt1 = Button(w, text="ON", command=lambda:ejecutar(encender()), 
font=("Arial Black", 9), bg=color(183, 190, 39), fg=color(0, 40, 90))
bt1.pack()
bt1.place(x=120, y=38)

bt2 = Button(w, text="OFF", command=lambda:ejecutar(apagar()),
font=("Arial Black", 9), bg=color(183, 190, 39), fg=color(0, 40, 90))
bt2.pack()
bt2.place(x=190, y=38)

bt3 = Button(w, text="X", command=lambda:ejecutar(salir()),
font=("Arial Black", 7), width=2, bg=color(183, 190, 39), fg=color(0, 40, 90))
bt3.pack()
bt3.place(x=0, y=155)

lb1 = Label(w, textvariable=var, font=("Arial Black", 9), 
bg=color(210, 213, 60), fg=color(0, 40, 90))
var.set("Facility code: ")
lb1.pack()
lb1.place(x=116, y=130)

lb2 = Label(w, textvariable=var2, font=("Arial Black", 9), 
bg=color(210, 213, 60), fg=color(0, 40, 90))
var2.set("User code: ")
lb2.pack()
lb2.place(x=116, y=150)

pi = pigpio.pi()

wieg = decoder(pi, 23, 22, callback)

w.mainloop()


   
