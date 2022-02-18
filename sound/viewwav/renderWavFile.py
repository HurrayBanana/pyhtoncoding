'''
simple wav file visualiser
copyright Hurray Banana Feb 2022
Only looks at left channel to simplify data
So stated file sizes wont be same as stereo files as
only basing it on a single channel
'''
import wave
import pygame
import os

''' global system values '''
version = "1.10"
win = None
font = None
keys = None
delta = 0
deltaF = 0
gametime = 0
''' ui display system globals '''
scrWidth = 0
scrHeight = 0
scrMid = 0
scrThird = 0
scrTwoThird = 0
scrSixth = 0
waveAmp = 0
upperDisplay = 0
lowerDisplay = 0
modifiedDataPosition = 0
originalDataPosition = 0
''' constants '''
X = 0
Y = 1
R = 0
G = 1
B = 2
''' wave system globals '''
selectingFile = True
modeline = True
overlay = False
samplingOn = False
scale = 20
step = 1
waveFiles = []
fileChosen = 0
'''key delay handlers'''
ldelay = 0
heldtime = 0
speedscroll = 1
lwait = 0.25
speedKeys = [pygame.K_LEFT, pygame.K_RIGHT,pygame.K_UP, pygame.K_DOWN,pygame.K_a,pygame.K_q]
''' Current WAV file data '''
currSamples = 0
currFreq = 0
currChannels = 0
currSeconds = 0
currbytesPerSample = 0
normalsamples = []
#end of globals

def loadWavFile(file):
    '''load given wave and set render wav and render data
    file - the wav file to load    
    '''

    global currSamples, currFreq, currSeconds, currbytesPerSample, sampleStart
    wv = wave.open(file, 'rb')
    meta = wv.getparams()
    '''
    print(file)
    print("channels",meta.nchannels)
    print("samples",meta.nframes)
    print("sample size",meta.sampwidth*8)
    print("sample freq",meta.framerate, "Hz")'''
    currFreq = meta.framerate
    currSamples = meta.nframes# / meta.nchannels
    samples = wv.readframes(meta.nframes)
    currSeconds = currSamples / currFreq
    currbytesPerSample = meta.sampwidth

    #print("length in seconds: " + str(currSeconds))
    p = 0
    normalsamples.clear()
    while p < currSamples:
        c = 0
        while c < 16 and p < currSamples:
            samp = samples[p] if samples[p]< 128 else -((samples[p] ^ 255)+1)
            normalsamples.append(samp)
            p+=1
            c+=1

    pygame.display.set_caption(file + " " + str(currFreq) + "Hz samples:" + str(currSamples) + "  " + str(currbytesPerSample*8) + " bits per sample")
    sampleStart = 0
    genDynamicData()
#end def loadWavFile(file):

def drawWAV(w, col, s0, sc, dsam, tk, mode, centre, amp):
    '''
    draws the given audio sample
    using the given step distance
    w - wave file
    col - colour to render with
    s0 - starting sample
    sc - horizontal scale factor to use
    dsam - number of samples to skip
    tk - line thickness
    mode - line or chart
    centre - centre of render
    amp - maximum height of render
    '''    
    mute = 0.75
    axisC = (int(col[0]*mute),int(col[1]*mute),int(col[2]*mute))
    pygame.draw.line(win, axisC, [0,centre],[win.get_width(),centre])
    
    thispixW = pixW * dsam
    p = s0 - s0 % dsam
    x = (p-s0) * pixW
    sy = amp/128
    end =  currSamples - dsam

    while x < scrWidth and p < end:
        v1 = [x,sy*w[p] + centre]
        x += thispixW
        p += dsam
        v2 = [x,sy*w[p] + centre]
        if mode:
            pygame.draw.line(win, col, v1, v2, tk)  
        else:
            if v1[Y] > centre:
                pygame.draw.rect(win, col, (v1[X], centre, pixW*dsam, v1[Y]-centre))
            else:
                pygame.draw.rect(win, col, (v1[X], v1[Y], pixW*dsam, centre-v1[Y]))
