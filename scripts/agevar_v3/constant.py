# CONSTANTS

N_MOD = 1           # Number of modules of the robot

#serve ancora? TODO
N_VAR = 7           # Number of kinetic variables 

ANGLE_MAX = 35      # [°] Is the maximum angle between two moduless

FREQ = 50          # [Hz] Is the refresh rate of the program. Is you to determinate the time passed from the previous operation

#serve ancora? TODO
FILE_PATH = "/home/andrea/agevarFiles/modulo_" # Percorso in cui verranno salvarti i file necessari al funzionamento del codice di agevar

ADDRESSES = [ 21, 48, 69 ] # 0x15, 0x30, 0x45

a = 1         # [m] distanza tra il punto centrale del modulo i-esimo e il giunto d'imbardata precedente

b = 1         # [m] distanza tra il punto centrale del modulo i-esimo e il giunto d'imbardata successivo

d = 0.2         # [m] lunghezza dell'interasse tra le due ruote equivalenti

r = 0.05        # [m] raggio delle ruote equivalenti
