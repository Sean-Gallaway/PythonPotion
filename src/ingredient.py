from enum import Enum
import random
from effects import *
from items import *

# price(int), name(str), effects(list), icon(str), desc(str), chop(bool), chopTo(IngredientType), 
class IngredientType(Enum):
    CHOPPED_ROOT        = {"price": 12, "name": "Chopped Big Root", "effects": [ [EffectType.DAMAGE, 20.0, 4.0, 1.0] ], "icon": "big_root_powder.png", "desc": "A chopped up big root, eating it is definitely unwise.", "chop": False}
    ROOT                = {"price": 10, "name": "Big Root", "effects": [ [EffectType.DAMAGE, 10.0, 4.0, 1.0] ], "icon": "big_root.png", "desc": "A big root from an unnamed plant, eating it might be unwise.", "chop": True, "chopTo": CHOPPED_ROOT}
    FROST_POWDER        = {"price": 20, "name": "Frost Powder", "effects": [ [EffectType.DAMAGE, 1.0, 1.0, 1.0] ], "icon": "frost_powder.png", "desc": "Powder obtained through crushing ice that never melts, cold to the touch.", "chop": False}
    MINT_POWDER         = {"price": 17, "name": "Mint Powder", "effects": [ [EffectType.HEALING, 200.0, 1.0, 1.0] ], "icon": "mint_powder.png", "desc": "Garden variety mint chopped up finely, immensely soothing.", "chop": False}
    MINT                = {"price": 15, "name": "Mint", "effects": [ [EffectType.HEALING, 100.0, 1.0, 1.0] ], "icon": "mint.png", "desc": "Garden variety mint, soothing.", "chop": True, "chopTo": MINT_POWDER}
    # NIRNROOT
    # FLAX
    # WILLOW_WISP
    # ECTOPLASM
    # FIRE_SALTS
    # FROST_SALTS
    HONEY               = {"price": 20, "name": "Honey", "effects": [[EffectType.HEALING, 100, 1, 1],[EffectType.MAXHEALTH, 100, 1, 1]], "icon": "honey.png", "desc": "Localy sourced honey", "chop": False}


currPotionList = []


# the Ingredient class stores info based on an ingredient, with some variance because some ingredients can be better than others,
# regardless of if they are the same type or not.
class Ingredient(Item):
    def __init__ (self, itype: IngredientType):
        itype = IngredientType(itype)
        self.name = itype.value["name"]
        self.info = []
        self.itype = itype
        for a in itype.value.get("effects"):
            if a[0] == EffectType.CONDITIONAL:
                continue
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
            return DamageEffect(EffectType.DAMAGE.name, params[0], params[1], params[2])
        case EffectType.HEALING:
            return HealingEffect(EffectType.HEALING.name, params[0], params[1], params[2])
        case EffectType.CONDITIONAL:
            test = generateEffect(params[0][0], params[0][1::])
            return ConditionalEffect(EffectType.CONDITIONAL.name, test, str(params[1]) )
        case EffectType.MAXHEALTH:
            return HealthEffect(EffectType.MAXHEALTH, params[0], params[1], params[2])


def generatePotion ():
    list = []
    for ing in currPotionList:
        for effect in ing.value["effects"]:
            list.append(generateEffect(effect[0], effect[1::]))
    p = PotionBuilder.addEffect(list).setUses(1).setName("Weird Potion").createPotion()
    currPotionList.clear()
    return p


def addIngredient(itype: Ingredient):
    currPotionList.append(itype)