from enum import Enum
import random
from effects import *
from items import PotionBuilder

class IngredientType(Enum):
    ROOT                = {"name": "Big Root", "effects": [ [EffectType.DAMAGE, 10, 4, 1] ], "icon": "big_root.png", "desc": "A big root from an unnamed plant, eating it might be unwise.", "chop": True}

    FROST_POWDER        = {"name": "Frost Powder", "effects": [ [EffectType.DAMAGE, 1, 1, 1] ], "icon": "frost_powder.png", "desc": "Powder obtained through crushing ice that never melts, cold to the touch.", "chop": False}
    
    MINT                = {"name": "Mint", "effects": [ [EffectType.CONDITIONAL, [EffectType.HEALING, 100, 1, 1], "user.hp < 0" ] ], "icon": "mint.png", "desc": "Garden variety mint, soothing.", "chop": True}


currPotionList = []



# the Ingredient class stores info based on an ingredient, with some variance because some ingredients can be better than others,
# regardless of if they are the same type or not.
class Ingredient():
    info = []

    def __init__ (self, type: IngredientType):
        self.info = []
        for a in type.value.get("effects"):
            e = []
            e.append(a[0])
            for b in a[1:-1:]:
                e.append(round(b * random.uniform(.6, 1.4), 2))
            e.append(a[-1])
            self.info.append(e)


# generate an effect based on a given EffectType.
def generateEffect (type: EffectType, params: list) -> Effect:
    match type:
        case EffectType.DAMAGE:
            # TODO check list size
            return DamageEffect("damage", params[0], params[1], params[2])
        case EffectType.HEALING:
            return HealingEffect("healing", params[0], params[1], params[2])
        case EffectType.CONDITIONAL:
            test = generateEffect(params[0][0], params[0][1::])
            return ConditionalEffect("con", test, str(params[1]) )


def generatePotion ():
    list = []
    for ing in currPotionList:
        for effect in ing.info:
            list.append(generateEffect(effect[0], effect[1::]))
            
    return PotionBuilder.addEffect(list).setUses(1).setName("Weird Potion").createPotion()


def addIngredient(type: Ingredient):
    currPotionList.append(type)