from effects import *
from items import *
from user import *
from inventory import *
from tkinter import *

user = User()

def test():
    print("")
    

# user.addToInventory(PotionBuilder
#             .addEffect(DamageEffect("Poison", 10, 3, 1))
#             .setUses(2)
#             .setName("Poison Potion")
#             .createPotion())

user.addToInventory(PotionBuilder
                    .addEffect(ConditionalEffect("Con", DamageEffect("dmg", 10, 1, 1), "2 == 2"))
                    .setUses(1)
                    .setName("Weird Potion")
                    .createPotion() )



user.useItem(0)
print("user hp:", user.hp)
user.advanceEffects()

# user.useItem(0)
print("user hp:", user.hp)
user.advanceEffects()

print("user hp:", user.hp)
print("deleting user")
del user

# window = Tk()
# window.title("Potion Game")
# window.configure(background="gray")
# window.minsize(300, 200)

# test = Button(window, text="drink", command=test)
# test.pack()

# window.mainloop();

print("end")