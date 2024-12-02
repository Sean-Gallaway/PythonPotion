from __future__ import annotations
from flags import vprint
from enum import Enum

class EffectType(Enum):
    CONDITIONAL = 0
    HEALING = 1
    DAMAGE = 2


class Effect:
    def __init__(self):
        self.effectName = ""
        self.duration = 0

    def useEffect (self, name: str, duration = 100):
        raise NotImplementedError()
    
    def __del__ (self):
        vprint("Deleted " + self.effectName)

    # check if this Effect has expired or not
    def expired (self) -> bool:
        return self.duration <= 0

class DamageEffect(Effect):
    # constructor
    def __init__ (self, name: str, amount: int, times: int, duration: int):
        super().__init__()
        self.effectName = name
        self.amount = amount
        self.times = times
        self.duration = duration

    # 
    def useEffect (self, user: User): # type: ignore
        self.duration -= 1
        user.hp -= (self.amount * self.times)

    def __str__ (self):
        return self.name + " amount: " + str(self.amount) + " times: " + str(self.times) 

class HealingEffect(DamageEffect):
    # override damage effect, just turn it negative
    def useEffect (self, user: User) -> int: # type: ignore
        self.duration -= 1
        user.hp += (self.amount * self.times)
    
class ConditionalEffect(Effect):
    #
    def __init__ (self, name: str, eff: Effect, con: str):
        self.triggeredEffect = eff
        self.condition = con
        Effect.name = name
    
    #
    def useEffect (self, user: User): # type: ignore
        if self.condition != "":
            if eval(self.condition):
                print("passed condition")
                return self.triggeredEffect.useEffect(user)
            else:
                print("did not pass condition")

    #
    def expired (self) -> bool:
        return self.triggeredEffect.duration <= 0
