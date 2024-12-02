import animationGlobals as ag
from animationObject import *
from screens import *

mainMenu(ag.scene)
import driver as dr
scoreboard = label("Score: " + str(dr.score), fontSize=winSize[0]*0.02, size=(winSize[0]*.2, winSize[1]*.09), center=True, fontColor=(255, 255, 255, 255))
scoreboard.setBackgroundColor(0, 0, 0, 150, outline=5, outlineColor=(255, 255, 255, 255))
scoreboard.setXY(0, 0)
scoreboardPoll = 0

def playGame():
    global dt
    global currentAnim
    global anim
    global vid
    play = True
    keys_pressed = None
    while play:
        keys_pressed = pygame.key.get_pressed()
        dt = ag.clock.tick(60) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ag.vid.stop()
                play = False
    
            if event.type == pygame.KEYUP:
                for widget in actionList:
                    if len(widget.animations) != 0:
                        widget.ifAction(keys_pressed)
    
            if event.type == MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                for btn in buttonList:
                    btn.cursorInBounds(mpos)
        
        if ag.vid.draw(ag.vidSurface, (0, 0), force_draw=False):
            pygame.display.update()

        if not ag.vid.active:
            if ag.currentAnim == ag.animations.IDLE or ag.currentAnim == ag.animations.MAIN:
                ag.vid.restart()
            else:
                ag.vid = Video(ag.animations.IDLE.value)
                ag.currentAnim = ag.animations.IDLE
                ag.vid.resize(winSize)
            

        ag.window.blit(ag.vidSurface, (0, 0))
        try:
            for k, item in ag.scene.items():
                item.draw(ag.window)
        except:
            pass
        
        if ag.currentAnim != ag.animations.MAIN:
            global scoreboardPoll
            scoreboardPoll += 1
            if scoreboardPoll == 60:
                scoreboardPoll = 0
                scoreboard.setText("Score: " + str(dr.score), center=True)
            scoreboard.draw(ag.window) 
        pygame.display.update()
        pygame.time.wait(16) # around 60 fps
playGame()
pygame.quit()