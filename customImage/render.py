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
width=2
height=2
colourdepth=2
sx=50 #size of each pixel
sy=50
xpos=100 #top left corner of image
ypos=100
pixels=[0,1,1,0]

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
    global xpos
    if keys[pygame.K_LEFT]:
        xpos -= 1
    elif keys[pygame.K_RIGHT]:
        xpos += 1
#end def gameKeys()

def drawImage():
    pix = 0
    y = ypos
    for row in range(height):
        x = xpos
        for col in range(width):
            pen = pixels[pix]
            pygame.draw.rect(win, pal[pen],(x,y,sx,sy))
            x += sx # move x to next pixel location
            pix += 1 # move to next pixel data
        y += sy


def drawTest():
    pen = pixels[0]
    pygame.draw.rect(win, pal[pen], (xpos, ypos, sx, sy))
    pen = pixels[1]
    pygame.draw.rect(win, pal[pen], (xpos +sx, 100, sx, sy))
    pen = pixels[2]
    pygame.draw.rect(win, pal[pen], (xpos, ypos+sy, sx, sy))
    pen = pixels[3]
    pygame.draw.rect(win, pal[pen], (xpos+sx, ypos+sy, sx, sy))

'''
perform any rendering actions after all logic is processed
'''
def drawGame():
    #clear screen with black (r,g,b)
    win.fill((0,0,0))

    drawImage()
    #drawTest()
    #draw a test rectangle at x=50,y=40,width=30,height=20
    #pygame.draw.rect(win, (0,255,0), (50, 40, 30, 20))

    #draw some text in white (r255,g255,b255) at x=10,y=10
    #win.blit(font.render("version " +str(version), False, (255,255,255)), (10,10))

    #shows drawing on screen
    pygame.display.flip()
#end def drawGame()

#=== start point of code ===#
# initialise pygame library, set window and font
# start gameloop, quit when it exits
pygame.init()
win = pygame.display.set_mode((400, 400))
font = pygame.font.SysFont("monospace",20)
gameLoop()
pygame.quit()
