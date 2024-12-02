import copy
from typing import List
from effects import *

class Item:
    name = ""
    
    # constructor
    def __init__ (self, name: str):
        self.name = name 

# a consumable Item that keeps tracks of the amount of times its been used.
class Consumable(Item):
    uses = 0
    effect = []

    # constructor
    def __init__ (self, name: str, uses: int, effect: list[Effect]):
        Item.name = name
        self.uses = uses
        self.effect = effect

    # destructor
    def __del__ (self):
        self.effect.clear()
        del self.effect

    # get the effects
    def getEffects (self) -> list:
        return self.effect
    
    # check if we can use the consumable
    def canUse (self) -> bool:
        if (self.uses > 0):
            return True; 
        return False

    # when the consumable is used, uses should decrement. returns a list of effects
    def use (self) -> list:
        list = []
        if (self.canUse()):
            self.uses -= 1 
            # a consumable applies an effect, once applied the effect is individual from the potion, so it should be a deepcopy.
            for eff in self.effect:
                list.append(copy.deepcopy(eff))
        elif (self.uses == 0):
            del self
        return list
    
    def __str__(self):
        eff = ""
        for effect in self.effect:
            eff += str(effect)
        return self.name + " " + eff + " uses: " + str(self.uses)

# builder pattern to create potions via method chaining.
class PotionBuilder:
    effectList = []
    uses = 1000
    name = ""

    # creates the potion and empties this objects effectlist.
    @staticmethod
    def createPotion ():
        # this copying is important, because python reference system is annoying. >:(
        tempList = PotionBuilder.effectList.copy()
        PotionBuilder.effectList.clear()
        c = Consumable(PotionBuilder.name, PotionBuilder.uses, tempList)
        PotionBuilder.name = ""
        PotionBuilder.uses = 1000
        return c
    
    # adds an effect to the potion effect list.
    @staticmethod
    def addEffect (effect: Effect):
        PotionBuilder.effectList.append(effect)
        return PotionBuilder
    
    # adds an effect to the potion effect list.
    @staticmethod
    def addEffect (effect: List[Effect]):
        PotionBuilder.effectList.extend(effect)
        return PotionBuilder
    
    # sets the number of uses a potion has.
    @staticmethod
    def setUses (uses: int):
        PotionBuilder.uses = uses
        return PotionBuilder
    
    # sets the name of the potion.
    @staticmethod
    def setName (name: str):
        PotionBuilder.name = name
        return PotionBuilder

