from items import *
from typing import List
import flags

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
        if self.storageSize > len(self.storage):
            self.storage.append(item)
            # if running verbose mode
            if flags.verbose:
                print("Item added")
            #
            return True
        
        # if running verbose mode
        if flags.verbose:
            print("Inventory full!")
        #
        
        return False
    
    # uses the item in the inventory
    def useItem (self, slot: int):
        # check if the index is in range
        if len(self.storage) >= slot:
            
            # use the item, then check if we can still use it, if not then we delete the consumable.
            returnVal = self.storage[slot].use();
            if not self.storage[slot].canUse():
                
                # if running verbose mode
                if flags.verbose:
                    print("Used up " + self.storage[slot].name)
                #
                
                del self.storage[slot]
            return returnVal
        else:
            # if running verbose mode
            if flags.verbose:
                print("invalid index")
            #
            return -1