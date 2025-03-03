import serial
from turtle import * 

# Configuration du port série
port = "/dev/ttyACM1"
baudrate = 115200
bytesize = serial.EIGHTBITS
parity = serial.PARITY_NONE
stopbits = serial.STOPBITS_ONE
timeout = 1

# Ouverture du port série
ser = serial.Serial(port, baudrate, bytesize, parity, stopbits, timeout)
penup()
lastZ = 0
ecrire = False
while True:
   # Lecture des données disponibles sur le port série
   line = ser.readline().decode()
   
   # Affichage des données reçues
   if line and len(line)>1:
       s = line.split()
       if len(s)>5:
           x= int(s[1])-(512+16)
           y= int(s[3])-(512-4)
           z = int(s[5])
           print(x, y)
           if z and not lastZ:
               ecrire = not ecrire
               if ecrire :
                   pendown()
               else:
                   penup()
           goto(xcor()+x//10, ycor()+y//10)
           lastZ = z
       