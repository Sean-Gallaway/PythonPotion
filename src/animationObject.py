from animationGlobals import *



buttonList = []
actionList = []

#triggerable object
class triggerable ():
    keyActions = None
    def __init__ (self):
        self.keyActions = {}

    # check if the pressed keys match any of the keyAction trigger keys.
    def ifAction(self, keys):
        print("aaa", self)
        for key in self.keyActions.keys():
            if keys[key]:
                if callable(self.keyActions[key][0]):
                    self.keyActions[key][0](self.keyActions[key][1])
    
    # sets an action to activate when a key is pressed.
    def keyAction (self, key: int, func, *args: str):
        if self not in actionList:
            actionList.append(self)
        self.keyActions[key] = [func, args]




# base class for anything being drawn to the screen.
class drawObject (triggerable):
    x = 0
    y = 0
    width = 0
    height = 0
    obj = None
    animations = {}
    currentAnimation = None
    background = (100, 100, 100, 255)

    # constructor
    def __init__ (self, size: tuple, path = ""):
        self.width = size[0]
        self.height = size[1]

        if path != "":
            self.obj = pygame.image.load(path)
            self.obj = pygame.transform.scale(self.obj, size)
        else:
            self.obj = pygame.surface.Surface(size, pygame.SRCALPHA, 32 )
            self.obj.fill(self.background)
        self.animations = {}
        super().__init__()

    # draws this object to a given surface. 
    def draw (self, window: pygame.surface.Surface):
        if self.currentAnimation != None:
            self.currentAnimation.advance(dt)
        window.blit(self.obj, (self.x, self.y))

    # sets the position of this object using screen space coordinates.
    def setXY (self, dx, dy, center = False):
        if center:            
            self.x = dx - self.width/2
            self.y = dy - self.height/2
        else:
            self.x = dx
            self.y = dy
    
    # set the background color as a tuple
    def setBackgroundColor (self, r, g, b, a):
        self.background = (r, g, b, a)
        self.obj.fill(self.background)

    # add to the animation dictionary of this object
    def addAnim(self, name: str, a: 'animation'):   
        self.animations[name] = a

    # play an animation from the dictionary
    def playAnim(self, name):
        self.currentAnimation = self.animations[name[0]]
        self.currentAnimation.start(self)
        print(self, "\t", self.animations)





# says how to animate a drawObject
class animation ():
    endPos = None
    interpol = None
    duration = None
    time = 0
    subject = None
    playing = False
    startPos = None

    def __init__ (self, dxdy: tuple, duration: float, interpol = None, xy = None, ):
        self.endPos = dxdy
        self.duration = duration
        self.interpol = interpol
        self.startPos = xy

    # start an animation, the start position should be the objects current position to make things make sense.
    def start (self, obj: drawObject):
        self.time = 0
        self.subject = obj
        self.playing = True
        self.startPos = (obj.x, obj.y)

    # advances the animation based on a timeStep, usually delta time.
    # in other programs it might not make total sense why we use delta time over other options,
    # but here it is because the animation happens in a fixed timeframe, regardless of the easing function
    def advance (self, timeStep: float):
        if self.playing == False:
            return
        try:
            # use the interpolation function given when this object is created to go from
            # point A to point B with a given time interval.
            if self.duration < self.time:
                self.playing = False

            self.time += timeStep
            x = self.interpol(self.startPos[0], self.endPos[0], min(1, self.time/self.duration) )
            y = self.interpol(self.startPos[1], self.endPos[1], min(1, self.time/self.duration) )
            self.subject.setXY(x, y)

        except Exception as e:
            print(e)
            print("smoothing function failed.")




