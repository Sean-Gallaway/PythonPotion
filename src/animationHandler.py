import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import *
from pyvidplayer2 import *
from animationObject import *
from enum import Enum

# container for all the pre-rendered animations
class animations(Enum):
    MIX = "potion_game\\animation\\mix.mp4"
    CHOP = "potion_game\\animation\\chop.mp4"
    IDLE = "potion_game\\animation\\idle.mp4"
currentAnim = animations.IDLE;

# function that sets the current background video
def anim (a: animations):
    global vid
    global winSize
    global currentAnim
    vid.stop()
    vid = Video(a[0].value)
    vid.resize(winSize)
    currentAnim = a




# setup window
winSize = (int(1920/2), int(1080/2))
pygame.init()
window = pygame.display.set_mode(winSize)
pygame.display.set_caption("Potion Game")

# setup background
vid = Video("potion_game\\animation\\idle.mp4")
vid.resize( winSize );
vidSurface = pygame.surface.Surface( winSize )

#
btn1 = btn("mix", (200, .6*(winSize[1]/3) ))
btn1.setXY(200, 2.2*winSize[1]/3)
btn1.bindFunction(anim, animations.MIX)
#

#
btn2 = btn("chop", (200, .6*(winSize[1]/3) ))
btn2.setXY(0, 2.2*winSize[1]/3)
btn2.bindFunction(anim, animations.CHOP)
#

# Bottom menu
obj = menu((winSize[0], winSize[1]/3), manager=layoutManager(horizontal=False))
obj.setXY(0, 2*winSize[1]/3)

submenu = menu((500, 200), manager=layoutManager(horizontal=True))
submenu.addItem(btn1, lock=True)
submenu.addItem(btn2, lock=True)

obj.addItem(label("Test", (200, 50) ))
obj.addItem(submenu)
obj.keyAction(K_ESCAPE, obj.toggle)
#

#
ingredientMenu = menu((winSize[0]*.7, winSize[1]*.7), manager=layoutManager(horizontal=False))
ingredientMenu.setXY(winSize[0]*.15, winSize[1]*.15)
#


'''
Chop animation:
    acquired item
mix animation: 
finish animation:
    puff of smoke
        menu screen popup
'''



play = True
keys_pressed = None

while play:
    keys_pressed = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            vid.stop()
            play = False
   
        if event.type == pygame.KEYUP:
            obj.ifAction(keys_pressed)
   
        if event.type == MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            for btn in buttonList:
                btn.cursorInBounds(mpos)
    
    if vid.draw(vidSurface, (0, 0), force_draw=False):
        pygame.display.update()

    if not vid.active:
        if currentAnim == animations.IDLE:
            vid.restart()
        else:
            vid = Video(animations.IDLE.value)
            currentAnim = animations.IDLE
            vid.resize(winSize)
        

    window.blit(vidSurface, (0, 0))
    obj.draw(window)

    pygame.display.update()
    pygame.time.wait(16) # around 60 fps

pygame.quit()