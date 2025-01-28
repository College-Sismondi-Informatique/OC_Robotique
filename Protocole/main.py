'''
Protocole Réseau Pour Micro:bit OC Robotique 2025
Auteur·ice : Vincent Namy
Version : 1.0
Date : 28.1.25

TODO :
- Encryption
- passer trame en bytes ?
'''


from protocole import *
import music

userId = 0

while True:
    
    if button_a.was_pressed():
        if send_msg(1,[],userId, 1):
            display.show(Image.HAPPY)
        else:
            display.show(Image.SAD)
            
        sleep(100)
        display.clear()
            

    m = receive_msg(userId)        
    if m and m.msgId==1:
        music.pitch(600, duration=100, pin=pin0)
    elif m and m.msgId==2:
        display.show(Image.SQUARE)

