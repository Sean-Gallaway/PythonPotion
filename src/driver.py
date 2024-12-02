from user import *
from ingredient import *
from customer import *
from animationHandler import *

score = 0
money = 0
timeInterval = 7
currentTime = 0
rentAmt = 20
user = User()
user.addToInventory(Ingredient(IngredientType.ROOT))
