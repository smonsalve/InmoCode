import time
import serial
from threading import Thread
import json

arduino = serial.Serial('/dev/ttyAMA0', baudrate=115200, timeout=3.0)

class rfidReader(Thread):
    
    def __init__(self, flagL, txt="", txt1=""):
        Thread.__init__(self)
        self.flagL = flagL
        self.txt = txt
        self.txt1 = txt1

    def run(self):
        
        while(self.flagL == True):
            
            while arduino.inWaiting() > 0:
                self.txt = arduino.read(1)
                self.txt1 += self.txt
                if(self.txt == "}"):
                    print self.txt1
                    self.txt1 = ""
                time.sleep(0.0005)
            
            self.txt = ""
            self.txt1 = ""
            arduino.flush()
            
class convertCode:
   
    def __init__(self, rCode, tLOn, tLOff, tChOff, rBike, flag=True, txt=""):
        self.requestCode = rCode
        self.turnLightsOn = tLOn
        self.turnLightsOff = tLOff
        self.turnChargersOff = tChOff
        self.releaseBike = rBike
        self.flag = flag
        self.txt = txt 

    def sendData(self):
        while (rfid.flagL == True):
           
            comando = raw_input('introduce un comando:\n')
                  
            if(comando.startswith("releaseNode") == True):
                comando = comando.strip("releaseNode")
                try:
                    comando1 = int(comando)
                    arduino.write("*"+comando+"$")
                    #print "*" + comando + "$"
                                  
                except ValueError:
                    print "Posicion incorrecta, intente de nuevo"
         
                except:
                    print "Error inesperado"

            elif(comando == w.requestCode):
                arduino.write("*C$")
                time.sleep(1.7)
                arduino.write("*R$")
                #print "*R$"

            elif(comando == w.turnLightsOn):
                arduino.write("*E$")
                #print "*E$"
      
            elif(comando == w.turnLightsOff):
                arduino.write("*A$")
                #print "*A$"

            elif(comando == w.turnChargersOff):
                arduino.write("*C$")
                #print "*C$"
      
            elif(comando == "go_out"):
                rfid.flagL = False
                arduino.close()
                #print rfid.flagL
    
            else:
                print "Codigo incorrecto, intente de nuevo"
            time.sleep(2)

if __name__ == "__main__":

    w = convertCode("requestCode", "turnLightsOn", "turnLightsOff", "turnChargersOff", "releaseNode")
    rfid = rfidReader(True)
    rfid.start()
    w.sendData()
    
    






