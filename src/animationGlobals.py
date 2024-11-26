import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import *
import pygame

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