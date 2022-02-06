'''
creates a new custome bitmap image object
'''
class myimage:
    def __init__(me, pygameRef, surface, imagefile):
        me.pygame = pygameRef
        me.surf = surface
        me.pal = []
        me.pixels = []
        me.readImage(imagefile)
        me.pen0Opaque = False
        me.setPosition(0,0)

    ''' treats pen0 (first colour in palette) as transparent '''    
    def Pen0Transparent(me):
        me.pen0Opaque = False

    ''' treats pen0 (first colour in palette) as opaque so is drawn) '''    
    def Pen0Opaque(me):
        me.pen0Opaque = True

    ''' sets the colour depth ** is raise to the power'''
    def setBPP(me, bits):
        me.colourdepth = 2**bits

    ''' stores a list of pixel data, allowing you to change the pixel data dynamically'''
    def setPixels(me, pixels):
        me.pixels = pixels

    ''' sets the width and height of the bitmap, if this is larger than pixel data then the code will crash'''
    def setDim(me, width, height):
        me.width = width; me.height = height

    ''' sets the size of each pixel'''
    def setSize(me, pixelWidth, pixelHeight):
        me.sx = pixelWidth; me.sy = pixelHeight    

    ''' sets the position of image (used in conjuction with draw()'''
    def setPosition(me, x, y):
        me.xpos = x
        me.ypos = y

    '''
    draw image at the position specified by me.xpos, me.ypos
    '''
    def draw(me):
        pix = 0
        y = int(me.ypos) #ypos
        for row in range(me.height):
            x = int(me.xpos) #xpos
            for col in range(me.width):
                pen = me.pixels[pix]
                #only draw pen 0 if Opaque
                if pen != 0 or me.pen0Opaque:
                    me.pygame.draw.rect(me.surf, me.pal[pen],(x,y,me.sx,me.sy))
                x += me.sx # move x to next pixel location
                pix += 1 # move to next pixel data
            y += me.sy

    '''
    draw image at the given location xp, yp
    '''
    def drawHere(me, xp, yp):
        pix = 0
        y = int(yp) #ypos
        for row in range(me.height):
            x = int(xp) #xpos
            for col in range(me.width):
                pen = me.pixels[pix]
                #only draw pen 0 if Opaque
                if pen != 0 or me.pen0Opaque:
                    me.pygame.draw.rect(me.surf, me.pal[pen],(x,y,me.sx,me.sy))
                x += me.sx # move x to next pixel location
                pix += 1 # move to next pixel data
            y += me.sy
    
    ''' converts string based colour into a proper tuple'''    
    def readPalette(me, colourstring):
        colours = colourstring.replace("(","").replace(")","").split(",")
        colourTuple = (int(colours[0]),int(colours[1]),int(colours[2]))
        return colourTuple
    
    ''' reads a row of comma separated pixels and stores in the pixels list'''
    def readPix(me, data):
        pix = data.split(",")
        for p in pix:
            me.pixels.append(int(p))

    ''' attempts to load a custome bitmap file and setup the parameters'''
    def readImage(me, imagefile):
        f = open(imagefile,"r")
        line = f.readline()
        while line:
            if line[0] != ";":
                data = line.split(":")
                if data[0] == "bpp":
                    me.setBPP(int(data[1]))
                elif data[0] == "pal":
                    me.pal.append(me.readPalette(data[1]))
                elif data[0] == "pix":
                    me.readPix(data[1])
                elif data[0] == "dim":
                    me.setDim(int(data[1]), int(data[2]))
                elif data[0] == "siz":
                    me.setSize(int(data[1]), int(data[2]))
            line=f.readline()
        f.close()

