'''
Simulateur d'envoi et réception de msg microbits en python3 (ou pyodide sur notebooks)
Auteur·ice : Vincent Namy
Version : 1.0
Date : 04.01.26
'''


def list_to_bytes(payload:list[int]):    
    '''
    Convert  List[any] to bytes object via str
            Parameters:
                    payload(List[any]): payload in int format
            Returns:
                    bytesPayload(bytes): payload in bytes format
    '''
    return bytes(payload)

def bytes_to_list(bytesPayload:bytes):
    '''
    Convert bytes object to List[int]
            Parameters:
                    bytesPayload(bytes): payload in bytes format
            Returns:
                    intPayload(List[int]): payload in int format
    '''
    if bytesPayload is None :
        return None
    
    intPayload = []
    for i in bytesPayload:
        intPayload.append(ord(bytes([i])))        
    return intPayload   

class radio:
    msg = None # 1-buffer of bytes          
    
    @classmethod
    def send_bytes(self,a:bytes):
        self.msg = a
        
    @classmethod    
    def receive_bytes(self):
        m = self.msg
        self.msg = None
        return m
    
    @classmethod
    def send(self,a):
        self.msg = a
        
    @classmethod    
    def receive_bytes(self):
        m = self.msg
        self.msg = None
        return m
    

if __name__ == '__main__':
#     from microbit_radio import *

    data = list_to_bytes([12, 42])
    radio.send_bytes(data)
    print(bytes_to_list(radio.receive_bytes()))
    print(bytes_to_list(radio.receive_bytes()))