# classic label.
class label (drawObject):
    text = None
    textSize = None

    # constructor
    def __init__ (self, msg: str, size: tuple = None, fontSize: float = -1, fontColor = (0, 0, 0, 255)):
        if fontSize == -1 and size is None:
            print("Error with label, size or fontSize must be defined.")
            return

        # if we do not define a font size, we should probably make it a ratio of the size of the container.
        if fontSize == -1:
            fontSize = size[0] * .5
        font = pygame.font.SysFont('Corbel', int(fontSize)) 

        self.text = font.render(msg, True, fontColor)
        self.textSize = font.size(msg)
        if size is None:
            size = self.textSize

        super().__init__(size)
        self.obj.fill(self.background)


    # draws this object and its text to a given surface.
    def draw (self, window: pygame.surface.Surface):
        if self.currentAnimation != None:
            self.currentAnimation.advance(dt)
        window.blit(self.obj, (self.x, self.y))
        window.blit(self.text, (self.x+(self.width/2-self.textSize[0]/2), self.y+(self.height/2-self.textSize[1]/2)))




# classic button, does a thing if you bind a function to it.
class btn (label):
    func = None
    funcArgs = None

    # constructor
    def __init__ (self, msg: str, size: tuple):
        super().__init__(msg, size)
        buttonList.append(self)

    # check if the cursor is in the bounds of this button using screen space
    def cursorInBounds (self, mouse: list):
        if not (self.x < mouse[0] and mouse[0] < self.x + self.width):
            return
        if not (self.y < mouse[1] and mouse[1] < self.y + self.height):
            return
        
        # try to run the bound function
        try:
            self.func(self.funcArgs)
        except Exception as e:
            print(e)
            print("function failed")

    # binds a function to this button to be ran when this button is clicked.
    def bindFunction (self, func, *args):
        self.func = func
        self.funcArgs = args




# tells a menu how to layout its children.
class layoutManager ():
    paddingX = 1
    paddingY = 1
    horizontal = None
    wrap = False

    def __init__ (self, horizontal = None, wrap = False):
        self.horizontal = horizontal
        self.wrap = wrap

    # sets the position of all the animObjects in a list in a way specified by the menu
    def set (self, objects: list, pos: tuple, size: tuple):
        strideX = 0
        strideY = 0
        for item in objects:
            if self.horizontal == True:
                # check if wrapping
                if self.wrap:
                    if size[0] < strideX + self.paddingX + item.width:
                        strideX = 0
                        strideY += item.height + self.paddingY
                        item.setXY(pos[0] + strideX, pos[1] + strideY)
                else:
                    item.setXY(pos[0] + strideX, pos[1] + strideY)
                strideX += item.width + self.paddingX
            elif self.horizontal == False:
                # check if wrapping
                if self.wrap:
                    if size[1] < strideY + self.paddingY + item.height:
                        strideY = 0
                        strideX += item.height + self.paddingY
                        item.setXY(pos[0] + strideX, pos[1] + strideY)
                else:
                    item.setXY(pos[0] + strideX, pos[1] + strideY)
                strideY += item.height + self.paddingY
            else:
                pass





# menu object that holds other drawObjects.
class menu (drawObject):
    objects = None
    open = True
    manager = None
    

    #constructor
    def __init__ (self, size: tuple, manager = None, path = ""):
        super().__init__(size, path)
        self.objects = []
        self.manager = manager
    
    # draws the menu and its children if it is open.
    def draw (self, window: pygame.surface.Surface):
        if self.open:
            super().draw(window)
            for i in self.objects:
                i.draw(window)

    # toggles the state of the menu
    def toggle (self):
        self.open = not self.open

    # checks if object is within the bounds of this menu.
    def isWithin (self, obj: drawObject):
        if self.x > obj.x or self.x + self.width < obj.x:
            return False
        if self.y > obj.y or self.y + self.width < obj.y:
            return False
        return True
    
    # adds a child to the menu and sets its position in the layout if managed.
    def addItem (self, obj: drawObject, lock = False):
        self.objects.append(obj)
        if self.manager != None:
            self.manager.set(self.objects, (self.x, self.y), (self.width, self.height))
        else:
            if lock and not self.isWithin(obj):
                obj.setXY(self.x, self.y)

    # sets position of the menu and updates the positions of children if managed.
    def setXY(self, dx, dy):
        super().setXY(dx, dy)
        if self.manager != None:
            self.manager.set(self.objects, (self.x, self.y), (self.width, self.height))

