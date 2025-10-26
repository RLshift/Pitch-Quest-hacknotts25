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
background = pyglet.graphics.Group(order=0)
foreground = pyglet.graphics.Group(order=1)

flautist = image.load('flautist.png')
dragon = image.load('dragon.png')

#sprites = [pyglet.sprite.Sprite(flautist, batch=batch, group=foreground),pyglet.sprite.Sprite(dragon, batch=batch, group=foreground)]


flautistSprite = pyglet.sprite.Sprite(img=flautist, x=80, y=-25, batch=batch)
dragonSprite = pyglet.sprite.Sprite(img=dragon, x=1180, y=450, batch=batch)
#width, height = flautist.width, flautist.height


@window.event
def on_draw():
    window.clear()
    pic.blit(0, 0, 0)
    #flautist.blit(200,200,200)
    #sprite.draw()
    batch.draw()


pyglet.app.run()