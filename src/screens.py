import animationGlobals as ag
from animationGlobals import winSize
from animationObject import *

def mainMenu(scene):
    # main menu
    obj = menu((winSize[0]*.8, winSize[1]*.8), path="potion_game\\assets\\mainmenu.png")
    obj.setXY(winSize[0]*.1, winSize[1]*1.35)
    obj.addAnim("Enter", animation(.5, dxdy=(winSize[0]*.1, winSize[1]*.1), interpol=eioCubic))
    obj.keyAction(K_ESCAPE, obj.playAnim, "Enter")

    l2 = label("Potion Game", fontSize=winSize[1]*.075, center=True)
    l2.setBackgroundColor(0, 0, 0, 0)
    l2.setXY(winSize[0]*.5625, winSize[1]*1.425)
    obj.addItem(l2)

    la = label("Press ESC to start.", fontSize = winSize[1]*0.1, fontColor=(255, 255, 255, 255), center=True)
    la.setBackgroundColor(0, 0, 0, 100)
    la.setXY(winSize[0]*.5, winSize[1]*.4, True)
    #

    # main menu options
    submenu = menu((winSize[0]*.25, winSize[1]*.6), manager=layoutManager(horizontal=False, paddingY = winSize[1]*0.1))
    submenu.setXY(winSize[0]*.575, winSize[1]*1.55)
    submenu.setBackgroundColor(0, 0, 0, 0)
    obj.addItem(submenu)

    btn1 = btn("Start", (winSize[0]*.25, winSize[1]*.075), center=True, fontColor=(255, 255, 255, 255))
    btn1.setBackgroundColor(0, 0, 0, 150, outline=5, outlineColor=(255, 255, 255, 200))
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
    import animationHandler as ah
    ah.scoreboard.setXY(0, -winSize[1])
    ah.scoreboard.addAnim("open", animation(1, dxdy=(0, 0)))
    ah.scoreboard.addAnim("close", animation(1, dxdy=(0, -winSize[0])))
    ah.scoreboard.playAnim("open")
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


    # creates the menu that shows the customers to give a recently brewed potion to.
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
    cust.getDailyCustomers()
    try:
        for a in range(0, len(cust.customers)):
            custRow = menu((winSize[0]*.5-outline*1.25, winSize[1]*.1))
            custRow.setBackgroundColor(0, 0, 0, 150, outline=outline/2, outlineColor=(255, 255, 255, 200))
            custIcon = drawObject((winSize[1]*.09, winSize[1]*.09))
            custIcon.setBackgroundColor(100, 0, 0, 255)
            customers.addItem(custRow)
            custRow.addItem(custIcon)
            custIcon.setXY(custRow.x+winSize[1]*.005, custRow.y+winSize[1]*.005)

            custWant = label(cust.customers[a].wants(), fontSize=winSize[0]*0.015, size=(winSize[0]*.35, winSize[1]*.09), fontColor=(255, 255, 255, 255), lockSize=True)
            custWant.setBackgroundColor(0, 0, 0, 150)
            custRow.addItem(custWant)
            custWant.setXY(custRow.x+custIcon.width+outline/2, custRow.y+winSize[1]*0.005)

            give = btn("Give Potion", size=(winSize[0]*.075, winSize[1]*.05), fontSize=winSize[0]*0.01, fontColor=(255, 255, 255, 255), center=True)
            give.setXY(custRow.x+custRow.width-give.width-outline*.8, custRow.y+winSize[1]*0.025)
            give.setBackgroundColor(0, 0, 0, 150, outline=outline/2, outlineColor=(255, 255, 255, 200))
            
            give.bindFunction(cust.customers[a].evaluateGivenPotion, None)
            give.bindFunction(customerMenu.playAnim, "close")
            give.bindFunction(customers.removeItem, custRow)
            custRow.addItem(give)  
        #
    except Exception as e:
        print(e)

    # button to brew a potion.
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
    btn4.bindFunction(transitionScene, (.5, 1, ag.animations.MAIN, checkStateScreen))
    btn4.bindFunction(ah.scoreboard.playAnim, "close")
    btn4.setXY(winSize[0]-btn4.obj.get_width(), -winSize[1])
    btn4.addAnim("open", animation(1, dxdy=(winSize[0]-btn4.obj.get_width(), 0), interpol=eioCubic))
    btn4.playAnim("open")
    #


    root.addItem(obj)
    obj.addItem(btn1)
    obj.addItem(btn2)
    # obj.addItem(btn3)
    # root.addItem(addIng)
    root.addItem(btn4)
    root.addItem(customerMenu)


    scene["root"] = root

