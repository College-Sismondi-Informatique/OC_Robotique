from microbit import *
import radio

seqNum = 0
tryTime = 200
Timeout = 1000

def str_to_list(text:str):
    '''Convertit un str en list de int'''
    return [ord(c) for c in text]


def list_to_str(liste:list[int]):
    '''Convertit un str en list de int'''
    return ''.join([chr(i) for i in liste])


def list_to_bytes(payload:list[int]):    
    '''
    Convertit une liste de int en bytes
            Parameters:
                    payload(List[int]): payload in int format
            Returns:
                    bytesPayload(bytes): payload in bytes format
    '''
    return b''.join([i.to_bytes(2, "little")  for i in payload])

def bytes_to_list(bytesPayload:bytes):
    '''
    Convertit des bytes en List[int]
            Parameters:
                    bytesPayload(bytes): payload in bytes format
            Returns:
                    intPayload(List[int]): payload in int format
    '''
    if bytesPayload is None :
        return None
    bytesList = [bytesPayload[i:i+2] for i in range(0, len(bytesPayload), 2)]
    return [int.from_bytes(b, "little") for b in bytesList]   


def envoi_message(id_dest, id_exped, id_category, payload):
    global seqNum
    
    # Construction de la trame
    trame = [id_dest, id_exped, seqNum, id_category] + payload 
    checksum = sum(trame)
    trame = trame + [checksum]
    
    # Envoi + Attente du ack et ré-essai
    acked = False
    t0 = running_time()
    
    while not acked and running_time()-t0 < Timeout:
        radio.send_bytes(list_to_bytes(trame))
        sleep(tryTime)
        acked = check_last_message_ack(id_exped)
        
    seqNum = (seqNum+1)%256
    return acked
    

def envoi_ack(id_dest, id_exped, id_category, payload, ackSeqNum):
    # Construction de la trame
    trame = [id_dest, id_exped, ackSeqNum, id_category] + payload 
    checksum = sum(trame)
    trame = trame + [checksum]
    
    # Envoi
    radio.send_bytes(list_to_bytes(trame))
    return True

def check_last_message_ack(id_exped):
    # Receive ack
    id_dest_ack, id_exped_ack, id_category_ack, _, received_seqNum = reception_message(id_exped)
    
    # Check ack
    return received_seqNum == seqNum and id_category_ack == 255
    
def reception_message(mon_id):
    # Reception de la trame
    trame = bytes_to_list(radio.receive_bytes())
    
    # Deconstruction de la trame
    if trame :
        id_dest = trame[0]
        id_exped = trame[1]
        received_seqNum = trame[2]
        id_category = trame[3]
        payload = trame[4:-1]
        checksum =  trame[-1]

        if mon_id == id_dest and checksum == sum(trame[:-1]) : # On recalcule et compare la somme de contrôle
            if id_category != 255: # Si le message original n'est pas un ack, on envoie un ack
                envoi_ack(id_exped, id_dest, 255, [], received_seqNum)                
            return id_dest, id_exped, id_category, payload, received_seqNum
        
    return None, None, None, None, None # Retourne None en cas d'échec de réception

if __name__ == '__main__':
    while True :
        exp_id = 0
        dest_id  = 1
        if False :
                # Expéditeur
                data = [5, 623, 212, 40]
                id_aruco_msg = 12
                print("Envoi msg", seqNum)
                print(envoi_message(dest_id, exp_id, id_aruco_msg, data))
                sleep(1000)
            
        else:
                # Destinataire
                id_dest, id_exped, id_category, payload, seqNum = reception_message(dest_id)
                if id_dest:
                    print("Message", seqNum,"pour", id_dest,"de",  id_exped, "-- type", id_category, "-- Contenu :", payload)
                sleep(100)
        
        