#end def drawWAV(w, col, s0, sc, dsam, tk, mode, centre, amp):

def drawWAVSamples(w, col, s0, sc, dsam, tk, line, centre, amp):
    '''
    draws a vertical line from axis to peak
    w - wave file
    col - colour to render with
    s0 - starting sample
    sc - horizontal scale factor to use
    dsam - number of samples to skip
    tk - line thickness
    mode - line or circle/point
    centre - centre of render
    amp - maximum height of render
    '''    
    thispixW = pixW * dsam
    p = s0 - s0 % dsam
    x = (p-s0) * pixW
    sy = amp / 128
    end =  currSamples - dsam
    while x < scrWidth and p < end:
        v1 = [x,sy*w[p] + centre]
        v2 = [x,centre]
        if line:
            pygame.draw.line(win, col, v1, v2, tk)
        if samplingOn:
            pygame.draw.circle(win, col, v1, tk)
        x += thispixW
        p += dsam
#end def drawWAVSamples(w, col, s0, sc, dsam, tk, line,centre, amp):

def gameLoop():
    ''' performs the bolier plate code
    reading keys, tracking time deltas
    launching logic and drawing code
    watching out for quitting
    '''
    global keys, lastkeys, delta, gametime, deltaF
    running = True
    while running:
        delta = pygame.time.get_ticks() - gametime
        gametime += delta
        deltaF = delta * 0.001
        lastkeys = keys        
        keys = pygame.key.get_pressed()
        gameLogic()
        drawGame()
        if keys[pygame.K_ESCAPE]:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
#end def gameLoop()

def gameLogic():
    ''' perform any key checks and logic '''
    counters()
    gameKeys()
#end def gameLogic()   

def counters():
    '''manages all counters and delays'''
    global ldelay, heldtime, speedscroll, lwait 
    ldelay += deltaF

    if KeyListHeld(speedKeys):
        heldtime += deltaF
        if heldtime > 4.0:
            speedscroll = 10
            lwait = 1/60
        elif heldtime > 2:
            speedscroll = 5
            lwait = 1/12
            
    elif not(KeyListHeld(speedKeys)):
        heldtime = 0
        speedscroll = 1
        lwait = 0.15
#end def counters():        

def gameKeys():
    ''' react to any specific user key presses '''
    global sampleStart,scale,step, modeline, ldelay, samplingOn, overlay, fileChosen, selectingFile
    #file section keys
    if (selectingFile):
        if KeyPressed(pygame.K_UP) and fileChosen > 0:
            fileChosen -= 1
        if KeyPressed(pygame.K_DOWN) and fileChosen < len(waveFiles)-1:
            fileChosen += 1
        if KeyPressed(pygame.K_RETURN):
            selectingFile = False
            loadWavFile(waveFiles[fileChosen])
    #standard wave UI keys
    else:
        if KeyPressed(pygame.K_f):
            selectingFile = True
        dsampleStart = 0
        if KeyDown(pygame.K_LEFT) and ldelay > lwait:
            dsampleStart = -speedscroll
            ldelay = 0
        elif KeyDown(pygame.K_RIGHT) and ldelay > lwait:
            dsampleStart = speedscroll
            ldelay = 0

        sampleStart = clamp(sampleStart + dsampleStart, 0, currSamples - visibleSampCount) 

        dscale = 0
        if visibleSampCount < currSamples and KeyDown(pygame.K_UP) and ldelay > lwait:
            dscale = speedscroll
            ldelay = 0

        elif KeyDown(pygame.K_DOWN) and ldelay > lwait:
            dscale = -speedscroll
            ldelay = 0

        scale = clamp(scale + dscale, 10, maxScale)

        if step < currSamples/4 and KeyDown(pygame.K_q) and ldelay > lwait:
            step = step + speedscroll
            ldelay = 0
        elif KeyDown(pygame.K_a) and ldelay > lwait:
            step = max(1,step -speedscroll)
            ldelay = 0

        if KeyPressed(pygame.K_b):
            modeline = not modeline
        if KeyPressed(pygame.K_o):
            overlay = not overlay
        if step < 2:
            overlay = False
        if KeyPressed(pygame.K_s):
            samplingOn = not samplingOn