def checkStateScreen(scene):
    try:
        root = menu((0, 0))
        obj = menu((winSize[0]*.8, winSize[1]*.8), path="potion_game\\assets\\paper.png", manager=layoutManager(horizontal=False, outerPaddingX=winSize[0]*0.01, outerPaddingY=winSize[0]*0.01, paddingY=winSize[0]*.05))
        obj.setXY(winSize[0]*.1, winSize[1]*.1)

        import driver as dr
        dr.currentTime += 1
        checkBankrupt = False
        endOfWeek = False
        if dr.timeInterval == dr.currentTime:
            checkBankrupt = True
            endOfWeek = True
            dr.money -= dr.rentAmt
        if dr.money < 0 and checkBankrupt:
            # gameover
            gameover = label("GAME OVER", size=(winSize[0]*.8, winSize[1]*.2), fontSize=winSize[1]*0.1, fontColor=(255, 0, 0, 255), center=True)
            gameover.setXY(winSize[0]*.9-gameover.width, winSize[1]*.45-gameover.height/2)
            gameover.setBackgroundColor(0, 0, 0, 0)
            explain = btn("Restart?", size=(winSize[0]*.8, winSize[1]*.2), fontSize=winSize[1]*0.1, fontColor=(255, 255, 255, 255), center=True)
            explain.setXY(winSize[0]*.9-explain.width, winSize[1]*.9-explain.height)
            explain.setBackgroundColor(0, 0, 0, 150)

            def reset (*args):
                dr.currentTime = 0
                dr.money = 0
                dr.user.inv.storage.clear()
                dr.score = 0
                dr.rentAmt = 20
                import ingredient as ing
                from ingredient import IngredientType
                dr.user.inv.addItem(ing.Ingredient(IngredientType.ROOT))
                transitionScene((.5, 1, ag.animations.MAIN, mainMenu))
            explain.bindFunction(reset, None)


            root.addItem(obj)
            root.addItem(gameover)
            root.addItem(explain)
        else:
            checkBankrupt = False
            if endOfWeek:
                rent = label("Rent was paid: " + str(dr.rentAmt) + "g", size=(winSize[0]*.8, winSize[1]*.1), fontSize=winSize[1]*0.1)
                dr.rentAmt += 10
                nextRent = label("Next weeks rent will be: " + str(dr.rentAmt) + "g", size=(winSize[0]*.8, winSize[1]*.1), fontSize=winSize[1]*0.1)
                nextRent.setBackgroundColor(0, 0, 0, 0)
                obj.addItem(rent)     
                obj.addItem(nextRent)
                root.addItem(obj)
            else:
                rent = label("Rent in " + str(dr.timeInterval-dr.currentTime) + " days", size=(winSize[0]*.8, winSize[1]*.1), fontSize=winSize[1]*0.1)
                obj.addItem(rent)     
            rent.setBackgroundColor(0, 0, 0, 0)
            info = btn("Continue", size=(winSize[0]*.3, winSize[1]*.1), fontSize=winSize[1]*0.1, center=True, fontColor=(255, 255, 255, 255))
            info.setXY(winSize[0]*.9-info.width, winSize[1]*.9-info.height)
            info.setBackgroundColor(0, 0, 0, 100, outline=5, outlineColor=(255, 255, 255, 255))
            info.bindFunction(transitionScene, (.5, 1, ag.animations.MAIN, stockScreen))
            root.addItem(obj)
            root.addItem(info)
        scene["root"] = root
    except Exception as e:
        print(e)
    
    

