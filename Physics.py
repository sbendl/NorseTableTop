"""
All measurements in mm / MPa / Joules / Kilograms
"""
import math
from scipy import integrate

import numpy as np


def logistic(x, L, k, x0, y0):
    return L / (1 + math.e ** (-k*(x-x0))) + y0 - L / 2

def logit(x, L, k, x0, y0):
    try:
        return -L*math.log((1 / (k * (x-x0+1/(2*k)))) - 1) + y0
    except Exception as e:
        pass
        # print(x, (1 / (k * (x-x0+.5-k))) - 1,  e)

def logitprime(x, L, k, x0, y0):
    return -(4*k*L)/(-1 + 4*k**2*(x - x0)**2)


def compose(slope, tan_x, asymptote):
    func1 = lambda x: x * slope
    tan_y = tan_x * slope
    k = 1 / (2 * (asymptote - tan_x))
    L = slope / (4 * k)
    func2 = lambda x: logit(x, L, k, tan_x, tan_y)
    print(logitprime(tan_x, L, k, tan_x, tan_y))
    print(k, L, tan_x, tan_y)
    elastic_energy = func1(tan_x) * tan_x / 2
    print(elastic_energy, integrate.quad(func1, 0, tan_x))
    break_energy = integrate.quad(func2, tan_x, asymptote)[0] + elastic_energy

    return lambda x: func1(x) if x < tan_x else func2(x), elastic_energy, break_energy

class Sword_Low_Carbon:
    tensile_ult = 766
    tensile_yield = 572

class Sword_Med_Carbon:
    tensile_ult = 987
    tensile_yield = 685

class Sword_High_Carbon:
    tensile_ult = 1010
    tensile_yield = 810

class Sword:
    thickness = 2.6
    width = 48.5
    length = 886
    tensile_ult = 130 * 1000000
    tensile_yield = 11 00 * 1000000
    shear_yield = tensile_yield * .566
    shear_ult = tensile_ult * .566
    mod_of_elasticity = 202000 * 1000000
    shear_modulus = 80000 * 1000000
    mass = 1.182
    strain_at_fracture = .2

    def __init__(self):
        self.tensile_stress_strain, self.tensile_elastic_limit, self.tensile_plastic_limit = self.calc_stress_strain(self.mod_of_elasticity, self.tensile_yield, self.tensile_ult, self.strain_at_fracture)
        self.shear_stress_strain, self.shear_elastic_limit, self.shear_plastic_limit = self.calc_stress_strain(self.shear_modulus, self.shear_yield, self.shear_ult, self.strain_at_fracture)

    def calc_stress_strain(self, slope, tan_y, asymptote, break_point):
        func1 = lambda x: x * slope
        tan_x = tan_y / slope
        L = (asymptote - tan_y) * 2
        k = (slope * 4) / L
        func2 = lambda x: logistic(x, L, k, tan_x, tan_y)
        elastic_energy = func1(tan_x) * tan_x / 2
        break_energy = integrate.quad(func2, tan_x, break_point)[0] + elastic_energy

        def comp(x):
            if x < tan_x:
                return func1(x)
            elif tan_x < x < break_point:
                return func2(x)
            else:
                return 0

        return comp, elastic_energy, break_energy

    def calc_damage(self, KE, volume):
        print("weapon:")
        pl = self.shear_plastic_limit * volume
        el = self.shear_elastic_limit * volume

        print(KE, el, pl)

        if KE > pl:
            print('Pierced')
        elif KE > el:
            print('Bent')
            for s in np.linspace(0, self.strain_at_fracture, 100, endpoint=False):
                if integrate.quad(self.shear_stress_strain, 0, s)[0] * volume > KE:
                    print(s)
                    break
        else:
            print('Deflected')

    def slash(self, other, velocity):
        KE = .5 * self.mass * velocity ** 2
        volume = 2 * (self.thickness * min(self.length, other.width) * other.thickness) / 1000 ** 3
        # volume = (self.thickness * self.length * other.thickness) / 1000 ** 3
        cut_length = min(self.length, other.width, other.length)
        volume_other = (cut_length * other.thickness * self.thickness) / 1000**3
        volume_self = (self.thickness * self.width * self.length) / 1000**3


        self.calc_damage(KE, volume_self)
        other.calc_damage(KE, volume_other)

    def stab(self, other, velocity):
        KE = .5 * self.mass * velocity ** 2
        volume = 2 * (self.thickness * min(self.width, other.width) * other.thickness) / 1000 ** 3
        # volume = (self.thickness * self.length * other.thickness) / 1000 ** 3
        area = min(self.width, other.width, other.length) * self.thickness

        self.calc_damage(KE, 8 * (area * self.length) / 1000 ** 3)
        other.calc_damage(KE, 8 * (area * other.thickness) / 1000 ** 3)



class Breastplate:
    thickness = 3
    width = 500
    length = 700
    tensile_ult = 766 * 1000000
    tensile_yield = 572 * 1000000
    shear_yield = tensile_yield / 2
    shear_ult = tensile_ult / 2
    mod_of_elasticity = 1202000 * 1000000
    shear_modulus = 79500 * 1000000
    strain_at_fracture = .2

    def __init__(self):
        self.tensile_stress_strain, self.tensile_elastic_limit, self.tensile_plastic_limit = self.calc_stress_strain(
            self.mod_of_elasticity, self.tensile_yield, self.tensile_ult, self.strain_at_fracture)
        self.shear_stress_strain, self.shear_elastic_limit, self.shear_plastic_limit = self.calc_stress_strain(
            self.shear_modulus, self.shear_yield, self.shear_ult, self.strain_at_fracture)

    def calc_stress_strain(self, slope, tan_y, asymptote, break_point):
        func1 = lambda x: x * slope
        tan_x = tan_y / slope
        L = (asymptote - tan_y) * 2
        k = (slope * 4) / L
        func2 = lambda x: logistic(x, L, k, tan_x, tan_y)
        elastic_energy = func1(tan_x) * tan_x / 2
        break_energy = integrate.quad(func2, tan_x, break_point)[0] + elastic_energy

        def comp(x):
            if x < tan_x:
                return func1(x)
            elif tan_x < x < break_point:
                return func2(x)
            else:
                return 0

        return comp, elastic_energy, break_energy

    def calc_damage(self, KE, volume):
        print("armour:")
        pl = self.shear_plastic_limit * volume
        el = self.shear_elastic_limit * volume

        print(KE, el, pl)

        if KE > pl:
            print('Pierced')
        elif KE > el:
            print('Bent')
            for s in np.linspace(0, self.strain_at_fracture, 100, endpoint=False):
                if integrate.quad(self.shear_stress_strain, 0, s)[0] * volume > KE:
                    print(s)
                    break
        else:
            print('Deflected')

s = Sword()
bp = Breastplate()

s.slash(bp, 20)


# First compare yield strength to elastic limit and then to plastic limit of weapon to armor if it is lower then it can
# never cause damage.
#
# Then calculate damage to weapon then damage to armor
#

