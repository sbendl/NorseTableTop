import Physics

class Material:
    tensile_ult = 1
    tensile_yield = 0
    shear_yield = 0
    shear_ult = 1
    mod_of_elasticity = 1
    shear_modulus = 1
    strain_at_fracture = 0
    density = 0

    def __init__(self):
        self.tensile_stress_strain, self.tensile_elastic_limit, self.tensile_plastic_limit = Physics.calc_stress_strain(
            self.mod_of_elasticity, self.tensile_yield, self.tensile_ult,
            self.strain_at_fracture)
        self.shear_stress_strain, self.shear_elastic_limit, self.shear_plastic_limit = Physics.calc_stress_strain(
            self.shear_modulus, self.shear_yield, self.shear_ult,
            self.strain_at_fracture)


class Low_Carbon(Material):
    density = 8.05 * 1000
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
    density = 7.85 * 1000
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
    density = 7.5 * 1000
    tensile_ult = 1010 * 1e6
    tensile_yield = 810 * 1e6
    shear_yield = tensile_yield * .566
    shear_ult = tensile_ult * .566
    mod_of_elasticity = 198 * 1000 * 1e6
    shear_modulus = 79.9 * 1000 * 1e6
    strain_at_fracture = .146

    def __init__(self):
        super().__init__()


class Fleshy(Material):
    density = .985 * 1000
    tensile_ult = .47 * 1e6
    tensile_yield = .42 * 1e6
    shear_yield = tensile_yield * .566
    shear_ult = tensile_ult * .566
    shear_modulus = .3 * 1e6
    mod_of_elasticity = .266 * 1e6
    strain_at_fracture = .2

    def __init__(self):
        super().__init__()

class Muscle(Fleshy):
    density = 1.2 * 1000
    tensile_ult = .47 * 1e6
    tensile_yield = .42 * 1e6
    shear_yield = tensile_yield * .566
    shear_ult = tensile_ult * .566
    shear_modulus = .3 * 1e6
    mod_of_elasticity = .266 * 1e6
    strain_at_fracture = .2

    def __init__(self):
        super().__init__()

class Tendon(Fleshy):
    density = 1.2 * 1000
    tensile_ult = 80 * 1e6
    tensile_yield = 75 * 1e6
    shear_yield = tensile_yield * .566
    shear_ult = tensile_ult * .566
    strain_at_fracture = .25
    mod_of_elasticity = 2 * 1000 * 1e6

    def __init__(self):
        super().__init__()

class Bone(Fleshy):
    tensile_ult = 130 * 1e6
    tensile_yield = 122 * 1e6
    shear_yield = tensile_yield * .566
    shear_ult = tensile_ult * .566
    mod_of_elasticity = 17.6 * 1000 * 1e6
    shear_modulus = 4 * 1000 * 1e6
    strain_at_fracture = .03
    density = 3.3 * 1000

    def __init__(self):
        super().__init__()

