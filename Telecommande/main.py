'''
Gestion télécommande Pour Micro:bit OC Robotique 2025
Auteur·ice : Vincent Namy
Version : 1.0
Date : 3.2.25

'''
from math import *
from microbit import *
from protocole import *
import lib_robot_maqueen as mqn
display.off()

# # CONSTANTES
MOTOR_FORWARD = 0
MOTOR_BACKWARD = 1
SPEED = 70

def run(x,y):
    threshold = 0.2
    motor = MOTOR_FORWARD
    if abs(x) <= threshold and  abs(y) <= threshold: # neutral
        g = 0
        d = 0
    elif abs(x) <= threshold: # forward
        g= int(SPEED)
        d= int(SPEED)
        motor =  y < 0
    elif abs(y) <= threshold: # right/left
        g= int((x>0)*SPEED)
        d= int((x<0)*SPEED)
    else:                     # diag
        g= int((0.1 + (x>0)*0.9) * SPEED)
        d= int((0.1 + (x<0)*0.9) * SPEED)
        motor =  y < 0
        
    
    print("Motors :", g*(-2*motor+1),d*(-2*motor+1))
    robot.motorControl(robot.MT_L,motor, g)
    robot.motorControl(robot.MT_R,motor,  d)

if __name__ == '__main__':
    
    userId = 1
    destId = 0
    robot =  mqn.MaqueenPlus()
    lastMsgTime = running_time()
    run(0,0)
    
    # Main
    while True:
        sleep(10)
    
        
        m = receive_msg(userId)
        if m and m.msgId==73 :#and len(m.payload) == 3:
            x = m.payload[0]*2 /255 - 1 # [0;255] --> [-1;1]
            y = m.payload[1]*2 /255 - 1 # [0;255] --> [-1;1]
            z = m.payload[2]
            print("Joystick :", x,y,z)
            run(x,y)
        elif (lastMsgTime - running_time()) > 200:
            run(0,0)
            


