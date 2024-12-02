from effects import EffectType
import random

customers = []

wantDict = {EffectType.DAMAGE:"that will hurt their enemies", EffectType.HEALING: "that will cure their ills", EffectType.CONDITIONAL: "that has a dual nature"}

class customer():
    def __init__ (self):
        self.effectsWanted = []
        self.wantedString = "A potion "
        for e in range(random.randint(1, 3)):
            want = random.choice(list(EffectType))
            self.effectsWanted.append(want.name)
            if e != 0:
                self.wantedString += " and "
            self.wantedString += wantDict[want]

    def wants (self):
        return self.wantedString
    
    def evaluateGivenPotion (self):
        import ingredient as ing
        potion = ing.generatePotion()

        hits = 0
        for e in potion.effect:
            if e.effectName in self.effectsWanted:
                hits += 1

        import driver as dr
        dr.score += hits
        print(dr.score)



# on day start, get the daily customer orders
def getDailyCustomers ():
    customers.clear()
    for c in range(random.randint(1, 4)):
        customers.append(customer())