def stockScreen(scene):
    obj = menu((winSize[0]*.8, winSize[1]*.8), path="potion_game\\assets\\paper.png", manager=layoutManager(horizontal=False, outerPaddingX=winSize[0]*0.01, outerPaddingY=winSize[0]*0.01))
    obj.setBackgroundColor(0, 0, 0, 50, outline=5, outlineColor=(255, 255, 255, 200))
    obj.setXY(winSize[0]*.1, winSize[1])
    obj.addAnim("open", animation(1, dxdy=(winSize[0]*.1, winSize[1]*.1), interpol=eioCubic))
    obj.playAnim("open")

    import driver as dr
    moneyLabel = label("Money: "+str(dr.money), size=(winSize[0]*.3, winSize[0]*.05), fontSize=winSize[0]*0.04, fontColor=(255, 255, 10, 255), center=True)
    moneyLabel.setBackgroundColor(0, 0, 0, 0)
    header = menu((winSize[0]*.78, moneyLabel.height))
    header.addItem(moneyLabel)
    header.setBackgroundColor(0, 0, 0, 50)

    
    import ingredient as ing
    shopBase = menu((winSize[0]*.7, winSize[1]*.6), manager=layoutManager(horizontal=False))
    shopBase.setXY(winSize[0]*.1, winSize[1])
    shopBase.setBackgroundColor(0, 0, 0, 0)

    index = 0
    row = menu((winSize[0]*.7, winSize[1]*.2), manager=layoutManager(horizontal=True))
    row.setBackgroundColor(0, 0, 0, 0)
    shopBase.addItem(row)
    dir = "potion_game\\assets\\ingredients\\"
    
    for ingredient in ing.IngredientType:
        if index == 4:
            row = menu((winSize[0]*.7, winSize[1]*.2), manager=layoutManager(horizontal=True))
            row.setBackgroundColor(0, 0, 0, 0)
            shopBase.addItem(row)
            index = 0
        ingredientShopItem = menu((winSize[1]*.2, winSize[1]*.2))
        ingredientShopItem.setBackgroundColor(0, 0, 0, 100)
        row.addItem(ingredientShopItem)

        
        ingredientPortrait = drawObject((winSize[1]*.15, winSize[1]*.15), path=dir+ingredient.value["icon"])
        ingredientPortrait.setXY(ingredientShopItem.x+(ingredientShopItem.width-ingredientPortrait.width)/2, ingredientShopItem.y)

        buy = btn("Buy for " + str(ingredient.value["price"])+ "g", (winSize[1]*.2, winSize[1]*.05), fontSize=winSize[1]*0.025, center=True, fontColor=(255, 255, 255, 255))
        buy.setBackgroundColor(0, 0, 0, 100, outline=5, outlineColor=(0, 0, 0, 255))
        buy.setXY(ingredientShopItem.x, ingredientShopItem.y+winSize[1]*.15)


        def buyFunction (ingredient):
            dr.money -= ingredient.value["price"]
            moneyLabel.setText("Money: "+str(dr.money), center=True)
            dr.user.addToInventory(ing.Ingredient(ingredient))

        buy.bindFunction(buyFunction, (ingredient))

        ingredientShopItem.addItem(ingredientPortrait)
        ingredientShopItem.addItem(buy)
        index += 1


    #
    btn4 = btn("Next Day", size=(winSize[0]*.3, winSize[0]*.05), fontSize=winSize[0]*0.04, fontColor=(255, 255, 255, 255), center=True)
    btn4.setBackgroundColor(0, 0, 0, 150, outline=5, outlineColor=(255, 255, 255, 200))
    btn4.bindFunction(transitionScene, (.5, 1, ag.animations.IDLE, mixScreen))
    btn4.setXY(winSize[0]*.78-btn4.width, 0)
    header.addItem(btn4)
    #


    obj.addItem(header)
    obj.addItem(shopBase)
    

    scene["root"] = obj