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
    import customer as cust
    btn1.bindFunction(cust.getDailyCustomers, None)

    # btn2 = btn("Options", (winSize[0]*.25, winSize[1]*.075), path="potion_game\\assets\\paper.png", center=True)
    submenu.addItem(btn1)
    # submenu.addItem(btn2)
    #
    scene["la"] = la
    scene["root"] = obj
    

def mixScreen (scene):
    outline = 10
    root = menu((0, 0))

    obj = menu((winSize[0], winSize[1]*.15))
    obj.setBackgroundColor(0, 0, 0, 150, outline=outline, outlineColor=(255, 255, 255, 200))
    obj.setXY(0, winSize[1]*1.5)
    obj.addAnim("open", animation(1, dxdy=(0, winSize[1]*.85), interpol=eioCubic))
    obj.playAnim("open")


    #
    btn1 = btn("Ingredients", size=(winSize[0]*.25, winSize[1]*.115), fontSize=winSize[0]*0.03, fontColor=(255, 255, 255, 255), center=True)
    btn1.setXY(outline, winSize[1]*1.505+outline)
    btn1.setBackgroundColor(0, 0, 0, 100, outline=outline/2, outlineColor=(255, 255, 255, 200))
    btn1.bindFunction(popup, ("ing") )


    def printInv(*args):
        import driver as dr
        for i in dr.user.inv.storage:
            print(i.name)

    btn3 = btn("Inventory", size=(winSize[0]*.225, winSize[1]*.115), fontSize=winSize[0]*0.03, fontColor=(255, 255, 255, 255), center=True)
    btn3.setBackgroundColor(0, 0, 0, 150, outline=outline/2, outlineColor=(255, 255, 255, 200))
    btn3.bindFunction(printInv, None)
    btn3.setXY(outline*2+btn1.obj.get_width(), winSize[1]*1.505+outline)
    #


    #
    customerMenu = menu((winSize[0]*.5, winSize[1]*.5))
    customers = menu((winSize[0]*.5-outline, winSize[1]*.4), manager=layoutManager(horizontal=False))
    customerDone = btn("Done", size=(winSize[0]*.15, winSize[1]*.075), fontSize=winSize[0]*0.03, fontColor=(255, 255, 255, 255), center=True)

    customerMenu.addItem(customers)
    customerMenu.addItem(customerDone)

    customerMenu.setXY(winSize[0]*.25, winSize[1]*2)
    customers.setXY(customerMenu.x+outline/2, customerMenu.y+outline/2)
    customerDone.setXY(customerMenu.x+customerMenu.width-customerDone.width-outline/2, customerMenu.y+customerMenu.height-customerDone.height-outline/2)

    customerMenu.addAnim("open", animation(.5, dxdy=(winSize[0]*.25, winSize[1]*.25), interpol=eioCubic, consumable=False))
    customerMenu.addAnim("close", animation(.5, dxdy=(winSize[0]*.25, winSize[1]*2), interpol=eioCubic, consumable=False))
    customerDone.bindFunction(customerMenu.playAnim, "close")

    customerMenu.setBackgroundColor(0, 0, 0, 150, outline=outline/2, outlineColor=(255, 255, 255, 200))
    customers.setBackgroundColor(0, 0, 0, 150)
    import customer as cust
    import ingredient as ig
    for c in cust.customers:
        custRow = menu((winSize[0]*.5-outline*1.25, winSize[1]*.1))
        custRow.setBackgroundColor(0, 0, 0, 150, outline=outline/2, outlineColor=(255, 255, 255, 200))
        custIcon = drawObject((winSize[1]*.09, winSize[1]*.09))
        custIcon.setBackgroundColor(100, 0, 0, 255)
        customers.addItem(custRow)
        custRow.addItem(custIcon)
        custIcon.setXY(custRow.x+winSize[1]*.005, custRow.y+winSize[1]*.005)

        custWant = label(c.wants(), fontSize=winSize[0]*0.015, size=(winSize[0]*.35, winSize[1]*.09), fontColor=(255, 255, 255, 255), lockSize=True)
        custWant.setBackgroundColor(0, 0, 0, 150)
        custRow.addItem(custWant)
        custWant.setXY(custRow.x+custIcon.width+outline/2, custRow.y+winSize[1]*0.005)

        give = btn("Give Potion", size=(winSize[0]*.075, winSize[1]*.05), fontSize=winSize[0]*0.01, fontColor=(255, 255, 255, 255), center=True)
        give.setXY(custRow.x+custRow.width-give.width-outline*.8, custRow.y+winSize[1]*0.025)
        give.setBackgroundColor(0, 0, 0, 150, outline=outline/2, outlineColor=(255, 255, 255, 200))
        give.bindFunction(c.evaluateGivenPotion, None)
        give.bindFunction(customerMenu.playAnim, "close")
        custRow.addItem(give)
    #

    #
    btn2 = btn("Brew", fontColor=(255, 255, 255, 255))
    btn2.setXY(winSize[0]-btn2.width-outline, winSize[1]*1.505+outline)
    btn2.setBackgroundColor(0, 0, 0, 100, outline=outline/2, outlineColor=(255, 255, 255, 200))
    btn2.bindFunction(customerMenu.playAnim, "open")

    # btn2.bindFunction(ig.generatePotion, None)

    
    # addIng = menu((winSize[0]*.5, winSize[1]*.5))
    # addIng.setXY(winSize[0]*.25, winSize[1])
    # addIng.setBackgroundColor(0, 0, 0, 150, outline=outline, outlineColor=(255, 255, 255, 200))
    # addIng.addAnim("openIng", animation(1, dxdy=(winSize[0]*.25, winSize[1]*.25), interpol=eioCubic))
    # addIng.keyAction(K_b, addIng.playAnim, "openIng")

    

    #
    btn4 = btn("Next Day", size=(winSize[0]*.25, winSize[1]*.115), fontSize=winSize[0]*0.05, fontColor=(255, 255, 255, 255), center=True)
    btn4.setBackgroundColor(0, 0, 0, 150, outline=outline, outlineColor=(255, 255, 255, 200))
    btn4.bindFunction(transitionScene, (.5, 1, ag.animations.MAIN, customerScreen))
    btn4.setXY(winSize[0]-btn4.obj.get_width(), -winSize[1])
    btn4.addAnim("open", animation(1, dxdy=(winSize[0]-btn4.obj.get_width(), 0), interpol=eioCubic))
    btn4.playAnim("open")
    #


    root.addItem(obj)
    obj.addItem(btn1)
    obj.addItem(btn2)
    obj.addItem(btn3)
    # root.addItem(addIng)
    root.addItem(btn4)
    root.addItem(customerMenu)


    scene["root"] = root

def customerScreen():
    pass