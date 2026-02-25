'''
Protocole Réseau Pour Micro:bit OC Robotique 2025
Fichier de test de la lib protocole
Auteur·ice : Vincent Namy
Version : 2.0
Date : 10.02.26

'''
from protocole import *

mon_id = 1


while True:      
        
#         print("Envoi msg", envoi_message(0, mon_id, 12, [5, 623, 212, 40]))
        

        id_dest, id_exped, id_category, payload, received_seqNum = reception_message(mon_id)
        
        if id_dest != None:
            print("Message", received_seqNum,"pour", id_dest,"de",  id_exped, "-- type", id_category, "-- Contenu :", payload)
            display.scroll(list_to_str(payload))
        sleep(20)

