import pyglet
from pyglet.window import mouse

# importing shapes from pyglet library
from pyglet import shapes
import player as Player
from player import *
import dragon as Dragon
from dragon import *
import notes as Notes
from notes import *
import time
import random

#from frontend import main
#from main import *
#import main 
# Canvas
window = pyglet.window.Window(2560, 1440)
batch = pyglet.graphics.Batch()

dra = Dragon()
plr = Player()
songs = ["nights", "stargazing", "dont_stop", "coulda_been_me", "kilby_girl"]

from pyglet import image
start_screen = image.load('images/backgroundStartScreen.png')
gameplay_screen = image.load('images/backgroundGamePlay.png')

songPick = random.choice(songs)
noteArray = Notes.getNotes(songPick)  
dra.setMaxHealth(len(noteArray))
dra.setHealth(len(noteArray))

# At the top with your other variables
user_input = ""
correct_notes = noteArray  # Your expected note sequence
current_note_index = 0

dragonHBRatio = dra.getHealth()/dra.getMaxHealth()

# Use a list to make it mutable in nested functions
game_state = {'started': False}

def get_current_pic():
    if game_state['started']:
        return gameplay_screen
    else:
        return start_screen

pic = get_current_pic()
width, height = pic.width, pic.height

def startButtonAction():
    print("Start Button clicked!")
    
    print(noteArray)
    game_state['started'] = True


startButton = pyglet.image.load('images/startButton.png')
startButtonSprite = pyglet.sprite.Sprite(startButton, 600, y=420)

batch = pyglet.graphics.Batch()
inInventory = pyglet.graphics.Batch()
notActive = pyglet.graphics.Batch()

#depending on pu in playerClass
items = []

#coords, status
powerupP1 = [33,850, plr.pu[0]]
powerupP2 = [33,610, plr.pu[1]]
powerupP3 = [33,370, plr.pu[2]]

flautist = image.load('images/flautist.png')
# dragon = image.load('images/dragon.png')
ani = pyglet.resource.animation('images/dragon.gif')
dragon = pyglet.sprite.Sprite(img=ani)
images = [pyglet.resource.image('images/injury.png'),
          pyglet.resource.image('images/injury brighter.png'),
          pyglet.resource.image('images/injury.png'),
          pyglet.resource.image('images/injury brighter.png')]

ani = pyglet.image.Animation.from_image_sequence(images, duration=0.1, loop=True)
hurting = pyglet.sprite.Sprite(img=ani)
playerHealthFull = image.load('images/playerHealthFull.png')
playerHealthHalf = image.load('images/playerHealthHalf.png')
playerHealthDead = image.load('images/playerHealthDead.png')
shield = image.load('images/shield.png')
potion = image.load('images/potion.png')
doubleDamage = image.load('images/doubleDamage.png')
dragonHealthBarImage = image.load('images/dragonHealthBarBorder.png')
fireball = image.load('images/fireball.png')

                                                                                                                      
#0 = Full, 1 = Half, 2 = Dead, Complete player Health = 6
# Complete player Health = 6
def statusUpdate():

    health = plr.getHealth()

    # Calculate health for each slot (0-2 per slot)
    slot1_health = min(health, 2)
    slot2_health = min(max(health - 2, 0), 2)
    slot3_health = min(max(health - 4, 0), 2)

    # Map health values to images
    healthImages = {0: playerHealthDead, 1: playerHealthHalf, 2: playerHealthFull}

    playerHealthStatus1 = healthImages[slot1_health]
    playerHealthStatus2 = healthImages[slot2_health]
    playerHealthStatus3 = healthImages[slot3_health]

    if plr.pu[0] == True:
        powerUpStatus1 = batch
    else:
        powerUpStatus1 = notActive

    if plr.pu[1] == True:
        powerUpStatus2 = batch
    else:
        powerUpStatus2 = notActive

    if plr.pu[2] == True:
        powerUpStatus3 = batch
    else:
        powerUpStatus3 = notActive
    
    #Initally evrything is set to 60

    dragonHBRatio = dra.getHealth()/dra.getMaxHealth()
    print(dragonHBRatio)

    return playerHealthStatus1, playerHealthStatus2, playerHealthStatus3, powerUpStatus1, powerUpStatus2, powerUpStatus3, dragonHBRatio


