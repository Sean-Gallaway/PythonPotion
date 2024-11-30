import animationGlobals as ag
from animationGlobals import winSize
from animationObject import *

def mainMenu(scene):
    # main menu
    obj = menu((winSize[0]*.8, winSize[1]*.8), path="potion_game\\assets\\mainmenu.png")
    obj.setXY(winSize[0]*.1, winSize[1]+200)
    obj.addAnim("Enter", animation(.5, dxdy=(winSize[0]*.1, winSize[1]*.1), interpol=eioCubic))
    obj.keyAction(K_ESCAPE, obj.playAnim, "Enter")

    l2 = label("Potion Game", fontSize=50, center=True)
    l2.setBackgroundColor(0, 0, 0, 0)
    l2.setXY(winSize[0]*.57, winSize[1]*1.365)
    obj.addItem(l2)

    la = label("Press ESC to start.", fontSize = 60, fontColor=(255, 255, 255, 255), center=True)
    la.setBackgroundColor(0, 0, 0, 100)
    la.setXY(winSize[0]/2, winSize[1]/2-100, True)
    #

    # main menu options
    submenu = menu((winSize[0]*.25, winSize[1]*.6), manager=layoutManager(horizontal=False, paddingY = winSize[1]*0.05))
    submenu.setXY(winSize[0]*.575, winSize[1]*1.4875)
    submenu.setBackgroundColor(0, 0, 0, 0)
    obj.addItem(submenu)

    btn1 = btn("Start", (winSize[0]*.25, winSize[1]*.075), path="potion_game\\assets\\paper.png", center=True)
    btn1.bindFunction(transitionScene, (.5, 1, ag.animations.IDLE, mixScreen))
    btn2 = btn("Options", (winSize[0]*.25, winSize[1]*.075), path="potion_game\\assets\\paper.png", center=True)
    submenu.addItem(btn1)
    submenu.addItem(btn2)
    #
    scene["la"] = la
    scene["root"] = obj
    

def mixScreen (scene):
    outline = 10
    obj = menu((winSize[0], winSize[1]*.15))
    obj.setBackgroundColor(0, 0, 0, 150, outline=outline, outlineColor=(255, 255, 255, 200))
    obj.setXY(0, winSize[1]*1.5)
    obj.addAnim("open", animation(1, dxdy=(0, winSize[1]*.85), interpol=eioCubic))
    obj.playAnim("open")

    btn1 = btn("Ingredients", fontColor=(255, 255, 255, 255))
    btn1.setXY(outline, winSize[1]*1.505+outline)
    btn1.setBackgroundColor(0, 0, 0, 100, outline=outline/2, outlineColor=(255, 255, 255, 200))
    btn1.bindFunction(popup, ("ing") )

    btn2 = btn("Brew", fontColor=(255, 255, 255, 255))
    btn2.setXY(winSize[0]-btn2.width-outline, winSize[1]*1.505+outline)
    btn2.setBackgroundColor(0, 0, 0, 100, outline=outline/2, outlineColor=(255, 255, 255, 200))


    obj.addItem(btn1)
    obj.addItem(btn2)

    scene["root"] = obj