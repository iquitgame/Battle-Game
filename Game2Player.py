import pyglet
from pyglet.window import key, FPSDisplay
from math import *
from pyglet.gl import *
from pyglet.sprite import Sprite
from random import uniform, randint
import numpy as np

INPUT_NUM = 22

windowHeight = 800
windowWidth = 800
gameName = "Battle Game"

playerLength = 50
playerWidth = 50
movementSpeed = 300

counter_games = 0

def preload_image(image):
    img = pyglet.image.load('res/' + image)
    return img

class GameObject:
    def __init__(self, posx, posy, sprite=None):
        self.posx = posx
        self.posy = posy
        self.velx = 0
        self.vely = 0
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

class Player:
    def __init__(self, posx,posy, color):
        self.health = 100
        self.posx = posx #left side of square
        self.posy = posy #bottom side of square
        self.velx = 0
        self.vely = 0
        self.width = playerWidth
        self.height = playerLength
        self.color = color + color + color + color
        self.fire = False
        self.fire_rate = 0;
        self.kill = False
        self.death = False

    def draw(self):
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0,1,2, 0,2,3],
                             ('v2i', (self.posx, self.posy,
                                      self.posx + playerWidth, self.posy,
                                      self.posx + playerWidth, self.posy + playerLength,
                                      self.posx, self.posy + playerLength)),
                             ('c3B', self.color))


    def update(self,dt):

        self.posx +=int(self.velx*dt)
        self.posy +=int(self.vely*dt)
        if self.posx <= 0:
            self.posx = 0
        if self.posx >= windowWidth - playerWidth:
            self.posx = windowWidth - playerWidth
        if self.posy <= 0:
            self.posy = 0
        if self.posy >= windowHeight-playerLength:
            self.posy = windowHeight-playerLength



