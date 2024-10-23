from inventory import *

class User():
    persistent: list[Effect]
    inv = None
    hp = 20
    
    # initialize the inventory to a preset amount and set the persistent list to empty.
    def __init__(self):
        self.inv = Inventory(10)   
        self.persistent = []     
    
    # when we are done with this User object, we should get rid of any references it might hold.
    def __del__(self):
        del self.inv
        self.persistent.clear()
        del self.persistent

    # if there are any effects in the persistent buffer, we should probably do something about that.
    def advanceEffects(self):
        # if running verbose mode
        vprint("Advancing effects, count =" + str(len(self.persistent)) )
        #

        # for each effect in the persistent buffer, we use the effect if its not expired.
        for effect in self.persistent:
            if not effect.expired():
                effect.useEffect(self)
                if effect.expired():
                    vprint("\tremoved effect")
                    self.persistent.remove(effect)
                

    # uses an item and applies its effects into persistent.
    def useItem(self, slot: int):
        val = self.inv.useItem(slot)
        self.persistent.extend(val)

    def getItem(self, slot: int):
        return self.inv.getItem(slot)
    
    # adds a given item to the inventory
    def addToInventory(self, item: Item):
        self.inv.addItem(item)