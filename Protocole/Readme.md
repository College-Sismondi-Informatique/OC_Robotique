# Protocole OC-Robotique Sismondi

Librairie de protocole réseau pour micro:bit en microPython avec :
* Destinataire, expéditeur
* Acquittement et réenvoi jusqu'à timeout
* Somme de contrôle
* Encryption AES

Librairie créée pour un TP de l'OC Robotique du collège Sismondi.

## Fichiers
* protocole.py : Version finale de la librairie protocole
* main.py : exemple d'utilisation pour déclencher un smiley ou du son
* template.py : fichier de base pour implémentation du protocole pour les élèves 
* correction_Etape_X.py : corrections des étapes incrémentales du TP 
* aes_full.py : Implémentation de AES issue de https://github.com/boppreh/aes/tree/master adaptée pour microPython
* aes.py : version allégée de aes_full.py. Ces 2 fichiers ne sont nécessaires que si on passe Encryption à True dans protocole.py

## Utilisation

```python
from protocole import *

userId = 1
destId = 0
    while True:
        # Messages à envoyer
        if button_a.was_pressed():
            print(send_msg(1, [60, 45], userId, destId))            

                
        # Reception des messages
        m = receive_msg(userId)
        if m and m.msgId==1 and len(payload)==2:
            print(m.msgStr())
            print("Message de type 1, contenu : ", m.payload[0], m.payload[1])
```