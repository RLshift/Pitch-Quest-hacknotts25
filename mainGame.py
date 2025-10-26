import pyglet

# importing shapes from pyglet library
from pyglet import shapes

# Canvas
window = pyglet.window.Window(2560, 1440)
batch = pyglet.graphics.Batch()

from pyglet import image
pic = image.load('images/backgroundGamePlay.png')
width, height = pic.width, pic.height

batch = pyglet.graphics.Batch()
dead = pyglet.graphics.Batch()

powerupP1 = [33,850]
powerupP2 = [33,610]
powerupP3 = [33,370]

#1 = Full, 2 = Half, 3 = Dead, Complete player Health = 6

playerHealthStatus1 = [1]
playerHealthStatus2 = [2]
playerHealthStatus3 = [3]

dragonMaxHealth = 60
dragonHealth = 15
dragonHBRatio = dragonHealth/dragonMaxHealth

background = pyglet.graphics.Group(order=0)
foreground = pyglet.graphics.Group(order=1)

flautist = image.load('images/flautist.png')
dragon = image.load('images/dragon.png')
playerHealthFull = image.load('images/playerHealthFull.png')
playerHealthHalf = image.load('images/playerHealthHalf.png')
playerHealthDead = image.load('images/playerHealthDead.png')
shield = image.load('images/shield.png')
potion = image.load('images/potion.png')
doubleDamage = image.load('images/doubleDamage.png')
dragonHealthBarImage = image.load('images/dragonHealthBarBorder.png')


flautistSprite = pyglet.sprite.Sprite(img=flautist, x=380, y=-25, batch=batch)
dragonSprite = pyglet.sprite.Sprite(img=dragon, x=1180, y=450, batch=batch)
playerHealthBackground= shapes.Rectangle(35, 50, 500, 130, color=(164,164,164,180), batch=batch)
playerHealthBorder= shapes.Box(33, 48, 502, 132, thickness=5,color=(87,87,87), batch=batch)

inventoryBackground= shapes.Rectangle(55, 370, 200, 700, color=(164,164,164,220), batch=batch)
inventoryBorder= shapes.Box(53, 372, 202, 702, thickness=8,color=(87,87,87), batch=batch)
inventory1Border= shapes.Box(53, 372, 202, 702, thickness=8,color=(87,87,87), batch=batch)
inventory2Border= shapes.Box(53, 372, 202, 468, thickness=8,color=(87,87,87), batch=batch)
inventory3Border= shapes.Box(53, 372, 202, 234, thickness=8,color=(87,87,87), batch=batch)

dragonHealthBarBorder = pyglet.sprite.Sprite(img=dragonHealthBarImage, x=650, y=1125, batch=batch)
dragonHealthBar= shapes.Rectangle(800, 1340, 1065*dragonHBRatio, 40, color=(202,67,92), batch=batch)

#Based on whether player health is damaged, different health will show:
playerHealth1Sprite = pyglet.sprite.Sprite(img=playerHealthFull, x=20, y=15, batch=batch)
playerHealth2Sprite = pyglet.sprite.Sprite(img=playerHealthHalf, x=160, y=15, batch=batch)
playerHealth3Sprite = pyglet.sprite.Sprite(img=playerHealthDead, x=300, y=15, batch=batch)

#image will be chosen at random
powerup1Sprite = pyglet.sprite.Sprite(img=shield, x=powerupP1[0], y=powerupP1[1], batch=batch)
powerup2Sprite = pyglet.sprite.Sprite(img=potion, x=powerupP2[0], y=powerupP2[1], batch=batch)
powerup3Sprite = pyglet.sprite.Sprite(img=doubleDamage, x=powerupP3[0], y=powerupP3[1], batch=batch)

#width, height = flautist.width, flautist.height


@window.event
def on_draw():
    window.clear()
    pic.blit(0, 0, 0)
    #sprite.draw()
    batch.draw()


pyglet.app.run()