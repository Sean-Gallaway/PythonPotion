import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import *
import pygame
from pyvidplayer2 import *
from enum import Enum

# just using ktinker for screen size
from tkinter import *
root = Tk()
height = root.winfo_screenheight()
width = root.winfo_screenwidth()
#

# setup window
winSize = (int(width/2), int(height/2))
pygame.init()
window = pygame.display.set_mode(winSize)
pygame.display.set_caption("Potion Game")


clock = pygame.time.Clock();
dt = clock.tick(60) / 1000

scene = {}

# container for all the pre-rendered animations
class animations(Enum):
    MIX = "potion_game\\animation\\mix.mp4"
    CHOP = "potion_game\\animation\\chop.mp4"
    IDLE = "potion_game\\animation\\idle.mp4"
currentAnim = animations.IDLE;

# setup background
vid = Video("potion_game\\animation\\main.mp4")
vid.resize( winSize );
vidSurface = pygame.surface.Surface( winSize )

def removeFromScene(args: tuple):
    for item in args:
        try:
            del scene[item]
        except:
            print("failed removal")

def addToScene(args: tuple):
    for item in args:
        scene[item[0]] = item[1]


# function that sets the current background video
def anim (a: animations):
    global vid
    global winSize
    global currentAnim
    vid.stop()

    if type(a) is list or type(a) is tuple:
        print(a[0])
        vid = Video(a[0].value)
    else:
        vid = Video(a.value)
    vid.resize(winSize)

    currentAnim = a




