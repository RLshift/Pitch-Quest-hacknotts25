import pyglet

# importing shapes from pyglet library
from pyglet import shapes

# Canvas
window = pyglet.window.Window(2560, 1440)
batch = pyglet.graphics.Batch()

from pyglet import image
pic = image.load('backgroundGamePlay.png')
width, height = pic.width, pic.height

batch = pyglet.graphics.Batch()
dead = pyglet.graphics.Batch()

background = pyglet.graphics.Group(order=0)
foreground = pyglet.graphics.Group(order=1)

flautist = image.load('flautist.png')
dragon = image.load('dragon.png')
playerHealth = image.load('playerHealth.png')
playerHealthDead = image.load('playerHealthDead.png')


flautistSprite = pyglet.sprite.Sprite(img=flautist, x=140, y=-25, batch=batch)
dragonSprite = pyglet.sprite.Sprite(img=dragon, x=1180, y=450, batch=batch)
playerHealthBackground= shapes.Rectangle(35, 50, 500, 130, color=(169,169,169,180), batch=batch)
playerHealthBorder= shapes.Box(33, 48, 502, 132, thickness=5,color=(87,87,87), batch=batch)

#Based on whether player health is damaged, different health will show:
playerHealth1Sprite = pyglet.sprite.Sprite(img=playerHealth, x=20, y=15, batch=batch)
playerHealth2Sprite = pyglet.sprite.Sprite(img=playerHealth, x=160, y=15, batch=batch)
playerHealth3Sprite = pyglet.sprite.Sprite(img=playerHealth, x=300, y=15, batch=batch)
playerHealthDead1Sprite = pyglet.sprite.Sprite(img=playerHealthDead, x=20, y=15, batch=dead)
playerHealthDead2Sprite = pyglet.sprite.Sprite(img=playerHealthDead, x=160, y=15, batch=dead)
playerHealthDead3Sprite = pyglet.sprite.Sprite(img=playerHealthDead, x=300, y=15, batch=dead)

#width, height = flautist.width, flautist.height


@window.event
def on_draw():
    window.clear()
    pic.blit(0, 0, 0)
    #sprite.draw()
    batch.draw()


pyglet.app.run()