flautist = image.load('images/flautist.png')
dragon = image.load('images/dragon.png')
playerHealthFull = image.load('images/playerHealthFull.png')
playerHealthHalf = image.load('images/playerHealthHalf.png')
playerHealthDead = image.load('images/playerHealthDead.png')
shield = image.load('images/shield.png')
potion = image.load('images/potion.png')
doubleDamage = image.load('images/doubleDamage.png')
dragonHealthBarImage = image.load('images/dragonHealthBarBorder.png')
fireball = image.load('images/fireball.png')

# After all your image loads, create these as global variables
flautistSprite = None
dragonSprite = None
playerHealthBackground = None
playerHealthBorder = None
inventoryBackground = None
inventoryBorder = None
inventory1Border = None
inventory2Border = None
inventory3Border = None
dragonHealthBarBorder = None
dragonHealthBar = None
playerHealth1Sprite = None
playerHealth2Sprite = None
playerHealth3Sprite = None
powerup1Sprite = None
powerup2Sprite = None
powerup3Sprite = None

def redraw():
    global flautistSprite, dragonSprite, playerHealthBackground, playerHealthBorder
    global inventoryBackground, inventoryBorder, inventory1Border, inventory2Border, inventory3Border
    global dragonHealthBarBorder, dragonHealthBar
    global playerHealth1Sprite, playerHealth2Sprite, playerHealth3Sprite
    global powerup1Sprite, powerup2Sprite, powerup3Sprite
    
    # Get updated values
    statusUpdateValues = statusUpdate()
    playerHealthStatus1 = statusUpdateValues[0]
    playerHealthStatus2 = statusUpdateValues[1]
    playerHealthStatus3 = statusUpdateValues[2]
    powerUpStatus1 = statusUpdateValues[3]
    powerUpStatus2 = statusUpdateValues[4]
    powerUpStatus3 = statusUpdateValues[5]
    dragonHBRatio = statusUpdateValues[6]

flautistSprite = pyglet.sprite.Sprite(img=flautist, x=380, y=-25, batch=batch)
dragon_animation = pyglet.image.load_animation("images/dragon.gif")
#dragonSprite = pyglet.sprite.Sprite(img=dragon, x=1180, y=450, batch=batch)
playerHealthBackground= shapes.Rectangle(35, 50, 500, 130, color=(164,164,164,180), batch=batch)
playerHealthBorder= shapes.Box(33, 48, 502, 132, thickness=5,color=(87,87,87), batch=batch)

    inventoryBackground= shapes.Rectangle(55, 370, 200, 700, color=(164,164,164,220), batch=batch)
    inventoryBorder= shapes.Box(53, 372, 202, 702, thickness=8,color=(87,87,87), batch=batch)
    inventory1Border= shapes.Box(53, 372, 202, 702, thickness=8,color=(87,87,87), batch=batch)
    inventory2Border= shapes.Box(53, 372, 202, 468, thickness=8,color=(87,87,87), batch=batch)
    inventory3Border= shapes.Box(53, 372, 202, 234, thickness=8,color=(87,87,87), batch=batch)

    dragonHealthBarBorder = pyglet.sprite.Sprite(img=dragonHealthBarImage, x=650, y=1125, batch=batch)
    dragonHealthBar= shapes.Rectangle(800, 1340, int(1065*dragonHBRatio), 40, color=(202,67,92), batch=batch)

    #Based on whether player health is damaged, different health will show:
    playerHealth1Sprite = pyglet.sprite.Sprite(img=playerHealthStatus1, x=20, y=15, batch=batch)
    playerHealth2Sprite = pyglet.sprite.Sprite(img=playerHealthStatus2, x=160, y=15, batch=batch)
    playerHealth3Sprite = pyglet.sprite.Sprite(img=playerHealthStatus3, x=300, y=15, batch=batch)

    #image will be chosen at random
    powerup1Sprite = pyglet.sprite.Sprite(img=shield, x=powerupP1[0], y=powerupP1[1], batch=powerUpStatus1)
    powerup2Sprite = pyglet.sprite.Sprite(img=potion, x=powerupP2[0], y=powerupP2[1], batch=powerUpStatus2)
    powerup3Sprite = pyglet.sprite.Sprite(img=doubleDamage, x=powerupP3[0], y=powerupP3[1], batch=powerUpStatus3)

