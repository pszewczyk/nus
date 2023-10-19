# Natural Unit System

Different things are natural for different people and that's ok.
This package allow conversion between different unit systems, in particular between 'natural' systems. It is done by specifying three primary units (e.g. meter, kilogram and second for SI system), which defines units for the whole system.

### Example usage

Defining unit systems is done by specifying 3 constraints on the basic units:

``` python
from nus.unit_system import UnitSystem

cgs = UnitSystem(len=1e-2, mass=1e-3, time=1)
geo = UnitSystem(Gunit=G, mass=MSol, vel=c)
```

Conversion between systems:

``` python

p_geo = cgs.convert_to(geo, p_cgs, 'pressure')
rho_geo = geo.convert_from(cgs, rho_cgs, 'mass_density')

```
