seqNum = 0
tryTime = 200
Timeout = 1000
port = '/dev/ttyACM0' #ou 'radio'

############## PAS BESOIN DE COMPRENDRE CECI ###########################################
if port == "radio":
    from microbit import *
    import radio
    def send(trame):
        radio.send_bytes(list_to_bytes(trame))
        
    def receive():
        r= radio.receive_bytes()
        return bytes_to_list(r)
else:
    import serial, time
    ser = serial.Serial(port, 115200, timeout=0.5)
    
    def send(trame):
        ser.write(list_to_bytes(trame))
        
    def receive():
        d=ser.read_until(';'.encode())
        return bytes_to_list(d)
    
    def running_time():
        return time.time()*1000
    
    def sleep(t):
        return time.sleep(t//1000)
    
def list_to_bytes(payload:list[int]):    
    return (','.join(str(x) for x in payload)+';').encode()

def bytes_to_list(bytesPayload:bytes):
    if not bytesPayload :
        return None
    return [float(s) for s in bytesPayload.decode().split(';')[0].split(',')]

def str_to_list(text:str):
    return [ord(c) for c in text]


def list_to_str(liste:list[int]):
    return ''.join([chr(i) for i in liste])
#######################################################################################




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
        send(trame)
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
    send(trame)
    return True

def check_last_message_ack(id_exped):
    # Receive ack
    id_dest_ack, id_exped_ack, id_category_ack, _, received_seqNum = reception_message(id_exped)
    
    # Check ack
    return received_seqNum == seqNum and id_category_ack == 255
    
def reception_message(mon_id):
    # Reception de la trame
    trame = receive()
    
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
    mon_id = 0

    sleep(2000)
    while True:      
            
            print("Envoi msg", seqNum, "reçu" , envoi_message(1, mon_id, 12, [5, 623]))
            

            id_dest, id_exped, id_category, payload, received_seqNum = reception_message(1)
            
            if id_dest != None:
                print("Message", received_seqNum,"pour", id_dest,"de",  id_exped, "-- type", id_category, "-- Contenu :", payload)

            sleep(200)
        
        




