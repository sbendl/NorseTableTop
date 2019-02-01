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