class MainWindow(pyglet.window.Window):

    def __init__(self):

        super().__init__(windowWidth, windowHeight, gameName)
        # The game loop
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        self.fps_display = FPSDisplay(self)
        self.player1 = Player(375,50,(255,0,0))

        self.player_laser = preload_image('laser.png')
        self.player1_laser_list = []

        self.player2 = Player(375,700, (0,0,255))
        self.player2_laser_list = []

    def on_key_press(self, symbol, modifiers): # idk what agent does here
        if symbol == key.RIGHT:
            self.player1.velx += movementSpeed
        if symbol == key.LEFT:
            self.player1.velx += -movementSpeed
        if symbol == key.UP:
            self.player1.vely += movementSpeed
        if symbol == key.DOWN:
            self.player1.vely += -movementSpeed
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        if symbol == key.SPACE:
            self.player1.fire = True

        if symbol == key.D:
            self.player2.velx += movementSpeed
        if symbol == key.A:
            self.player2.velx += -movementSpeed
        if symbol == key.W:
            self.player2.vely += movementSpeed
        if symbol == key.S:
            self.player2.vely += -movementSpeed
        if symbol == key._1:
            self.player2.fire = True


    def on_key_release(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.player1.velx -= movementSpeed
        if symbol == key.LEFT:
            self.player1.velx += movementSpeed
        if symbol == key.UP:
            self.player1.vely -= movementSpeed
        if symbol == key.DOWN:
            self.player1.vely += movementSpeed
        if symbol == key.SPACE:
            self.player1.fire = False

        if symbol == key.D:
            self.player2.velx -= movementSpeed
        if symbol == key.A:
            self.player2.velx += movementSpeed
        if symbol == key.W:
            self.player2.vely -= movementSpeed
        if symbol == key.S:
            self.player2.vely += movementSpeed
        if symbol == key._1:
            self.player2.fire = False

    def on_draw(self):
        self.clear()
        self.fps_display.draw()

        self.player1.draw()
        self.player2.draw()

        for laser in self.player1_laser_list:
            laser.draw()

        for laser in self.player2_laser_list:
            laser.draw()

    def update_player_laser(self, dt):
        for i in range(len(self.player1_laser_list)):
            self.player1_laser_list[i].update()
            if i % 4 == 0:
                self.player1_laser_list[i].posy += 400 * dt
            if i % 4 == 1:
                self.player1_laser_list[i].posy -= 400 * dt
            if i % 4 == 2:
                self.player1_laser_list[i].posx += 400 * dt
            if i % 4 == 3:
                self.player1_laser_list[i].posx -= 400 * dt

        for i in range(round(len(self.player1_laser_list)/4.0)):
            if self.player1_laser_list[i].posy > 800 and self.player1_laser_list[i+1].posy < 0 and self.player1_laser_list[i+2].posx > 800 and self.player1_laser_list[i+3].posx < 0:
                self.player1_laser_list.remove(self.player1_laser_list[i + 3])
                self.player1_laser_list.remove(self.player1_laser_list[i + 2])
                self.player1_laser_list.remove(self.player1_laser_list[i + 1])
                self.player1_laser_list.remove(self.player1_laser_list[i])

        for i in range(len(self.player2_laser_list)):
            self.player2_laser_list[i].update()
            if i % 4 == 0:
                self.player2_laser_list[i].posy += 400 * dt
            if i % 4 == 1:
                self.player2_laser_list[i].posy -= 400 * dt
            if i % 4 == 2:
                self.player2_laser_list[i].posx += 400 * dt
            if i % 4 == 3:
                self.player2_laser_list[i].posx -= 400 * dt

        for i in range(round(len(self.player2_laser_list)/4.0)):
            if self.player2_laser_list[i].posy > 800 and self.player2_laser_list[i+1].posy < 0 and self.player2_laser_list[i+2].posx > 800 and self.player2_laser_list[i+3].posx < 0:
                self.player2_laser_list.remove(self.player2_laser_list[i + 3])
                self.player2_laser_list.remove(self.player2_laser_list[i + 2])
                self.player2_laser_list.remove(self.player2_laser_list[i + 1])
                self.player2_laser_list.remove(self.player2_laser_list[i])

    def player1_fire(self,dt):
        self.player1.fire_rate -= dt
        if self.player1.fire_rate <= 0:
            self.player1_laser_list.append(
                GameObject(self.player1.posx + playerWidth / 4, self.player1.posy + playerLength,
                           Sprite(self.player_laser)))
            self.player1_laser_list.append(
                GameObject(self.player1.posx + playerWidth / 4, self.player1.posy - playerLength / 1.7,
                           Sprite(self.player_laser)))
            self.player1_laser_list.append(
                GameObject(self.player1.posx + playerWidth, self.player1.posy + playerLength / 4,
                           Sprite(self.player_laser)))
            self.player1_laser_list.append(
                GameObject(self.player1.posx - playerWidth / 1.8, self.player1.posy + playerLength / 4,
                           Sprite(self.player_laser)))
            self.player1.fire_rate = 0.5

    def player2_fire(self,dt):
        self.player2.fire_rate -= dt
        if self.player2.fire_rate <= 0:
            self.player2_laser_list.append(
                GameObject(self.player2.posx + playerWidth / 4, self.player2.posy + playerLength,
                           Sprite(self.player_laser)))
            self.player2_laser_list.append(
                GameObject(self.player2.posx + playerWidth / 4, self.player2.posy - playerLength / 1.7,
                           Sprite(self.player_laser)))
            self.player2_laser_list.append(
                GameObject(self.player2.posx + playerWidth, self.player2.posy + playerLength / 4,
                           Sprite(self.player_laser)))
            self.player2_laser_list.append(
                GameObject(self.player2.posx - playerWidth / 1.8, self.player2.posy + playerLength / 4,
                           Sprite(self.player_laser)))
            self.player2.fire_rate = 0.5

    def bullet_collision(self, entity, bullet_list):
        for lsr in bullet_list:
            if lsr.posx < entity.posx + entity.width and lsr.posx + lsr.width > entity.posx \
                    and lsr.posy < entity.posy + entity.height and lsr.height + lsr.posy > entity.posy:
                return True

    def update(self, dt):

        self.player1.update(dt)
        if self.player1.fire:
            self.player1_fire(dt)

        self.player2.update(dt)
        if self.player2.fire:
            self.player2_fire(dt)
        self.update_player_laser(dt)

        if self.bullet_collision(self.player1, self.player2_laser_list):
            print("Player 2 Wins!")
            self.player2.kill = True
            self.player1.death = True
            #pyglet.app.exit()
            pyglet.window.Window.close(self)

        if self.bullet_collision(self.player2, self.player1_laser_list):
            print("Player 1 Wins!")
            self.player1.kill = True # Shouldn't be required for training
            self.player2.death = True
            #pyglet.app.exit()
            pyglet.window.Window.close(self)

window = MainWindow()
pyglet.app.run()