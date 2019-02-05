from Items.Armour import Chainmail, Breastplate
from Items.Weapons import Sword
from Materials import Low_Carbon, High_Carbon
from Creatures import *

m = Low_Carbon()

h = Human(2, 20, {'strength': 50}, {'strength': 900})

s = Sword(h, High_Carbon())
a = Chainmail(High_Carbon())
h.right_palm.equip(s, held=True)

h.right_palm.jab(a, 2)
