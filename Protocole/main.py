'''
Protocole Réseau Pour Micro:bit OC Robotique 2025
Fichier de test de la lib protocole
Auteur·ice : Vincent Namy
Version : 2.0
Date : 10.02.26

'''
from protocole import *

mon_id = ...
role = ...


while True:      
    if role == "expediteur":
        data = str_to_list("...")
        id_msg = ...
        dest_id = ...
        
        print("Envoi msg", envoi_message(dest_id, mon_id, id_msg, data))
        sleep(1000)
        

    elif role == "destinataire":
        id_dest, id_exped, id_category, payload, seqNum = reception_message(mon_id)
        
        if id_dest != None:
            print("Message", seqNum,"pour", id_dest,"de",  id_exped, "-- type", id_category, "-- Contenu :", list_to_str(payload))
            display.scroll(list_to_str(payload))
        sleep(200)

