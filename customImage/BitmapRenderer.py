import pygame
import random
from bitmap import myimage

xpos = 0
ypos = 0

''' main system loop last until pygame is closed'''
def gameLoop():
    global keys
    running = True
    while running:
        keys = pygame.key.get_pressed()
        gameLogic()
        drawGame()
        if keys[pygame.K_ESCAPE]:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
#end def gameLoop()

'''
perform any key checks and logic
'''
def gameLogic():
    gameKeys()
#end def gameLogic()   
'''
react to any specific user key presses
'''
def gameKeys():
    global xpos, ypos
    if keys[pygame.K_LEFT]:
        xpos -= 0.5
    elif keys[pygame.K_RIGHT]:
        xpos += 0.5
    if keys[pygame.K_UP]:
        ypos -= 0.5
    elif keys[pygame.K_DOWN]:
        ypos += 0.5
#end def gameKeys()

'''
perform any rendering actions after all logic is processed
'''
def drawGame():
    #clear screen with black (r,g,b)
    win.fill((0,0,0))

    inky.draw()
    clyde.draw()
    pinky.draw()
    blinky.drawHere(xpos, ypos)

    #draw some text in white (r255,g255,b255) at x=10,y=10
    win.blit(font.render("use cursors to move Blinky", False, (255,255,255)), (10,10))

    #shows drawing on screen
    pygame.display.flip()
#end def drawGame()

#=== start point of code ===#
# initialise pygame library, set window and font
# start gameloop, quit when it exits
pygame.init()
win = pygame.display.set_mode((800, 800))
font = pygame.font.SysFont("monospace",20)
#load the same ghost 4 times, changing the final colour in the palette
blinky = myimage(pygame,win,"myghost.junk")
inky = myimage(pygame,win,"myghost.junk")
inky.pal[3] = (143,237,242)
inky.setPosition(100,100)
pinky = myimage(pygame,win,"myghost.junk")
pinky.pal[3] = (242,143,219)
pinky.setPosition(500,100)
clyde = myimage(pygame,win,"myghost.junk")
clyde.pal[3] = (237,189,100)
clyde.setPosition(300,100)
gameLoop()
pygame.quit()
