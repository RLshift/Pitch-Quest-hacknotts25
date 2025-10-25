import pyglet

# importing shapes from pyglet library
from pyglet import shapes

# Canvas
window = pyglet.window.Window(2560, 1440)
batch = pyglet.graphics.Batch()

from pyglet import image
pic = image.load('backgroundGamePlay.png')
width, height = pic.width, pic.height

flautist = image.load('flautist.png')
sprite = pyglet.sprite.Sprite(img=flautist, x=160, y=-25)
#width, height = flautist.width, flautist.height
# Making Green Circle
circle = shapes.Circle(700, 150, 100, 
                       color=(50, 225, 30),
                       batch=batch)


@window.event
def on_draw():
    window.clear()
    pic.blit(0, 0, 0)
    #flautist.blit(200,200,200)
    sprite.draw()
    #batch.draw()


pyglet.app.run()