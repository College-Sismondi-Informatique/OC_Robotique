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
    return [i.to_bytes(length=2, byteorder="little")  for i in payload]

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
     
    return [int.from_bytes(b, byteorder="little") for b in bytesPayload]   

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
    def send_int(self,a:int):
        self.send_bytes(list_to_bytes(a))
        
    @classmethod    
    def receive_int(self):
        return bytes_to_list(self.receive_bytes())
    
    @classmethod
    def send(self,a):
        self.msg = a
        
    @classmethod    
    def receive(self):
        m = self.msg
        self.msg = None
        return m
    

if __name__ == '__main__':
#     from microbit_radio_simu import *

    data = [12, 60000]
    radio.send_int(data)
    print(radio.receive_int())
    print(radio.receive_int())

