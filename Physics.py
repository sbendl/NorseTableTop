"""
All measurements in mm / MPa / Joules / Kilograms
"""
import math
from scipy import integrate

import numpy as np


def logistic(x, L, k, x0, y0):
    return L / (1 + math.e ** (-k * (x - x0))) + y0 - L / 2


def logit(x, L, k, x0, y0):
    try:
        return -L * math.log((1 / (k * (x - x0 + 1 / (2 * k)))) - 1) + y0
    except Exception as e:
        pass
        # print(x, (1 / (k * (x-x0+.5-k))) - 1,  e)


def logitprime(x, L, k, x0, y0):
    return -(4 * k * L) / (-1 + 4 * k ** 2 * (x - x0) ** 2)


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


class Material:
    tensile_ult = None
    tensile_yield = None
    shear_yield = None
    shear_ult = None
    mod_of_elasticity = None
    shear_modulus = None
    strain_at_fracture = None

    def __init__(self):
        self.tensile_stress_strain, self.tensile_elastic_limit, self.tensile_plastic_limit = self.calc_stress_strain(
            self.mod_of_elasticity, self.tensile_yield, self.tensile_ult,
            self.strain_at_fracture)
        self.shear_stress_strain, self.shear_elastic_limit, self.shear_plastic_limit = self.calc_stress_strain(
            self.shear_modulus, self.shear_yield, self.shear_ult,
            self.strain_at_fracture)

    @staticmethod
    def calc_stress_strain(slope, tan_y, asymptote, break_point):
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


class Low_Carbon(Material):
    tensile_ult = 766 * 1e6
    tensile_yield = 572 * 1e6
    shear_yield = tensile_yield * .566
    shear_ult = tensile_ult * .566
    mod_of_elasticity = 202 * 1000 * 1e6
    shear_modulus = 79.5 * 1000 * 1e6
    strain_at_fracture = .202

    def __init__(self):
        super().__init__()


class Med_Carbon(Material):
    tensile_ult = 987 * 1e6
    tensile_yield = 685 * 1e6
    shear_yield = tensile_yield * .566
    shear_ult = tensile_ult * .566
    mod_of_elasticity = 203 * 1000 * 1e6
    shear_modulus = 79.6 * 1000 * 1e6
    strain_at_fracture = .189

    def __init__(self):
        super().__init__()


class High_Carbon(Material):
    tensile_ult = 1010 * 1e6
    tensile_yield = 810 * 1e6
    shear_yield = tensile_yield * .566
    shear_ult = tensile_ult * .566
    mod_of_elasticity = 198 * 1000 * 1e6
    shear_modulus = 79.9 * 1000 * 1e6
    strain_at_fracture = .146

    def __init__(self):
        super().__init__()


class Sword:
    thickness = 2.6 / 1000
    width = 48.5 / 1000
    length = 886 / 1000
    mass = 1.182
    tip_angle = 45

    def __init__(self, wielder, material):
        self.wielder = wielder
        self.material = material

    def calc_damage(self, KE, other):
        print("weapon:")
        volume = self.width * self.thickness * self.length
        pl = self.material.shear_plastic_limit * volume
        el = self.material.shear_elastic_limit * volume

        print(KE, el, pl)

        if KE > pl:
            print('Broken')
        elif KE > el:
            print('Bent')
            for s in np.linspace(0, self.material.strain_at_fracture, 250, endpoint=False):
                if integrate.quad(self.material.shear_stress_strain, 0, s)[0] * volume > KE:
                    print(s)
                    break
        else:
            print('Deflected')

    def slash(self, other, ang_velocity):
        cut_length = min(self.length, other.width, other.length)
        tip_velocity = ang_velocity * (self.wielder.elbow_len + self.length)
        bottom_velocity = ang_velocity * (self.wielder.elbow_len + (self.length * 2 / 3) - cut_length)
        print(tip_velocity, bottom_velocity)
        KE_self = .5 * (self.mass / 2) * bottom_velocity ** 2
        KE_other = .5 * self.mass * tip_velocity ** 2
        self.calc_damage(KE_self, other)
        other.calc_cutting_damage(KE_other, self)

    def stab(self, other, velocity):
        KE = .5 * self.mass * velocity ** 2
        area = min(self.width, other.width, other.length) * self.thickness
        self.calc_damage(KE, 8 * (area * self.length))
        other.calc_piercing_damage(KE, self)


class Chainmail:
    link_thickness = 1.5 / 1000
    link_diameter = 4 / 1000
    thickness = link_thickness * 3
    width = 500 / 1000
    length = 700 / 1000

    def __init__(self, material):
        self.material = material

    def calc_cutting_damage(self, KE, other):
        cut_length = min(other.length, self.width, self.length)
        volume = (cut_length * self.thickness * self.link_diameter * 2)
        print("armour:")
        pl = self.material.shear_plastic_limit * volume
        el = self.material.shear_elastic_limit * volume

        print(KE, el, pl)

        if KE > pl:
            print('Pierced')
        elif KE > el:
            print('Bent')
            for s in np.linspace(0, self.material.strain_at_fracture, 100, endpoint=False):
                if integrate.quad(self.material.shear_stress_strain, 0, s)[0] * volume > KE:
                    print(s)
                    break
        else:
            print('Deflected')

    def calc_piercing_damage(self, KE, other):
        cut_length = min(other.width, self.width, self.length)
        area = 2 * math.pi * (self.link_thickness / 2)**2
        print("armour:")

        rip_size = self.link_diameter - self.link_thickness * 2

        while rip_size < cut_length and KE > 0:
            link_length = self.link_diameter * math.pi
            volume = area * rip_size
            pl = self.material.shear_plastic_limit * volume
            el = self.material.shear_elastic_limit * volume
            print(KE, el, pl)
            if KE > pl:
                print('Link Broken')
                KE -= pl
                rip_size += link_length
                if rip_size > cut_length:
                    print('Pierced', KE)
            elif KE > el:
                print('Bent')
                for s in np.linspace(0, self.material.strain_at_fracture, 100, endpoint=False):
                    e = integrate.quad(self.material.shear_stress_strain, 0, s)[0] * volume
                    if rip_size * s >= cut_length:
                        KE -= pl
                        print("Pierced", KE)
                        break
                    if e > KE:
                        print(s*link_length)
                        KE = 0
                        break
            else:
                print('Deflected')


class Breastplate:
    thickness = 3 / 1000
    width = 500 / 1000
    length = 700 / 1000

    def __init__(self, material):
        self.material = material

    def calc_damage(self, KE, volume):
        print("armour:")
        pl = self.material.shear_plastic_limit * volume
        el = self.material.shear_elastic_limit * volume

        print(KE, el, pl)

        if KE > pl:
            print('Pierced')
        elif KE > el:
            print('Bent')
            for s in np.linspace(0, self.material.strain_at_fracture, 100, endpoint=False):
                if integrate.quad(self.material.shear_stress_strain, 0, s)[0] * volume > KE:
                    print(s)
                    break
        else:
            print('Deflected')

    def calc_piercing_damage(self, KE, other):
        cut_length = min(other.width, other.thickness, self.width)
        volume = cut_length * self.thickness * max(self.width, self.length)
        self.calc_damage(KE, volume)

    def calc_cutting_damage(self, KE, other):
        cut_length = min(other.length, self.width, self.length)
        volume = cut_length * self.thickness * max(self.width, self.length)
        self.calc_damage(KE, volume)


class Human:
    elbow_len = 460 / 1000


m = Low_Carbon()

h = Human()
s = Sword(h, High_Carbon())
a = Chainmail(Low_Carbon())

s.stab(a, 5)
