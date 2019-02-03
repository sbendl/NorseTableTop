import math
from scipy import integrate

import numpy as np

class Sword:
    thickness = 2.6 / 1000
    width = 48.5 / 1000
    length = 886 / 1000
    mass = 1.182
    tip_angle = 45

    def __init__(self, wielder, material):
        self.wielder = wielder
        self.material = material

    def calc_moment_of_inertia(self, extra_length=0):
        return (1 / 3) * self.mass * (self.length + extra_length) ** 2

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