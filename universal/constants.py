import numpy as np

PI = np.pi

kB = 1.380658e-23  # [kg m2 s-2 K-1 molec-1], Boltzmann's constant
NA = 6.02214076e23  # [molec mol-1], Avogadro constant
T00 = 273.15  # [K]
P00 = 1.0e5  # [Pa]
Ps = 1.01325e5  # [Pa]

Rgas = 8.31446261815324  # [J K-1 mol-1], gas constant
Md = 28.966e-3  # [kg mol-1], molar mass of dry air
Mv = 18.01528e-3  # [kg mol-1], molar mass of water vapor
Rd = Rgas / Md
Rv = Rgas / Mv
epsv = Rd/Rv  # 0.622
epsv1 = 1.0/epsv
epsv2 = (1.0-epsv)/epsv  # 0.608

cvd = 717.63   # [J kg-1 K-1], specific heat of dry air at constant volume
cvv = 1403.2   # [J kg-1 K-1], specific heat of water vapor at constant volume
cpd = 1004.67  # [J kg-1 K-1], specific heat of dry air at constant pressure
cpv = 1865.1   # [J kg-1 K-1], specific heat of water vapor at constant pressure

kappad = Rd/cpd


molec_mass_dry_air = 4.8096e-26  # [kg molec-1], average mass of one air molecule
