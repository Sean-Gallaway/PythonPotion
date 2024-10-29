from effects import EffectType
import random

class customer():
    effectsWanted = []

    def __init__ (self):
        for e in range(random.randint(1, len(EffectType))):
            self.effectsWanted.append( random.choice(list(EffectType)) )

    def wants (self):
        print(self.effectsWanted)

# on day start, get the daily customer orders
def getDailyCustomers ():
    customersList = []
    for c in range(random.randint(1, 4)):
        customersList.append(customer())
    return customersList