redraw()  # Initial draw


# Create a label to display the array
array_label = pyglet.text.Label(
    str(noteArray),  # Convert array to string
    font_name='Arial',
    font_size=14,
    x=50, y=1400,
    color=(0, 0, 0, 255)  # White text (R, G, B, Alpha)
)


# Create labels
input_label = pyglet.text.Label(
    'Enter notes: ',
    font_size=50,
    x=300, y=200,
    color=(0, 0, 0, 255)
)

user_text_label = pyglet.text.Label(
    user_input,
    font_size=50,
    x=450, y=200,
    color=(0, 0, 0, 255)
)


# Event handlers
@window.event
def on_text(text):
    global user_input
    if game_state['started']:  # Only accept input during gameplay
        user_input += text
        user_text_label.text = user_input
        print(user_input)

@window.event  # ADD THIS DECORATOR!
def on_key_press(symbol, modifiers):
    global user_input, current_note_index
    
    if symbol == pyglet.window.key.RETURN:
        print("Entered")
        print(user_input)
        print(correct_notes[current_note_index])
        if current_note_index < len(correct_notes):
            # Check current note
            if user_input.strip().upper() == correct_notes[current_note_index].upper():
                print(f"✓ Note {current_note_index + 1} correct!")
                current_note_index += 1
                dra.redHealth(1)
                dragonHBRatio = dra.getHealth()/dra.getMaxHealth()  # Update health ratio
                redraw()

                # All notes correct?
                if current_note_index >= len(correct_notes):
                    print("🎉 Sequence complete! Dragon defeated!")
                    
                    # Trigger win condition
                    exit(0)
            else:
                print(f"✗ Wrong note! Expected {correct_notes[current_note_index]}")
                plr.redHealth()  # Damage player
                redraw()
                if plr.getHealth == 0:
                    print("You lose!")
                    exit(0)
        
        user_input = ""
        user_text_label.text = user_input
        
    elif symbol == pyglet.window.key.BACKSPACE:
        user_input = user_input[:-1]
        user_text_label.text = user_input


def isPointInsideSprite(x, y, sprite):
    print(f"Checking bounds - Click: ({x}, {y}), Sprite: ({sprite.x}, {sprite.y}) to ({sprite.x + sprite.width}, {sprite.y + sprite.height})")
    return (sprite.x <= x <= sprite.x + sprite.width and
            sprite.y <= y <= sprite.y + sprite.height)

animSprite = pyglet.sprite.Sprite(dragon_animation)
aniHurtingSprite = pyglet.sprite.Sprite(ani, x=1900, y=450)
animSprite.scale = 2.5            # increase this to make the dragon larger (try 2.0–3.0)
animSprite.x = 1250              # move horizontally (increase to move right)
animSprite.y = 400                # move vertically (increase to move up)


aniHurtingSprite.scale = 0.3       # increase this to make the dragon larger (try 2.0–3.0)
# aniHurtingSprite.x = 1250               # move horizontally (increase to move right)
# aniHurtingSprite.y = 400                # move vertically (increase to move up)

@window.event
def on_mouse_press(x, y, button, modifiers):  # FIXED: Changed from onMousePress
    print(f"Mouse clicked at: {x}, {y}")
    if button == mouse.LEFT:
        if isPointInsideSprite(x, y, startButtonSprite):
            startButtonAction()

end = False
@window.event
def on_draw():
    window.clear()
    pic = get_current_pic()  # Get the current background
    pic.blit(0,0,0)
    if not game_state['started']:
        startButtonSprite.draw()
    else:
        batch.draw()
        array_label.draw()
        input_label.draw()
        user_text_label.draw()

        animSprite.draw()
        aniHurtingSprite.draw()

pyglet.app.run()