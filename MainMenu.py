import pyglet
#import Game2Player
#import GameWithPyglet
#import GameWith2AI
from pyglet.gl import *
import importlib

windowWidth = 800
windowLength = 800

title = "Main Menu"

class GameObject:
    def __init__(self, posx, posy, sprite=None):
        self.posx = posx
        self.posy = posy
        if sprite is not None:
            self.sprite = sprite
            self.sprite.x=self.posx
            self.sprite.y=self.posy
            self.width = self.sprite.width
            self.height = self.sprite.height
    def draw(self):
        self.sprite.draw()
    def update(self):
        self.sprite.x = self.posx
        self.sprite.y = self.posy

def preload_image(image):
    img = pyglet.image.load('res/' + image)
    return img
MenuWindow = pyglet.window.Window()
MenuWindow.set_size(windowWidth,windowLength)
label = pyglet.text.Label("Main Menu",
                          font_name="Arial",
                          bold=True,
                          color=(255,0,0,255),
                          font_size=48,
                          x=windowWidth/2,y=windowLength/2,
                          anchor_x='center', anchor_y='center')

img = preload_image('Button.png')
button1 = GameObject(windowWidth/2-200,windowLength/2-90,pyglet.sprite.Sprite(img))
button1Label = pyglet.text.Label("1 v 1",
                                 font_name='Arial',
                                 bold=True,
                                 color=(0,0,0,255),
                                 font_size=24,
                                 x=windowWidth/2-200+53,
                                 y=windowLength/2-90+30,
                                 anchor_x='center', anchor_y='center')
button2 = GameObject(windowWidth/2-50,windowLength/2-90,pyglet.sprite.Sprite(img))
button2Label = pyglet.text.Label("1 v AI",
                                 font_name='Arial',
                                 bold=True,
                                 color=(0,0,0,255),
                                 font_size=24,
                                 x=windowWidth/2-50+53,
                                 y=windowLength/2-90+30,
                                 anchor_x='center', anchor_y='center')
button3 = GameObject(windowWidth/2+100,windowLength/2-90,pyglet.sprite.Sprite(img))
button3Label = pyglet.text.Label("AI v AI",
                                 font_name='Arial',
                                 bold=True,
                                 color=(0,0,0,255),
                                 font_size=24,
                                 x=windowWidth/2+100+53,
                                 y=windowLength/2-90+30,
                                 anchor_x='center', anchor_y='center')


@MenuWindow.event
def on_mouse_press(x, y, button, modifiers):
    game1 = False
    game2 = False
    game3 = False

    if (y >= 310) and (y <= 370):
        if (x >= 200) and (x <=305):
            #Launch 1v1
            import Game2Player
            #importlib.reload(Game2Player)
            #window = Game2Player.MainWindow()
        elif (x >= 350) and (x <= 455):
            #Launch 1vAI
            import GameWithPyglet
            #window2 = GameWithPyglet.MainWindow2()
        elif (x >= 500) and (x <= 605):
            #Launch AI v AI
            import GameWith2AI
            #window3 = GameWith2AI.MainWindow3()

@MenuWindow.event
def on_close():
    pyglet.app.exit()

@MenuWindow.event
def on_draw():
        MenuWindow.clear()
        label.draw()
        button1.draw()
        button1Label.draw()
        button2.draw()
        button2Label.draw()
        button3.draw()
        button3Label.draw()

pyglet.app.run()
