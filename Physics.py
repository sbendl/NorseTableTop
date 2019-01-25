
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


def logit(x, L, k, x0, y0):
    try:
        return -math.log(L / (k * (x - x0)) - 1) + y0
    except Exception:
        print(x)


# def logit(x, L, k, x0, y0):
#     try:
#         return (x * x0 - math.log(-1 + L/(k + L/2 - y0)))/x
#     except Exception:
#         print(x)

def logitprime(x, L, k, x0, y0):
    return L / ((x - x0) * (L + k * (-x + x0)))


#     return L / (1 + math.e ** (-k*(x-x0))) + y0 - L / 2

x0 = 0
y0 = 0
step = .001
# plt.plot(np.arange(xmin, xmax, step), [logit(x, L=1, k=1, x0=0, y0=0) for x in np.arange(xmin, xmax, step)])
plt.plot(np.arange(x0, x0 + 1, step), [logit(x, L=1, k=1, x0=0, y0=0) for x in np.arange(x0, x0 + 1, step)])

plt.show()
logitprime(.5, L=1, k=128, x0=0, y0=0)

def compose(slope, tan_x, asymptote):
    func1 = lambda x: x * slope
    tan_y = tan_x * slope
    L = asymptote - tan_y
    k = (L * 4) / slope
    func2 = lambda x: logit(x, L, k, tan_x, tan_y)
    return lambda x: func1(x) if x < tan_x else func2(x)

def compose(slope, tan_x, asymptote):
    func1 = lambda x: x * slope
    tan_y = tan_x * slope
    L = asymptote - tan_y
    k = (L * 4) / slope
    func2 = lambda x: logit(x, L, k, tan_x, tan_y)
    return lambda x: func1(x) if x < tan_x else func2(x)
xmin = 0.1
xmax = 9.9
step = .1
comp = compose(1, 4, 9.9)
plt.plot(np.arange(xmin, xmax, step), [comp(x) for x in np.arange(xmin, xmax, step)])
plt.show()