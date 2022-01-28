import pygame
import random

#global system values
win = None
font = None
keys = None
version = 1.0

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
    pass # used to mark a function as empty (supresses errors)
#    if keys[pygame.K_LEFT]:
#        respone to left being pressed
#end def gameKeys()
'''
perform any rendering actions after all logic is processed
'''
def drawGame():
    #clear screen with black (r,g,b)
    win.fill((0,0,0))

    #draw a test rectangle at x=50,y=40,width=30,height=20
    pygame.draw.rect(win, (0,255,0), (50, 40, 30, 20))

    #draw some text in white (r255,g255,b255) at x=10,y=10
    win.blit(font.render("version " +str(version), False, (255,255,255)), (10,10))

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
