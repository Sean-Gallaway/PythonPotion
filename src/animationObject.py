import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import *
import pygame


buttonList = []
font = pygame.font.SysFont('Corbel',35) 


# base class for anything being drawn to the screen.
class drawObject ():
    x = 0
    y = 0
    width = 0
    height = 0
    obj = None

    # constructor
    def __init__ (self, size: tuple):
        self.width = size[0]
        self.height = size[1]
        self.obj = pygame.surface.Surface(size, pygame.SRCALPHA, 32 )
        self.obj.fill((0, 0, 0, 180))

    # draws this object to a given surface
    def draw (self, window: pygame.surface.Surface):
        window.blit(self.obj, (self.x, self.y))

    # sets the position of this object using screen space coordinates.
    def setXY (self, dx, dy):
        self.x = dx
        self.y = dy


# classic label.
class label (drawObject):
    text = None
    textSize = None

    # constructor
    def __init__ (self, msg: str, size: tuple):
        super().__init__(size)
        self.obj.fill((100, 100, 100, 255))
        self.text = font.render(msg, True, (0, 0, 0))
        self.textSize = font.size(msg)

    # draws this object and its text to a given surface.
    def draw (self, window: pygame.surface.Surface):
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

    # check if the cursor is in the bounds of this button
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
        self.funcArgs = args;

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

#triggerable object
class triggerable ():
    # check if the pressed keys match any of the keyAction trigger keys.
    # list comprehension could make this better, but this works.
    def ifAction(self, keys):
        for key in self.keyActions.keys():
            if keys[key]:
                if callable(self.keyActions[key]):
                    self.keyActions[key]()
    
    # sets an action to activate when a key is pressed.
    def keyAction (self, key: int, func):
        self.keyActions[key] = func

# says how to animate a drawObject
class anim ():
    startPos = None
    currPos = None
    endPos = None
    interpol = None
    duration = None

    def __init__ (self, dxdy: tuple, duration: float, interpol = None, xy = None, ):
        self.endPos = dxdy
        self.duration = duration
        self.interpol = interpol
        self.startPos = xy

    def start (self, obj: drawObject):
        # if we have a defined start position, we should start there, otherwise we will start where the
        # object currently is located at.
        if self.startPos != None:
            self.currPos = self.startPos
        else:
            self.currPos = (obj.x, obj.y)

    def advance (self, timeStep: float):
        try:
            # use the interpolation function given when this object is created to go from
            # point A to point B with a given time interval.
            t = timeStep/self.duration
            x = self.interpol(self.currPos[0], self.endPos[0], t)
            y = self.interpol(self.currPos[1], self.endPos[1], t)
        except:
            print("smoothing function failed.")

# menu object that holds other drawObjects.
class menu (drawObject, triggerable):
    objects = None
    open = True
    manager = None
    keyActions = {}

    #constructor
    def __init__ (self, size: tuple, manager = None):
        super().__init__(size)
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

