import player as Player
from player import *
import dragon as Dragon
from dragon import *
import notes as Notes
from notes import *
import time
import random


end = False
pu = [False, False, False]
dra = Dragon()
plr = Player()
songs = ["nights", "stargazing", "dont_stop", "coulda_been_me", "kilby_girl"]

while not end: 
    song_index = random.randint(0,4)
    #play song from songs[song_index]
    note_array = Notes.getNotes(songs[song_index]) # FIX randomise songs 
    #show notes animation
    input = 
    t_end = time.time() + 30
    while time.time() < t_end:
        if Notes.checkNotes(note_array, #input):
            #run animation
            dra.redHealth(1*plr.getMult())
            if not dra.checkAlive:
                end = True
        elif not Notes.checkNotes(note_array, #input):
            if not plr.usingShield():   
                plr.redHealth()
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


    