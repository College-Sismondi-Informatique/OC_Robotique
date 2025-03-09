'''
Protocole Réseau Pour Micro:bit OC Robotique 2025
Fichier de test de la lib
Auteur·ice : Vincent Namy
Version : 1.0
Date : 28.1.25

'''


from protocole import *
import music

userId = 0


while True:
    
    # Messages à envoyer
    destId = 1
    if button_a.was_pressed():
        send_msg(1,[60],userId, destId)
    elif button_b.was_pressed():
        send_msg(1,[120],userId, destId)
        

            
    # Reception des messages
    m = receive_msg(userId)        
    if m and m.msgId==1:
        print(m.msgStr())
        music.pitch(m.payload[0]*10, duration=100, pin=pin0)
    elif m and m.msgId==2:
        display.show(Image.SQUARE)

