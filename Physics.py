
# K / 4 = tangent at 0
# L / 4 = tangent at 0

# (K * L) / 4 = tangent at 0
import math


def logistic(x, L, k, x0, y0):
    return L / (1 + math.e ** (-k*(x-x0))) + y0 - L / 2

def compose(slope, tan_x, asymptote):
    func1 = lambda x: x * slope
    tan_y = tan_x * slope
    L = asymptote - tan_y
    k = (slope * 4) / L
    func2 = lambda x: logistic(x, L, k, tan_x, tan_y)
    return lambda x: func1(x) if x < tan_x else func2(x)

class Sword_Low_Carbon:
    tensile_ult = 766
    tensile_yield = 572

class Sword_Med_Carbon:
    tensile_ult = 987
    tensile_yield = 685

class Sword_High_Carbon:
    tensile_ult = 1010
    tensile_yield = 810