import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import *
from pyvidplayer2 import *
from animationObject import *

winSize = (int(1920/2), int(1080/2))

pygame.init()
window = pygame.display.set_mode(winSize)
pygame.display.set_caption("Potion Game")
vid = Video("potion_game\\animation\\mix.mp4")
vid.resize( winSize );
vidSurface = pygame.surface.Surface( winSize )

obj = animObject((winSize[0], winSize[1]/3))
obj.setXY(0, 2*winSize[1]/3)

btn = abutton("idle", (200, .6*(winSize[1]/3) ))
btn.setXY(200, 2.2*winSize[1]/3)

btn2 = abutton("chop", (200, .6*(winSize[1]/3) ))
btn2.setXY(0, 2.2*winSize[1]/3)

def anim (path: str):
    global vid
    global winSize
    vid = Video(path[0])
    vid.resize( winSize );

btn.bindFunction(anim, "potion_game\\animation\\idle.mp4")
btn2.bindFunction(anim, "potion_game\\animation\\chop.mp4")

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            vid.stop()
            play = False
        if event.type == MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            for btn in buttonList:
                btn.cursorInBounds(mpos)
    if vid.draw(vidSurface, (0, 0), force_draw=False):
        pygame.display.update()

    if not vid.active:
        vid.restart()

    window.blit(vidSurface, (0, 0))
    obj.draw(window)
    btn.setXY(210, 2.2*winSize[1]/3)
    btn.draw(window)
    btn2.setXY(0, 2.2*winSize[1]/3)
    btn2.draw(window)

    pygame.time.wait(16) # around 60 fps

pygame.quit()
