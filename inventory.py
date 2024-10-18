from items import *
from typing import List
from flags import vprint

class Inventory:
    storage: List[Item] = []
    storageSize = 0;

    # when deleting, delete any references this class might hold.
    def __del__ (self):
        self.storage.clear()

    # sets the initial storage size of this inventory object
    def __init__ (self, size: int):
        self.storageSize = size

    #     
    def addItem (self, item: Item) -> bool:
        # check if given index is within the bounds of this storage object
        if self.storageSize > len(self.storage):
            self.storage.append(item)
            vprint("Item added")
            return True
        
        vprint("Inventory full!")        
        return False
    
    # uses the item in the inventory
    def useItem (self, slot: int):
        # check if the index is in range
        if len(self.storage) >= slot:
            
            # use the item, then check if we can still use it, if not then we delete the consumable.
            returnVal = self.storage[slot].use();
            if not self.storage[slot].canUse():
                vprint("Used up " + self.storage[slot].name)
                del self.storage[slot]
            return returnVal
        else:
            vprint("invalid index")
            return -1