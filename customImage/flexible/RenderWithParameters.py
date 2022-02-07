import pygame
import random

#global system values
win = None
font = None
keys = None
version = 1.0

#imagedata
#colour pallete
pal=[(255,0,0),(150,150,255)]
pal2=[(255,255,0),(0,0,255)]
width=8
height=8
colourdepth=2
sx=10 #size of each pixel
sy=10
xpos=100 #top left corner of image
ypos=100
pixels=[0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0]

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
        xpos -= 1
    elif keys[pygame.K_RIGHT]:
        xpos += 1
    if keys[pygame.K_UP]:
        ypos -= 1
    elif keys[pygame.K_DOWN]:
        ypos += 1
#end def gameKeys()

def drawImage(startx, starty, thispal, scx, scy):
    pix = 0
    y = starty #ypos
    for row in range(height):
        x = startx #xpos
        for col in range(width):
            pen = pixels[pix]
            pygame.draw.rect(win, thispal[pen],(x,y,scx,scy))
            x += scx # move x to next pixel location
            pix += 1 # move to next pixel data
        y += scy


'''
perform any rendering actions after all logic is processed
'''
def drawGame():
    #clear screen with black (r,g,b)
    win.fill((0,0,0))

    drawImage(10,10,pal, 10,10)
    drawImage(300,300,pal2,30,20)

    #shows drawing on screen
    pygame.display.flip()
#end def drawGame()

#=== start point of code ===#
# initialise pygame library, set window and font
# start gameloop, quit when it exits
pygame.init()
win = pygame.display.set_mode((800, 800))
font = pygame.font.SysFont("monospace",20)
gameLoop()
pygame.quit()
