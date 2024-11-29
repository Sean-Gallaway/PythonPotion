from enum import Enum
import animationGlobals as ag
from pygame import *
import pygame
from easingFunctions import *
from pyvidplayer2 import *
from animationGlobals import winSize

buttonList = []
actionList = []
ingOpen = False

# params: fade in, fade out, scene
def transitionScene (args: tuple):
    buttonList.clear()
    actionList.clear()
    transition = drawObject(ag.winSize)
    transition.setBackgroundColor(0, 0, 0, 0)
    transition.addAnim("fadein", animation(args[0], 255, interpol=eioCubic, type=animType.FADE, func=[(ag.anim, ag.animations(args[2])), (transition.playAnim, "fadeout")] ))
    transition.addAnim("fadeout", animation(args[1], 0, interpol=eioCubic, type=animType.FADE, func=[(ag.scene.clear, None), (args[3], ag.scene)] ))
    ag.scene.clear()
    ag.scene["tran"] = (transition)
    transition.playAnim("fadein")


def ingOpenSet (open):
    global ingOpen
    ingOpen = open


def popup(args: tuple):
    m = cMenu((winSize[0]*.5, winSize[1]*.5), args[0], manager=layoutManager(horizontal=True, outerPaddingX=10, outerPaddingY=10))
    m.setBackgroundColor(0, 0, 0, 150, outline=10, outlineColor=(255, 255, 255, 200))
    m.setXY(winSize[0]*.25, winSize[1]*.25)
    ag.scene[args[0]] = m

    import ingredient as i
    def ingredientInfo (ing: i.IngredientType):
        global ingOpen
        print(ingOpen)
        if ingOpen:
            return
        ingOpen = True

        outlineSize = 10
        thisWin = (winSize[0]*.25, winSize[1]*.25)
        im = cMenu(thisWin, "ingWin")
        im.setBackgroundColor(0, 0, 0, 150, outline=outlineSize, outlineColor=(255, 255, 255, 200))
        im.setXY(winSize[0]*.5, winSize[1]*.35)
        ag.scene["ingWin"] = im
        im.exitBtn.bindFunction(ingOpenSet, False)

        name = label(ing.value["name"], fontSize=20, fontColor=(255, 255, 255, 255))
        im.addItem(name)
        name.setXY(winSize[0]*.5+outlineSize, winSize[1]*.35+outlineSize)
        name.setBackgroundColor(0,0,0,0)

        desc = label(ing.value["desc"], size=(thisWin[0]*.9, thisWin[1]*.1), fontSize=20, fontColor=(255, 255, 255, 255) )
        desc.setXY(winSize[0]*.5+outlineSize, winSize[1]*.4+outlineSize)
        im.addItem(desc)
        desc.setBackgroundColor(0,0,0,0)

        btnMenu = menu((thisWin[0], thisWin[1]*.1), manager=layoutManager(horizontal=True))
        btnMenu.setBackgroundColor(0, 0, 0, 0)
        btnMenu.setXY(winSize[0]*.5+outlineSize, winSize[1]*.6-thisWin[1]*.11-outlineSize)

        mix = btn("Add to Mix", size=(thisWin[0]*.4, thisWin[1]*.1), center=True, fontColor=(255, 255, 255, 255))
        mix.setBackgroundColor(0, 0, 0, 150, outline=outlineSize/2, outlineColor=(255, 255, 255, 200))
        mix.bindFunction(i.addIngredient, ing)
        mix.bindFunction(im.exitBtn.forceTrigger, None)
        mix.bindFunction(ag.anim, ag.animations.MIX)
        mix.bindFunction(m.exitBtn.forceTrigger, None)
        mix.bindFunction(ingOpenSet, False)
        btnMenu.addItem(mix)
        
        if ing.value["chop"]:
            chop = btn("Chop up and Mix", size=(thisWin[0]*.5, thisWin[1]*.1), center=True, fontColor=(255, 255, 255, 255) )
            chop.setBackgroundColor(0, 0, 0, 150, outline=outlineSize/2, outlineColor=(255, 255, 255, 200))
            chop.bindFunction(ag.anim, ag.animations.CHOP)
            chop.bindFunction(im.exitBtn.forceTrigger, None)
            chop.bindFunction(m.exitBtn.forceTrigger, None)
            chop.bindFunction(ingOpenSet, False)
            btnMenu.addItem(chop)

        im.addItem(btnMenu)



    dir = "potion_game\\assets\\ingredients\\"
    for val in i.IngredientType:
        b = btn(" ",  (winSize[0]*.05, winSize[0]*.05), path=dir+val.value["icon"])
        b.bindFunction(ingredientInfo, (val))
        m.addItem(b)
        




