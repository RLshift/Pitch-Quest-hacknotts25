import player as Player
from player import *
import dragon as Dragon
from dragon import *
import notes as Notes
from notes import *
import time
import random

import sys, os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from spotify.spotifyAPI import * 
from spotify import spotifyAPI



end = False
pu = [False, False, False]
dra = Dragon()
plr = Player()
songs = ["nights", "stargazing", "dont_stop", "coulda_been_me", "kilby_girl"]


# notes_array = getNotes("nights")
# print(notes_array)


while not end: 
    song_index = random.randint(0,4)
    spotifyAPI.runApp(songs[song_index])
    print("running app")
    #play song from songs[song_index]
    note_array = getNotes(songs[song_index])  
    #show notes animation
    # input = 
    t_end = time.time() + 30
    while time.time() < t_end:
        if checkNotes(note_array, input):
            #run animation
            dra.redHealth(1*plr.getMult())
            if not dra.checkAlive:
                end = True
        elif not checkNotes(note_array, input):
            if not plr.usingShield():   
                plr.redHealth()
            if(plr.getHealth()==0 and plr.getPotion()):
                  plr.fullHealth()
    t_end = time.time() + 5
    while (time.time() < t_end) and end == False:
        
        if(dra.getHealth()<=50 and pu[0]==False):
            plr.newPowerUp()
            pu[0] = True
        elif(dra.getHealth()<=35 and pu[1]==False):
            plr.newPowerUp()
            pu[1] = True
        elif(dra.getHealth()<=15 and pu[2]==False):
            plr.newPowerUp()
            pu[2] = True
            
        # # if shield clicked: 
        #     plr.usingShield()
        # else:
        #     plr.resetShield()
        # # if potion clicked: 
        #     plr.usePotion()
        # # if combo clicked: 
        #     plr.useCombo()
        # else:
        #     plr.resetCombo()



    