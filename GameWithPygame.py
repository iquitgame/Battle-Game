import pygame
pygame.init()

x = 100
y = 100
radius = 50
vel = 10
screenWidth = 1000
screenHeight = 800

win = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Battle Game")

game = True

while game:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x-radius > 0:
        x-=vel
    if keys[pygame.K_RIGHT] and x+radius < screenWidth:
        x+=vel
    if keys[pygame.K_UP] and y-radius > 0:
        y-=vel
    if keys[pygame.K_DOWN] and y+radius < screenHeight:
        y+=vel

    win.fill((0,0,0))
    pygame.draw.circle(win, (255,0,0), (x, y), radius, 50)
    pygame.display.update()

pygame.quit()
