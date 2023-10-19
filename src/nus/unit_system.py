import numpy as np
from numpy.linalg import solve
from scipy import constants as C
import sys

class Prod:
    def __init__(self, **kwargs):
        self.q = kwargs

base_quantities = ['len', 'time', 'mass', 'T', 'charge']
MSol = 1.9885 * 1e30

quantities = {
        'vel': Prod(len=1, time=-1),
        'acc': Prod(vel=1, time=-1),
        'area': Prod(len=2),
        'vol': Prod(len=3),
        'momentum': Prod(vel=1, mass=1),
        'energy': Prod(vel=2, mass=1),
        'energy_density': Prod(energy=1, len=-3),
        'n_density': Prod(len=-3),
        'mass_density': Prod(mass=1, len=-3),
        'force': Prod(acc=1, mass=1),
        'pressure': Prod(force=1, len=-2),
        'Gunit': Prod(len=3, mass=-1, time=-2),
        }

# example:
# convs = populate(mass=msol, Gunit=G, vel=c)

## get the Prod in terms of the base coeficients
def get_base(k):
    ret = Prod()

    for b in base_quantities:
        ret.q[b] = 0

    if k in base_quantities:
        ret.q[k] = 1
        return ret

    s = quantities[k]
    for quant in s.q:
        if quant in base_quantities:
            ret.q[quant] += s.q[quant]
        else:
            prod = get_base(quant)
            for b in prod.q:
                ret.q[b] += s.q[quant] * prod.q[b]

    return ret
                

def find_conversion(fields, f):
    if f in fields:
        return fields[f]

    ret = 1
    prod = quantities[f]
    for p in prod.q:
        if p in fields:
            conv = fields[p] ** prod.q[p]
        else:
            conv = find_conversion(fields, p)

        ret *= conv

    return ret

## generate (the most) complete conversion table based on given units
def populate(**kwargs):
    ret = {}

    # degrees of freedom
    N = len(kwargs)
    X = np.zeros((N,N))
    Y = np.zeros(N)

    i = 0
    for k in kwargs:
        S = get_base(k)
        for j in range(N):
            X[i][j] = S.q[base_quantities[j]]
        Y[i] = np.log(kwargs[k])
        i += 1

    base = solve(X, Y)
    for i in range(len(base)):
        ret[base_quantities[i]] = np.exp(base[i])

    for f in quantities:
        ret[f] = find_conversion(ret, f)

    return ret

## Defines a unit system based on selected constants
class UnitSystem:
    def __init__(self, **kwargs):
        self.conv = populate(**kwargs)

    ## Convert given value to another unit system
    def convert_to(self, unit_system, value, quantity):
        return value * self.conv[quantity] / unit_system.conv[quantity]

    ## Convert given value to this unit system
    def convert_from(self, unit_system, value, quantity):
        return value * unit_system.conv[quantity] / self.conv[quantity]

    def conversion_factor(self, quantity):
        return self.conv[quantity]

    def add_quantity(self, quantity, **kwargs):
        pass
