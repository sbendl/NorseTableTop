import Physics

class Material:
    tensile_ult = None
    tensile_yield = None
    shear_yield = None
    shear_ult = None
    mod_of_elasticity = None
    shear_modulus = None
    strain_at_fracture = None

    def __init__(self):
        self.tensile_stress_strain, self.tensile_elastic_limit, self.tensile_plastic_limit = Physics.calc_stress_strain(
            self.mod_of_elasticity, self.tensile_yield, self.tensile_ult,
            self.strain_at_fracture)
        self.shear_stress_strain, self.shear_elastic_limit, self.shear_plastic_limit = Physics.calc_stress_strain(
            self.shear_modulus, self.shear_yield, self.shear_ult,
            self.strain_at_fracture)


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
