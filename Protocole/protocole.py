'''
Protocole Réseau Pour Micro:bit OC Robotique 2025
Auteur·ice : Vincent Namy
Version : 1.0
Date : 28.1.25

TODO :
- plusieurs messages
- passer trame en bytes ?
- doc string
- template
- Encryption
'''

#### Libraries ####
from microbit import *
import radio

#### Variables globales ####
seqNum = 0
tryTime = 100
Timeout = 300
ackMsgId = 0

#### Start radio module ####
radio.config(channel=7, address=50)
radio.on()


#### Classe Message ####
class Message:
  def __init__(self, dest:int, exped:int, seqNum:int, msgId:int, payload:List[int], crc:int):
    self.exped = exped
    self.dest = dest
    self.seqNum = seqNum
    self.payload = payload
    self.crc = crc
    self.msgId = msgId
  def msgStr(self):
      return "[n" + str(self.seqNum)+ "] "+ str(self.exped)+ " -> "+ str(self.dest)+ " : type "+ str(self.msgId)+" : " +str(self.payload)+ " (crc="+ str(self.crc)+")"

#### Toolbox ####
def bytes_to_int(bytesPayload:bytes):
    intPayload = []
    for i in bytesPayload:
        intPayload.append(ord(bytes([i])))        
    return intPayload

def int_to_bytes(intPayload:List[int]):    
    return bytes(intPayload)


#### Fonctions réseaux ####
def msg_to_trame(rawMsg : Message):
    l = [rawMsg.dest, rawMsg.exped, rawMsg.seqNum, rawMsg.msgId] + rawMsg.payload
    rawMsg.crc = sum(l)%255  # ?
    return l + [rawMsg.crc]


def trame_to_msg(trame : List[int], userId :int):
    msgObj = Message(trame[0], trame[1], trame[2], trame[3], trame[4:-1], trame[-1])
    if msgObj.crc == sum(trame[:-1])%255:
        if msgObj.dest != userId :
#             print("Not for me")
            return None
        else:
#             print(msgObj.msgStr())
            return msgObj
    
    
def ack_msg(msg : Message):
    ack = [msg.exped, msg.dest, msg.seqNum, ackMsgId]
    ack += [sum(ack)%255]
    radio.send_bytes(bytes(ack))
    print(ack)
    sleep(100)


def receive_ack(msg: Msg):
    new_trame = radio.receive_bytes()
    if new_trame:
        msgRecu = trame_to_msg(bytes_to_int(new_trame), msg.exped)
#         print("Reçu Ack : ", msgRecu.msgStr())
        return msgRecu.exped == msg.dest and msgRecu.dest == msg.exped and msgRecu.seqNum == msg.seqNum and msgRecu.msgId == ackMsgId
    else:
        return False
    

def send_msg(msgId, payload: List[int], userId:int, dest:int):
    global seqNum
    
    msg = Message(dest, userId, seqNum, msgId, payload,0)
    
    acked = False
    t0 = running_time()
    print("Envoyé : ", msg.msgStr())
    
    while not acked and running_time()-t0 < Timeout:
        print("envoi")
        radio.send_bytes(bytes(msg_to_trame(msg)))
        sleep(tryTime//2)
        display.clear()
        sleep(tryTime//2)
        acked = receive_ack(msg)
        print("acked : ", acked)
        #print(running_time()-t0)
        
    seqNum += 1
    return acked

def receive_msg(userId:int):
    new_trame = radio.receive_bytes()
    if new_trame:
        msgRecu = trame_to_msg(bytes_to_int(new_trame), userId)
        #print("Reçu : ", msgRecu.msgStr())
        if msgRecu.msgId != ackMsgId:
            ack_msg(msgRecu)
            return msgRecu


if __name__ == '__main__':
    
    userId = 0

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
    
