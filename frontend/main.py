import player as Player
from player import *
import dragon as Dragon
from dragon import *
import notes as Notes
from notes import *
import time

end = False
pu = [False, False, False]
dra = Dragon()
plr = Player()

while not end: 
    #play song
    Notes.getNotes()
    t_end = time.time() + 30
    while time.time() < t_end:
        # if notes.checkNote():
            #run animation
            dra.redHealth(1*plr.getMult())
            if not dra.checkAlive:
                end = True
        # elif not notes.checkNote():
            if not plr.usingShield():   
                plr.redHealth()
                plr.resetShield()
            if(plr.getHealth()==0 and plr.getPotion()):
                  plr.fullHealth()
    t_end = time.time() + 5
    while (time.time() < t_end) and end == False:
        for i in range(3):
            if(dra.getHealth()<=50 and pu[i]==False):
                plr.newPowerUp()
                pu[i] = True
                break
        # if shield clicked: 
            plr.usingShield()
        else:
            plr.resetShield()
        # if potion clicked: 
            plr.usePotion()
        # if combo clicked: 
            plr.useCombo()
        else:
            plr.resetCombo()


    