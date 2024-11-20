import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import *
import pygame


class animObject ():
    x = 0
    y = 0
    width = 0
    height = 0
    obj = None

    def __init__ (self, size: tuple):
        self.width = size[0]
        self.height = size[1]
        self.obj = pygame.surface.Surface(size, pygame.SRCALPHA, 32 )
        self.obj.fill((100, 100, 100, 120))

    def draw (self, window: pygame.surface.Surface):
        window.blit(self.obj, (self.x, self.y))

    def setXY (self, dx, dy):
        self.x = dx
        self.y = dy



buttonList = []

font = pygame.font.SysFont('Corbel',35) 
class abutton (animObject):
    func = None
    funcArgs = None
    text = None
    textSize = None

    # constructor
    def __init__ (self, msg: str, size: tuple):
        super().__init__(size)
        buttonList.append(self)
        self.obj.fill((100, 100, 100, 255))
        self.text = font.render(msg, True, (0, 0, 0))
        self.textSize = font.size(msg)

    #
    def draw (self, window: pygame.surface.Surface):
        window.blit(self.obj, (self.x, self.y))
        window.blit(self.text, (self.x+(self.width/2-self.textSize[0]/2), self.y+(self.height/2-self.textSize[1]/2)))

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