#triggerable object
class triggerable ():
    keyActions = None
    def __init__ (self):
        self.keyActions = {}

    # check if the pressed keys match any of the keyAction trigger keys.
    def ifAction(self, keys):
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

    # constructor
    def __init__ (self, size: tuple, path = "", outline = 0, outlineColor = (0, 0, 0, 255)):
        self.width = size[0]
        self.height = size[1]
        self.x = 0
        self.y = 0
        self.currentAnimation = None
        self.background = (100, 100, 100, 255)

        if path != "":
            self.obj = pygame.image.load(path)
            self.obj = pygame.transform.scale(self.obj, size)
        else:
            self.obj = pygame.surface.Surface(size, pygame.SRCALPHA, 32 )
            if outline != 0:
                self.obj.fill(outlineColor)
                self.obj.fill(self.background, self.obj.get_rect().inflate(-outline, -outline))
            else:
                self.obj.fill(self.background)
        self.animations = {}
        super().__init__()

    # draws this object to a given surface. 
    def draw (self, window: pygame.surface.Surface):
        if self.currentAnimation != None:
            self.currentAnimation.advance(ag.dt)
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
    def setBackgroundColor (self, r, g, b, a, outline = 0, outlineColor = (0, 0, 0, 255)):
        self.background = (r, g, b, a)
        if outline != 0:
            self.obj.fill(outlineColor)
            self.obj.fill(self.background, self.obj.get_rect().inflate(-outline, -outline))
        else:
            self.obj.fill(self.background)

    # add to the animation dictionary of this object
    def addAnim(self, name: str, a: 'animation'):   
        self.animations[name] = a

    def removeAnim(self, name: str):
        del self.animations[name]

    # play an animation from the dictionary
    def playAnim(self, name):
        if type(name) is list or type(name) is tuple:
            self.currentAnimation = self.animations[name[0]]
            self.currentAnimation.start(self, name[0])
        else:
            self.currentAnimation = self.animations[name]
            self.currentAnimation.start(self, name)




class animType(Enum):
    MOVEMENT = 0,
    FADE = 1




# says how to animate a drawObject
class animation ():

    def __init__ (self, duration: float, dxdy, interpol = None, type = animType.MOVEMENT, func = None):
        self.endPos = dxdy
        self.duration = duration
        self.interpol = interpol
        self.type = type
        self.func = func

    # start an animation, the start position should be the objects current position to make things make sense.
    def start (self, obj: drawObject, name):
        self.name = name
        self.time = 0
        self.subject = obj
        self.playing = True
        if self.type == animType.MOVEMENT:
            self.startPos = (obj.x, obj.y)
        elif self.type == animType.FADE:
            self.startPos = list(obj.background)

    # advances the animation based on a timeStep, usually delta time.
    # in other programs it might not make total sense why we use delta time over other options,
    # but here it is because the animation happens in a fixed timeframe, regardless of the easing function
    def advance (self, timeStep: float):
        if self.playing == False and self.name in self.subject.animations:
            self.subject.removeAnim(self.name)
            # run functions after animation is done
            if self.func is not None:
                if type(self.func) is list:
                    for function in self.func:
                        if function[1] != None:
                            function[0](function[1])
                        else:
                            function[0]()
                else:
                    if self.func[1] != None:
                        self.func[0](self.func[1])
                    else:
                        self.func[0]()
            return
        try:
            # use the interpolation function given when this object is created to go from
            # point A to point B with a given time interval.
            if self.duration < self.time:
                self.playing = False

            self.time += timeStep

            if self.type == animType.MOVEMENT:
                x = self.interpol(self.startPos[0], self.endPos[0], min(1, self.time/self.duration) )
                y = self.interpol(self.startPos[1], self.endPos[1], min(1, self.time/self.duration) )
                self.subject.setXY(x, y)
            elif self.type == animType.FADE:
                color = self.interpol(self.startPos[3], self.endPos, min(1, self.time/self.duration))
                full = self.subject.background
                self.subject.setBackgroundColor(full[0], full[1], full[2], color)
                

        except Exception as e:
            print(e)
            print("smoothing function failed.")




