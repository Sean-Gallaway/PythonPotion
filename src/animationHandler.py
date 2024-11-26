from animationGlobals import *
from pyvidplayer2 import *
from animationObject import *
from enum import Enum
from easingFunctions import *


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

# setup background
vid = Video("potion_game\\animation\\main.mp4")
vid.resize( winSize );
vidSurface = pygame.surface.Surface( winSize )


obj = menu((300, 300), path="potion_game\\assets\\paper.png", manager=layoutManager(horizontal=True))
obj.setXY(winSize[0]/2-300, winSize[1]+200)
obj.addAnim("Enter", animation((winSize[0]/2-300, winSize[1]/10), .5, interpol=eioCubic) )
obj.keyAction(K_ESCAPE, obj.playAnim, "Enter")

l2 = label("Hi", fontSize=50)
l2.setBackgroundColor(0, 0, 0, 0)
obj.addItem(l2, lock=True)

# img =  pygame.image.load("potion_game\\assets\\paper.png")
# isize = img.get_rect()
# img = pygame.transform.scale(img, (isize[0]*2, isize[1]*2))

la = label("Press ESC to start.", fontSize = 60, fontColor=(255, 255, 255, 255))
la.setBackgroundColor(0, 0, 0, 100)
la.setXY(winSize[0]/2, winSize[1]/2-100, True)
laa = animation((winSize[0]/2-300, -100), .05, interpol=eioCubic)
la.addAnim("Enter", laa)
la.keyAction(K_ESCAPE, la.playAnim, "Enter")



# #
# btn1 = btn("mix", (200, .6*(winSize[1]/3) ))
# btn1.setXY(200, 2.2*winSize[1]/3)
# btn1.bindFunction(anim, animations.MIX)
# #

# #
# btn2 = btn("chop", (200, .6*(winSize[1]/3) ))
# btn2.setXY(0, 2.2*winSize[1]/3)
# btn2.bindFunction(anim, animations.CHOP)
# #

# # Bottom menu
# obj = menu((winSize[0], winSize[1]/3), manager=layoutManager(horizontal=False))
# obj.setXY(0, 2*winSize[1]/3)

# submenu = menu((500, 200), manager=layoutManager(horizontal=True))
# submenu.addItem(btn1, lock=True)
# submenu.addItem(btn2, lock=True)

# obj.addItem(label("Test", (200, 50) ))
# obj.addItem(submenu)
# obj.keyAction(K_ESCAPE, obj.toggle)
# #

# #
# ingredientMenu = menu((winSize[0]*.7, winSize[1]*.7), manager=layoutManager(horizontal=False))
# ingredientMenu.setXY(winSize[0]*.15, winSize[1]*.15)
# #


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
    dt = clock.tick(60) / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            vid.stop()
            play = False
   
        if event.type == pygame.KEYUP:
            for widget in actionList:
                print(widget)
                widget.ifAction(keys_pressed)
   
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
    la.draw(window)

    pygame.display.update()
    pygame.time.wait(16) # around 60 fps

pygame.quit()