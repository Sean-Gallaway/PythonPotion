from enum import Enum
import random
from typing import List
from effects import *
from items import PotionBuilder

class IngredientType(Enum):
    ROOT                = {"name": "big root", "effects": [ [EffectType.DAMAGE, 10, 4, 1] ]}
    FROST_POWDER        = {"name": "frost powder", "effects": [ [EffectType.DAMAGE, 1, 1, 1] ]}
    MINT                = {"name": "mint", "effects": [ [EffectType.CONDITIONAL, [EffectType.HEALING, 100, 1, 1], "user.hp < 0" ] ]}

class Ingredient():
    info = []

    def __init__ (self, type: IngredientType):
        self.info = type.value.get("effects")
        for i in self.info[1::]:
            i *= random.uniform(.6, 1.4)

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


def generatePotion (*ingredientsUsed: Ingredient):
    list = []
    for ing in ingredientsUsed:
        for effect in ing.info:
            list.append(generateEffect(effect[0], effect[1::]))
            
    return PotionBuilder.addEffect(list).setUses(1).setName("Weird Potion").createPotion()