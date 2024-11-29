import animationGlobals as ag
from animationGlobals import winSize
from animationObject import *

def mainMenu(scene):
    # main menu
    obj = menu((winSize[0]*.8, winSize[1]*.8), path="potion_game\\assets\\mainmenu.png")
    obj.setXY(winSize[0]*.1, winSize[1]+200)
    obj.addAnim("Enter", animation(.5, dxdy=(winSize[0]*.1, winSize[1]*.1), interpol=eioCubic) )
    obj.keyAction(K_ESCAPE, obj.playAnim, "Enter")

    l2 = label("Potion Game", fontSize=50)
    l2.setBackgroundColor(0, 0, 0, 0)
    l2.setXY(winSize[0]*.57, winSize[1]*1.365)
    obj.addItem(l2)

    la = label("Press ESC to start.", fontSize = 60, fontColor=(255, 255, 255, 255))
    la.setBackgroundColor(0, 0, 0, 100)
    la.setXY(winSize[0]/2, winSize[1]/2-100, True)
    #

    # main menu options
    submenu = menu((winSize[0]*.25, winSize[1]*.6), manager=layoutManager(horizontal=False, paddingY = winSize[1]*0.05))
    submenu.setXY(winSize[0]*.575, winSize[1]*1.4875)
    submenu.setBackgroundColor(0, 0, 0, 0)
    obj.addItem(submenu)

    btn1 = btn("Start", (winSize[0]*.25, winSize[1]*.075), path="potion_game\\assets\\paper.png")
    # btn1.bindFunction(anim, animations.IDLE)
    btn1.bindFunction(transitionScene, (.5, 1, ag.animations.IDLE, mixScreen))
    btn2 = btn("Options", (winSize[0]*.25, winSize[1]*.075), path="potion_game\\assets\\paper.png")
    submenu.addItem(btn1)
    submenu.addItem(btn2)
    #
    scene["la"] = la
    scene["root"] = obj
    

def mixScreen (scene):
    obj = cMenu((winSize[0], winSize[1]*.3), "root", path="potion_game\\assets\\paper.png", manager=layoutManager(horizontal=True, paddingX=1))
    obj.setXY(0, winSize[1]*1.5)
    obj.addAnim("open", animation(2, dxdy=(0, winSize[1]*.7), interpol=eioCubic))
    obj.playAnim("open")

    btn1 = btn("Chop")
    btn1.bindFunction(ag.anim, ag.animations.CHOP)
    btn2 = btn("Mix")
    btn2.bindFunction(ag.anim, ag.animations.MIX)
    btn3 = btn("Idle")
    btn3.bindFunction(ag.anim, ag.animations.IDLE)

    try:
        btn4 = btn("Create Menu")
        # popup = cMenu((winSize[0]*.5, winSize[1]*.5), "a", path="potion_game\\assets\\paper.png")
        btn4.bindFunction(popup, ("ing") )
        # btn4.bindFunction(ag.scene["a"].setXY)
    except Exception as e:
        print(e)
        print("btn4 no")


    obj.addItem(btn1)
    obj.addItem(btn2)
    obj.addItem(btn3)
    obj.addItem(btn4)

    scene["root"] = obj