#end def gameKeys()

def KeyPressed(key):
    '''determines if key has just been pressed'''
    return keys[key] and not lastkeys[key]
def KeyDown(key):
    '''determines if a key is down'''
    return keys[key] 
def KeyHeld(key):
    '''determines if a key is down and was previously'''
    return keys[key] and lastkeys[key]

def KeyListHeld(keyList):
    ''' returns true if any key in the list is held false if none are held '''
    i = 0
    while i < len(keyList) and not KeyHeld(keyList[i]):
        i+=1
    return not i == len(keyList)
#end def KeyListHeld(keyList):

def clamp(value, min, max):
    '''ensures a value lies between min and max'''
    if value < min:
        return min
    elif value > max:
        return max
    return value    

def drawGame():
    ''' perform any rendering actions after all logic is processed '''
    #clear screen with black (r,g,b)
    win.fill((0,0,0))

    if (selectingFile):
        drawFileList(16)
    else:
        genDynamicData()
        iSS = int(sampleStart)
        
        #modified waveform
        if modeline:
            drawWAVSamples(normalsamples,(255,255,255),iSS,scale,step,1,True, upperDisplay, scrSixth)

        drawWAV(normalsamples,(255,255,0),iSS,scale,step,2, modeline, upperDisplay, scrSixth)
        textWithBox((255,255,0),(255,255,255),modifiedDataPosition, scrWidth, True,"Sample Frequency:" + str(round(fq,2)) + "Hz  " + str(currbytesPerSample*8) + " Bits per sample    File size: " + str(currbytesPerSample * int(currSamples/step)) + " bytes")
        
        #original waveform
        drawWAV(normalsamples,(255,0,0),iSS,scale,1,2, True, lowerDisplay, scrSixth)
        if overlay:
            drawWAV(normalsamples,(255,255,255),iSS,scale,step,2, True, lowerDisplay, scrSixth)

        drawWAVSamples(normalsamples,(255,255,255),iSS,scale,step,2,False, lowerDisplay, scrSixth)
        textWithBox( (255,0,0), (255,255,255), originalDataPosition, scrWidth, True, "Sample Frequency: " + str(currFreq) + "Hz   " + str(currbytesPerSample*8) + " Bits per sample    File size: " + str(currbytesPerSample * currSamples) + " bytes" )
        
        drawUI(iSS)
        renderPosition()

    #shows drawing on screen
    pygame.display.flip()
#end def drawGame()

def drawFileList(max):
    '''shows the wav files (limited to max) highlights the current selection '''
    pygame.draw.rect(win, (50,50,50), (40,50,scrWidth-80,scrHeight-100))
    ff = font.render("Use cursor to select file to load, [<--enter] to select", False, (255,255,255))
    win.blit(ff, (50,110))
    y = 140
    for i in range(len(waveFiles)):
        if i == fileChosen:
            ff = font.render(waveFiles[i], False, (255,255,255),(0,0,255))
        else:
            ff = font.render(waveFiles[i], False, (255,255,255))

        win.blit(ff, (60,y))
        y+= 35
#end def drawFileList(max):

def drawUI(samplestart):
    '''draws all UI text with highlghts'''
    xp = 10
    textWithBox((0,0,200),(255,255,255),(xp,10),110, modeline, "[b]locks")
    xp += 115
    textWithBox((0,200,0),(255,255,255),(xp,10),110,not overlay, "[o]verlay")
    xp += 115
    textWithBox((200,0, 0),(255,255,255),(xp,10),110,not samplingOn, "[s]amples")    
    xp += 115

    textWithBox((200,200, 0),(255,255,255),(xp,10),240,not(KeyDown(pygame.K_LEFT) or KeyDown(pygame.K_RIGHT)), "[<>] scroll " + str(samplestart))
    xp += 245
    textWithBox((0,200, 200),(255,255,255),(xp,10),210,not(KeyDown(pygame.K_UP) or KeyDown(pygame.K_DOWN)), "[v^] scale " + str(round(scale/100,2)))
    xp += 215
    textWithBox((200,0, 200),(255,255,255),(xp,10),180,not(KeyDown(pygame.K_a) or KeyDown(pygame.K_q)), "[qa] step " + str(step))
