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
    
    userId = 1
    destId = 0
    
    # Main
    while True:
        sleep(10)
        m = receive_msg(userId)
        if m and m.msgId==73:
            print("x", m.payload[0]*4, "y", m.payload[1]*4, "z", m.payload[2])
            


