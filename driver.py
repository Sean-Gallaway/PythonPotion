from effects import *
from items import *
from user import *
from inventory import *
from tkinter import *
from ingredient import *

user = User()

def test():
    print("")
    
user.addToInventory(generatePotion(Ingredient(IngredientType.FROST_POWDER), Ingredient(IngredientType.FROST_POWDER) ))


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