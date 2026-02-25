from microbit import *
import radio
import music


# ==============================
# PARAMÈTRES À ADAPTER
# ==============================
SOLUTION = 'WWWNES'

ID_VOITURE = 3        # <-- à changer selon le binôme
CANAL = 12
GROUPE = 7
DEADZONE = 100         # zone neutre du joystick
PERIODE = 100         # en ms (10 messages par seconde)

# --- Seuils joystick (à ajuster selon le matériel) ---
HAUT = 600
BAS  = 400
DROITE = 600
GAUCHE = 400

# ==============================
# INITIALISATION RADIO
# ==============================
radio.on()
radio.config(
    channel=CANAL,
    group=GROUPE,
    power=6,
    length=64,
    queue=10
)

# ==============================
# VARIABLES
# ==============================

# ==============================
# FONCTIONS UTILES
# ==============================
def deadzone(valeur):
    """Ramène la valeur à 512 si elle est dans la zone neutre"""
    if abs(valeur - 512) < DEADZONE:
        return 512
    return valeur


def xy_to_orientation(x, y):
    x = deadzone(x)
    y = deadzone(y)
    # --- 1) Diagonales (Y et X actifs ensemble) ---
#     if y > HAUT and x < GAUCHE:
#         display.show(Image.ARROW_NW)
# 
#     elif y > HAUT and x > DROITE:
#         display.show(Image.ARROW_NE)
# 
#     elif y < BAS and x < GAUCHE:
#         display.show(Image.ARROW_SW)
# 
#     elif y < BAS and x > DROITE:
#         display.show(Image.ARROW_SE)

    # --- 2) Directions simples ---
    if y > HAUT: #elif si diagonales
        display.show(Image.ARROW_N)
        return 'N'

    elif y < BAS:
        display.show(Image.ARROW_S)
        return 'S'

    elif x > DROITE:
        display.show(Image.ARROW_E)
        return 'E'

    elif x < GAUCHE:
        display.show(Image.ARROW_W)
        return 'W'

    # --- 3) Zone neutre ---
    else:
        display.show(Image.SQUARE)
        return '0'

# ==============================
# BOUCLE PRINCIPALE
# ==============================
display.show(Image.HAPPY)
position_in_solution = 0
relache = True
while True:
    # Lecture joystick
    x = pin2.read_analog()
    y = pin1.read_analog()
    z = pin5.read_digital()  # 1 = appuyé, 0 = relâché
    
    v = xy_to_orientation(x, y)
    if v == '0':
        relache = True
    else :
        if relache :
            if v == SOLUTION[position_in_solution]:
                position_in_solution+=1
            else: 
                position_in_solution = 0
            print(position_in_solution)
        relache = False
    
    # Victoire
    if position_in_solution == len(SOLUTION):
        music.play(music.FUNK)
        position_in_solution = 0
        
    sleep(PERIODE)

    


