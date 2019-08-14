import numpy as np


#####################################################
# Math constants
#####################################################
PI = np.pi


#####################################################
# Basic physics and chemistry constants
#####################################################
kB = 1.380658e-23  # [kg m2 s-2 K-1 molec-1], Boltzmann's constant
NA = 6.02214076e23  # [molec mol-1], Avogadro constant
Rgas = 8.31446261815324  # [J K-1 mol-1], gas constant

T00 = 273.15  # [K]

P00 = 1.0e5  # [Pa]
Patm = 1.01325e5  # [Pa], one standard atmosphere pressure

gacc = 9.81  # [m s-2], gravity acceleration
vonK = 0.4  # [-], von Karman constant

# Thermodynamics
cvd = 717.63   # [J kg-1 K-1], specific heat of dry air at constant volume
cvv = 1403.2   # [J kg-1 K-1], specific heat of water vapor at constant volume
cpd = 1004.67  # [J kg-1 K-1], specific heat of dry air at constant pressure
cpv = 1865.1   # [J kg-1 K-1], specific heat of water vapor at constant pressure

molec_mass_dry_air = 4.8096e-26  # [kg molec-1], average mass of one air molecule


#####################################################
# Molar masses [kg mol-1]
#####################################################
M_dryair = 28.966e-3    # dry air
M_H2O    = 18.01528e-3  # water vapor

# Aliases
Md = M_dryair
Mv = M_H2O

# Specific gas constants
Rd = Rgas / Md
Rv = Rgas / Mv


#####################################################
# Other constants
#####################################################
epsv = Rd/Rv  # 0.622
epsv1 = 1.0/epsv
epsv2 = (1.0-epsv)/epsv  # 0.608

kappad = Rd/cpd


#####################################################
# Time and date
#####################################################
# Month days
monthday      = [31, 28, 31, 30, 31,  30, 31, 31, 30, 31,  30, 31]
monthday_leap = [31, 29, 31, 30, 31,  30, 31, 31, 30, 31,  30, 31]

# Number of months per year
nmon = 12
