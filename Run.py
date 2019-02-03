from Items.Armour import Chainmail
from Items.Weapons import Sword
from Materials import Low_Carbon
from Creatures import *

m = Low_Carbon()

h = Human(2, 20, {}, {})
s = Sword(h, Low_Carbon())
a = Chainmail(Low_Carbon())

s.slash(a, 10)