# classic label.
class label (drawObject):

    # constructor
    def __init__ (self, msg: str, size: tuple = None, fontSize: float = -1, fontColor = (0, 0, 0, 255), path = "", center = False, outline = 0, outlineColor = (0, 0, 0, 255)):
        self.center = center
        if fontSize == -1 and size is None:
            print("Error with label, size or fontSize must be defined.")
            return

        # if we do not define a font size, we should probably make it a ratio of the size of the container.
        if fontSize == -1:
            fontSize = size[0] * .5
        font = pygame.font.SysFont('couriernew', int(fontSize)) 
        
        # define our size if we don't have a defined size, this is important for the future text splitting step.
        self.textSize = font.size(msg)
        if size is None:
            size = self.textSize

        # splits text and figures out where we should wrap it.
        words = msg.split()

        # now, construct lines out of these words
        self.textList = []
        while len(words) > 0:
            # get as many words as will fit within allowed_width
            line_words = []
            while len(words) > 0:
                line_words.append(words.pop(0))
                fw, fh = font.size(' '.join(line_words + words[:1]))
                if fw > size[0]:
                    break

            # add a line consisting of those words
            line = ' '.join(line_words)
            self.textList.append(line)


        # convert our textList into the pygame text objects so they can be rendered.
        self.text = []
        for t in self.textList:
            r = font.render(t, True, fontColor)
            self.text.append(r)

        if len(self.text) > 1:
            size = list(size)
            size[1] *= len(self.textList)
            size = tuple(size)

        super().__init__(size, outline=outline, outlineColor=outlineColor, path=path)


    # draws this object and its text to a given surface.
    def draw (self, window: pygame.surface.Surface):
        if self.currentAnimation != None:
            self.currentAnimation.advance(ag.dt)
        window.blit(self.obj, (self.x, self.y))


        # window.blit(self.text, (self.x+(self.width/2-self.textSize[0]/2), self.y+(self.height/2-self.textSize[1]/2)))
        offset = 0
        for t in self.text:
            if self.center:
                window.blit(t, (self.x+(self.width/2-self.textSize[0]/2), self.y+(self.height/2-self.textSize[1]/2)+offset))
            else:
                window.blit(t, (self.x, self.y+offset ))
            offset += self.textSize[1]




# classic button, does a thing if you bind a function to it.
class btn (label):

    # constructor
    def __init__ (self, msg: str, size: tuple = None, path = "", center = False, fontColor = (0, 0, 0, 255), outline = 0, outlineColor = (0, 0, 0, 255)):
        buttonList.append(self)
        self.func = []
        self.funcArgs = []
        if size is None:
            super().__init__(msg, size, outline=outline, outlineColor=outlineColor, fontSize = ag.winSize[1]*.1, path=path, center=center, fontColor=fontColor)
        else:
            super().__init__(msg, size, outline=outline, outlineColor=outlineColor, fontSize = size[1]*.9, path=path, center=center, fontColor=fontColor)

    def forceTrigger (self, *args):
        for a in range(0, len(self.func)):
            if type(self.funcArgs[a][0]) is str:
                self.func[a](self.funcArgs[a][0])
            elif type(self.funcArgs[a]) is None:
                self.func[a]()
            else:
                self.func[a](self.funcArgs[a][0])

    # check if the cursor is in the bounds of this button using screen space
    def cursorInBounds (self, mouse: list):
        if not (self.x < mouse[0] and mouse[0] < self.x + self.width):
            return
        if not (self.y < mouse[1] and mouse[1] < self.y + self.height):
            return
        # try to run the bound function
        for a in range(0, len(self.func)):
            # print(self.func[a].__name__, "\t", self.funcArgs[a])
            if type(self.funcArgs[a][0]) is str:
                self.func[a](self.funcArgs[a][0])
            elif type(self.funcArgs[a]) is None:
                self.func[a]()
            else:
                self.func[a](self.funcArgs[a][0])

            # print(self.funcArgs[a])
            # argString = ""
            # for val in range(len(self.funcArgs[a])):
            #     print(type(self.funcArgs[a][val]) )
            #     if callable(self.funcArgs[a][val]):
            #         print("agh")
            #         argString += self.funcArgs[a][val].__name__
            #     else:
            #         argString += str(self.funcArgs[a][val])
            #     if val != len(self.funcArgs[a])-1:
            #         argString += ", "

            # import importlib, screens
            # globals().update(importlib.import_module('screens').__dict__)
            # string = str(self.func[a].__name__) + "(" + argString + ")"
            # print(string)
            # exec(string, {'animations': ag.animations}, globals())


    # binds a function to this button to be ran when this button is clicked.
    def bindFunction (self, func, *args):
        self.func.append(func)
        if args is None:
            self.funcArgs.append(None)
        else:
            self.funcArgs.append(args)




