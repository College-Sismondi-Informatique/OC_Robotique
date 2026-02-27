# Protocole OC-Robotique Sismondi

Librairie de protocole réseau pour micro:bit en microPython avec :
* Destinataire, expéditeur
* Acquittement et réenvoi jusqu'à timeout
* Somme de contrôle
* (Encryption AES)

Librairie créée pour un TP de l'OC Robotique du collège Sismondi.

## Fichiers
* protocole.py : Version simplifiée de la librairie protocole
* main.py : exemple d'utilisation de la librairie
* serial_radio_transmission.py : fichier permettant la communication pc-radio
* aes_full.py : Implémentation de AES issue de https://github.com/boppreh/aes/tree/master adaptée pour microPython
* aes.py : version allégée de aes_full.py. Ces 2 fichiers ne sont nécessaires que si on passe Encryption à True dans protocole.py
* protocole_aes.py : Version plus complexe de la librairie protocole proposant une encryption aes.
* tuto_protocole.ipynb et tuto_protocole_corrige.ipynb : Notebook expliquant pas à pas l'implémentation d'un protocole de communication sécurisé pour micro:bit. Accessible à l'adresse : [Notebook](https://notebook.basthon.fr/?extensions=romd,sequenced,linenumbers&aux=https%3A%2F%2Fraw.githubusercontent.com%2FCollege-Sismondi-Informatique%2FOC_Robotique%2Frefs%2Fheads%2Fmain%2FProtocole%2Fmicrobit_radio_simu.py&kernel=python3&from=https://raw.githubusercontent.com/College-Sismondi-Informatique/OC_Robotique/refs/heads/main/Protocole/tuto_protocole.ipynb#) et [Corrigé](https://notebook.basthon.fr/?extensions=romd,linenumbers&aux=https%3A%2F%2Fraw.githubusercontent.com%2FCollege-Sismondi-Informatique%2FOC_Robotique%2Frefs%2Fheads%2Fmain%2FProtocole%2Fmicrobit_radio_simu.py&kernel=python3&from=https://raw.githubusercontent.com/College-Sismondi-Informatique/OC_Robotique/refs/heads/main/Protocole/tuto_protocole_corrige.ipynb#)

## Utilisation

Pour envoyer un message : 
```python
from protocole import *

userId = 0
destId = 1

print("Envoi msg", envoi_message(destId, userId, 12, [5, 623, 212, 40]))
```

Pour recevoir : 
```python
from protocole import *

userId = 0

while True:      

        id_dest, id_exped, id_category, payload, received_seqNum = reception_message(userId)        
        if id_dest != None:
            print("Message", received_seqNum,"pour", id_dest,"de",  id_exped, "-- type", id_category, "-- Contenu :", payload)
            display.scroll(list_to_str(received_seqNum))

        sleep(20)
```


N.B. : 
* La librairie peut également être appelée en python3.x sur un ordinateur auquel est connecté une carte micro:bit. La libraire enverra alors les paquets via le port série au micro:bit qui les transmettra par radio.
* Il faut pour cela lancer le programme `serial_radio_transmission.py` sur la carte micro:bit et adapter le port série dans la librairie.