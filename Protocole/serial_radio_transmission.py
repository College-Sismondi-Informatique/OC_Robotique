from microbit import *
import radio
uart.init(baudrate=115200)

while True:
    if uart.any():
        sleep(50)        
        received = uart.read()
        if received:
            radio.send_bytes(received)

    radio_received = radio.receive_bytes()
    if radio_received :
        uart.write(radio_received)
    
            
    
    sleep(50)