#end def drawUI(samplestart):

def textWithBox(backColour, textColour, pos, width, dim, txt):
    '''displays text with colour options and width options
    backColour background colour to use
    textColour colour for the text
    pos - tuple x and y position
    width - width to draw box to contain text, text centered. If zero then width of text used
    dim - Boolean if True then back colour is faded to 40%
    txt - the text to display
    '''
    dx = 0
    fx = 0.4
    if dim:
        backColour = (int(backColour[R]*fx),int(backColour[G]*fx),int(backColour[B]*fx))
    if width == 0:
        ff = font.render(txt, False, textColour, backColour)
    else:
        ff = font.render(txt, False, textColour)
        dx = (width - ff.get_width()) / 2
        pygame.draw.rect(win, backColour, (pos[X],pos[Y], width, ff.get_height() + 10))

    win.blit(ff, (pos[X] + dx,pos[Y] + 5))
#end def textWithBox(backColour, textColour, pos, width, dim, txt):

def genDynamicData():
    '''generates data values based on current wav, render and UI settings'''
    global visibleSampCount, pixW, maxScale, fq
    pixW = 100/scale
    visibleSampCount = clamp(scrWidth / pixW, 1,currSamples) 
    maxScale = currSamples / scrWidth *100
    fq = currFreq / step
#end def genDynamicData():

def renderPosition():
    ''' draws the sample size bar and position'''
    d = max(10,scrWidth * visibleSampCount/currSamples)
    f = 1000 * sampleStart/currSamples
    pygame.draw.rect(win, (50,50,50), (0,scrHeight-30, scrWidth, 20))
    pygame.draw.rect(win, (205,0,0), (f,scrHeight-35, d, 5))
    pygame.draw.rect(win, (100,0,0), (f,scrHeight-30, d, 20))
    pygame.draw.rect(win, (205,0,0), (f,scrHeight-10, d, 5))
#end def renderPosition():

def getwavFiles():
    ''' gets the wav files in the current cirectory'''
    waveFiles.clear()
    directory = os.getcwd()
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.name.find(".wav") != -1:
                waveFiles.append(entry.name)
#end def getwavFiles():
               
def screenMetrics():
    '''pre calculates some screen metrics'''
    global scrHeight,scrWidth,scrMid,scrThird,scrTwoThird,scrSixth,waveAmp, font
    global upperDisplay,lowerDisplay,modifiedDataPosition,originalDataPosition
    
    scrHeight = win.get_height()
    scrWidth = win.get_width()
    scrMid = scrHeight/2
    scrThird = scrHeight/3
    scrTwoThird = 2 * scrThird
    scrSixth = scrThird / 2
    waveAmp = scrSixth - 10
    upperDisplay = scrThird - 20
    lowerDisplay = scrTwoThird + 20
    modifiedDataPosition = (0, int(scrThird - waveAmp - 80))
    originalDataPosition = (0, int(scrTwoThird + waveAmp + 60))
#end def screenMetrics():

def main():
    '''initialise pygame library, set window and font, start gameloop'''
    global win, font, gametime
    pygame.init()
    win = pygame.display.set_mode((1000, 800))
    font = pygame.font.SysFont("monospace",20)
    screenMetrics()
    getwavFiles()
    gametime = pygame.time.get_ticks()
    gameLoop()

#=== start point of code ===#
'''first piece of code executed'''
'''run main() function, quit pygame when main ends'''
main()

pygame.quit()
