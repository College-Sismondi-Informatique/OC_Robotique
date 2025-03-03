'''
Gestion télécommande Pour Micro:bit OC Robotique 2025
Auteur·ice : Vincent Namy
Version : 1.0
Date : 3.2.25

'''
from microbit import *
from protocole import *
display.off()

if __name__ == '__main__':
    
    userId = 0
    destId = 1
    
    # Main
    while True:
        sleep(10)
        print("x", pin4.read_analog()//4, "y", pin3.read_analog()//4, "z", pin5.read_digital())
        
        payload = [pin4.read_analog()//4, pin3.read_analog()//4, pin5.read_digital()]
        print("sent : ", send_msg(73,payload,userId, destId))
            


