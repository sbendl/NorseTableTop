import math
from scipy import integrate

import numpy as np


class Chainmail:
    link_thickness = 1.7 / 1000
    link_diameter = 4 / 1000
    thickness = link_thickness * 3
    width = 500 / 1000
    length = 700 / 1000
    layer_padding = 0

    def __init__(self, material):
        self.material = material
        self.min_piercing_limit = self.material.tensile_plastic_limit * 2 * math.pi * (self.link_thickness / 2) ** 2 * (self.link_diameter - self.link_thickness * 2)
        self.min_cutting_limit = self.

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
        # TODO as shear strain increases cross sectional area decreases so tension toughness decreases
        cut_length = min(other.width, self.width, self.length)
        area = 2 * math.pi * (self.link_thickness / 2) ** 2
        print("armour:")
        link_broken = False

        rip_size = self.link_diameter - self.link_thickness * 2

        while rip_size < cut_length and KE > 0:
            link_length = self.link_diameter * math.pi
            volume = area * rip_size
            pl = self.material.tensile_plastic_limit * volume
            el = self.material.tensile_elastic_limit * volume
            print(KE, el, pl)
            if KE * math.cos(other.tip_angle) > pl:
                if not link_broken:
                    volume *= 2
                link_broken = True
                print('Link Broken')
                KE -= pl
                rip_size += link_length
                if rip_size > cut_length:
                    print('Pierced', KE)
            elif KE * math.cos(other.tip_angle) > el:
                print('Bent')
                for s in np.linspace(0, self.material.strain_at_fracture, 100, endpoint=False):
                    e = integrate.quad(self.material.tensile_stress_strain, 0, s)[0] * volume
                    if rip_size * s >= cut_length:
                        KE -= pl
                        print("Pierced", KE)
                        break
                    if e > KE * math.cos(other.tip_angle):
                        print(s * link_length)
                        KE = 0
                        break
                KE = 0
            else:
                print('Deflected')


class Breastplate:
    thickness = 3 / 1000
    width = 500 / 1000
    length = 700 / 1000
    layer_padding = 1 / 1000

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
        cut_length = min(other.width, other.thickness)
        volume = cut_length * self.thickness * self.width * self.length
        self.calc_damage(KE, volume)

    def calc_cutting_damage(self, KE, other):
        cut_length = min(other.length, self.width, self.length)
        volume = cut_length * self.thickness * self.width * self.length
        self.calc_damage(KE, volume)
