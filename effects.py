import flags
class Effect:
    effectName = ""
    duration = 0
    def useEffect (self, name: str, duration = 100):
        raise NotImplementedError()
    
    def __del__ (self):
        # if running verbose mode
        if flags.verbose:
            print("Deleted " + self.name)

    # check if this Effect has expired or not
    def expired (self) -> bool:
        return self.duration <= 0

class DamageEffect(Effect):
    amount = 0
    times = 0

    # constructor
    def __init__ (self, name: str, amount: int, times: int, duration: int):
        Effect.name = name
        self.amount = amount
        self.times = times
        self.duration = duration

    # 
    def useEffect (self) -> int:
        self.duration -= 1
        return -(self.amount * self.times)

class HealingEffect(DamageEffect):
    # override damage effect, just turn it negative
    def useEffect (self) -> int:
        self.duration -= 1
        return self.amount * self.times