# tells a menu how to layout its children.
class layoutManager ():

    def __init__ (self, horizontal = None, wrap = False, paddingX = 1, paddingY = 1, outerPaddingX = 1, outerPaddingY = 1):
        self.paddingX = paddingX
        self.paddingY = paddingY
        self.outerPaddingX = outerPaddingX
        self.outerPaddingY = outerPaddingY
        self.horizontal = horizontal
        self.wrap = wrap

    # sets the position of all the animObjects in a list in a way specified by the menu
    def set (self, objects: list, pos: tuple, size: tuple):
        strideX = self.outerPaddingX
        strideY = self.outerPaddingY
        for item in objects:
            if self.horizontal == True:
                # check if wrapping
                if self.wrap:
                    if size[0] < strideX + self.paddingX + item.width + self.outerPaddingX:
                        strideX = self.outerPaddingX
                        strideY += item.height + self.paddingY
                        item.setXY(pos[0] + strideX, pos[1] + strideY)
                else:
                    item.setXY(pos[0] + strideX, pos[1] + strideY)
                strideX += item.width + self.paddingX
            elif self.horizontal == False:
                # check if wrapping
                if self.wrap:
                    if size[1] < strideY + self.paddingY + item.height + self.outerPaddingY:
                        strideY = self.outerPaddingY
                        strideX += item.height + self.paddingY
                        item.setXY(pos[0] + strideX, pos[1] + strideY)
                else:
                    item.setXY(pos[0] + strideX, pos[1] + strideY)
                strideY += item.height + self.paddingY
            else:
                pass





# menu object that holds other drawObjects.
class menu (drawObject):

    #constructor
    def __init__ (self, size: tuple, manager = None, path = "", outline = 0, outlineColor = (0, 0, 0, 255)):
        super().__init__(size, path, outline=outline, outlineColor=outlineColor)
        self.objects = []
        self.manager = manager
        self.open = True
    
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
    def addItem (self, obj, lock = False):
        # if we pass a bunch of objs at once, we process them recursively
        if type(obj) == tuple:
            for o in obj:
                self.addItem(o)
            return
        
        self.objects.append(obj)
        if self.manager != None:
            self.manager.set(self.objects, (self.x, self.y), (self.width, self.height))
        else:
            if lock and not self.isWithin(obj):
                obj.setXY(self.x, self.y)

    # def addItem (self, objs: tuple, lock = False):
    #     for obj in objs:
    #         self.addItem(obj, lock)

    # sets position of the menu and updates the positions of children if managed.
    def setXY(self, dx, dy):
        originalX = self.x
        originalY = self.y
        if self.manager != None:
            self.manager.set(self.objects, (self.x, self.y), (self.width, self.height))
        else:
            for obj in self.objects:
                obj.setXY(dx+obj.x-originalX, dy+obj.y-originalY)
        super().setXY(dx, dy)





class cMenu (menu):
    def __init__(self, size: tuple, id, manager = None, path = "", outline = 0, outlineColor = (0, 0, 0, 255)):
        super().__init__(size, manager, path, outline=outline, outlineColor=outlineColor)
        self.exitBtn = btn("x", size=( ag.winSize[0]*.02, ag.winSize[0]*.02 ))
        self.exitBtn.setBackgroundColor(200, 0, 0, 255)
        self.exitBtn.bindFunction(ag.removeFromScene, id)
        self.exitBtn.bindFunction(self.removal, None)
        self.id = id
        self.setXY(0, 0)

    def draw (self, window: pygame.surface.Surface):
        super().draw(window)
        self.exitBtn.draw(window)

    def removal (self, *args):
        if self.exitBtn in buttonList:
            buttonList.remove(self.exitBtn)
        for item in self.objects:
            if item in buttonList:
                buttonList.remove(item)

    def setXY(self, dx, dy):
        super().setXY(dx, dy)
        self.exitBtn.setXY(dx + self.width - self.exitBtn.width + 1, dy)