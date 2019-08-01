import numpy as np

from constants import *


def average_thermal_speed(T, molec_mass):
  va = np.sqrt( 8.0*kB*T / (PI*molec_mass) )
  return va


def root_mean_square_speed(T, molec_mass):
  vrms = np.sqrt( 3.0*kB*T / (molec_mass) )
  return vrms


def most_probable_speed(T, molec_mass):
  vp = np.sqrt( 2.0*kB*T / (molec_mass) )
  return vp


def thermal_conductivity_dry_air(T):
  kappa_d = 0.023807 + 7.1128e-5*(T - T00)
  return kappa_d


def thermal_conductivity_water_vapor(T):
  kappa_v = 0.015606 + 8.3680e-5*(T - T00)
  return kappa_v


def thermal_conductivity_moist_air(T, nd, nv):
  kappa_d = thermal_conductivity_dry_air(T)
  kappa_v = thermal_conductivity_water_vapor(T)
  kappa_a = kappa_d*( 1.0 - (1.17 - 1.02*kappa_v/kappa_d) * nv/(nv+nd) )
  return kappa_a


def mmr_water_vapor_vmr(vmr_v):
  mmr_v = epsv * vmr_v
  return mmr_v


def mmr_water_vapor_rho(rhov, rhod):
  mmr_v = rhov/rhod
  return mmr_v


def mmr_water_vapor_p(pv, pd):
  mmr_v = epsv * pv/pd
  return mmr_v


def specific_humidity_rho(rhov, rhod):
  qv = rhov/(rhov+rhod)
  return qv


def specific_humidity_p(pv, pd):
  qv = epsv*pv/(pd+epsv*pv)
  return qv


def specific_humidity_mmr(mmr_v):
  qv = mmr_v/(1.0+mmr_v)
  return qv


def specific_gas_constant_moist_air_mmr(mmr_v):
  Rm = Rd * (1.0+mmr_v/epsv)/(1.0+mmr_v)
  return Rm
  

def specific_gas_constant_moist_air_q(qv):
  Rm = Rd * (1.0 + epsv2 * qv)
  return Rm


def virtual_temperature_mmr(T):
  Tv = T * (1.0+mmr_v/epsv)/(1.0+mmr_v)
  return Tv


def virtual_temperature_q(qv):
  Tv = T * (1.0 + epsv2 * qv)
  return Tv


def molar_mass_moist_air_q(qv):
  Ma = Md / (1.0 + epsv2*qv)
  return Ma


def specific_heat_liquid_water(T):
  """
  " [J kg-1 K-1]
  """
  Tc = T - T00  # [K] --> [degC]
  if (Tc >= -37.0) and (Tc < 0.0):
    cw = 4187.9 - 11.319*Tc - 0.097215*Tc**2 + 0.018317*Tc**3 + 0.0011354*Tc**4
  elif Tc < 35.0:
    cw = 4175.2 + 0.01297*(Tc - 35.0)**2 + 1.5899e-5*(Tc - 35.0)**4
  else:
    print('Out of temperature range')
    cw = -1.0

  return cw


def specific_heat_ice(T):
  """
  " [J kg-1 K-1]
  """
  Tc = T - T00
  if (Tc >= -40.0) and (Tc <= 0.0):
    ci = 2104.6 + 7.322*Tc
  else:
    print('Out of temperature range')
    ci = -1.0

  return ci


def latent_heat_evaporation(T):
  Tc = T - T00
  Le = 2.501e6 - 2370.0*Tc
  return Le


def latent_heat_melting(T):
  Tc = T - T00
  Lm = 3.3358e5 + Tc*(2030.0 - 10.46*Tc)
  return Lm


def latent_heat_sublimation(T):
  Le = latent_heat_evaporation(T)
  Lm = latent_heat_melting(T)
  Ls = Le + Lm
  
  return Ls


def saturation_vapor_pressure_over_water(T):
  # [Pa]
  pvs = 611.2 * np.exp(6816.0*(1.0/T00 - 1.0/T) + 5.1309*np.log(T00/T))
  return pvs


def saturation_vapor_pressure_over_water_empirical(T):
  """
  " Valid from -35 to 35 degC
  """
  Tc = T - T00
  pvs = 611.2 * np.exp( 17.67*Tc / (Tc + 243.5) )
  return pvs


def saturation_vapor_pressure_over_ice(T):
  # [Pa]
  if T <= T00:
    pvi = 611.2*np.exp( 4648*(1.0/T00 - 1.0/T) - 11.64*np.log(T00/T) + 0.02265*(T00 - T) )
  else:
    print('Out of temperature range.')
    pvi = -1.0

  return pvi


def saturation_vapor_pressure_over_ice_empirical(T):
  if (T >= 223.15) and (T <= T00):
    Tc = T - T00
    pvi = 610.64 * np.exp( 21.88*(T-T00) / (T-7.65) )
  else:
    print('Out of temperature range.')
    pvi = -1.0

  return pvi


def relative_humidity_WMO_mmr(mmr_v, mmr_vs):
  return mmr_v/mmr_vs


def relative_humidity_WMO_p(pv, pvs, pa=None):
  if pa is None:  # approximation
    RH = pv/pvs
  else:  # exact
    RH = pv*(pa-pvs) / (pvs*(pa-pv))

  return RH


def dew_point(pv):
  pv_hPa = pv/100.0
  TD = ( 4880.357 - 29.66*np.log(pv_hPa) ) / (19.48 - np.log(pv_hPa))
  return TD


def specific_heat_volume_moist_air(qv):
  cvm = cvd + qv*(cvv - cvd)
  return cvm


def specific_heat_pressure_moist_air(qv):
  cpm = cpd + qv*(cpv - cpd)
  return cpm


def potential_temperature_moist_air(T, P, qv):
  Rm = specific_gas_constant_moist_air_q(qv)
  cpm = specific_heat_pressure_moist_air(qv)
  kappam = Rm / cpm
  thetam = T*(P00/P)**kappam
  return thetam


def potential_temperature_dry_air(T, P):
  thetad = T*(P00/P)**kappad
  return thetad


def potential_virtual_temperature(T, P, qv):
  """
  " First calculate virtual temperture and consider the moist air parcel to dry air,
  " then bring it to 1000 hPa
  """
  Tv = virtual_temperature_q(qv)
  thetav = Tv*(P00/P)**kappad
  return thetav

    
def virtual_potential_temperature(T, P, qv):
  """
  " First bring moist air parcel to 1000 hPa, then calculate its virtual temperature
  """
  thetam = potential_temperature_moist_air(T, P, qv)
  thetapv = thetam * (1.0 + epsv2 * qv)
  return thetapv


def exner_pressure(P):
  Px = (P/P00)**kappad
  return Px


def exner_function(P):
  Px = exner_pressure(P)
  return cpd*Px


def dynamic_viscosity_theory(dmolec, Mgas, T):
  return 5.0/(16.0*NA*dmolec**2) * np.sqrt(Mgas*Rgas*T/PI)


def dynamic_viscosity_air_Sutherland(T):
  return 1.8325e-5 * ( 416.16 / (T+120.0) ) * (T/296.16)**1.5


if __name__ == '__main__':
  T = 200.0
  print(average_thermal_speed(T, molec_mass_dry_air))
  print(root_mean_square_speed(T, molec_mass_dry_air))
  print(most_probable_speed(T, molec_mass_dry_air))

  T = 300.0
  print(average_thermal_speed(T, molec_mass_dry_air))
  print(root_mean_square_speed(T, molec_mass_dry_air))
  print(most_probable_speed(T, molec_mass_dry_air))

  # Surface
  T = 298.0
  dT = -12.0
  dz = 0.001
  kappa_d = thermal_conductivity_dry_air(T)
  Hc = -kappa_d * dT/dz
  print(kappa_d, Hc)

  # Free troposphere
  T = 273.0
  dT_dz = -6.5e-3
  kappa_d = thermal_conductivity_dry_air(T)
  Hc = -kappa_d * dT_dz
  print(kappa_d, Hc)

  # eps
  print('epsv1: ', epsv1)
  print('epsv2: ', epsv2)

  # water vapor
  pd = 1.013e5
  pv = 1.0e3
  T = 298
  qv = specific_humidity_p(pv, pd)
  Ma = molar_mass_moist_air_q(qv)
  Rm = specific_gas_constant_moist_air_q(qv)
  Tv = virtual_temperature_q(qv)
  print('qv: ', qv)
  print('Ma: ', Ma)
  print('Rm: ', Rm)
  print('Tv: ', Tv)
  print('rhoa: ', (pd + pv)/(Rm*T))
  print('rhoa: ', (pd + pv)/(Rd*Tv))

  # Le, Lm, Ls
  print('Le at 100 degC:', latent_heat_evaporation(100 + T00))
  print('Lm at -10 degC:', latent_heat_melting(-10 + T00))

  # svp
  T = np.linspace(250.0, 300.0, 6)
  svp1 = saturation_vapor_pressure_over_water(T)
  svp2 = saturation_vapor_pressure_over_water_empirical(T)
  print('svp1 - svp2:', svp1 - svp2)

  T = 253.15
  svp1 = saturation_vapor_pressure_over_water(T)
  svp2 = saturation_vapor_pressure_over_water_empirical(T)
  print('svp1, svp2 at 253.15:', svp1, svp2)

  T = 298.15
  svp1 = saturation_vapor_pressure_over_water(T)
  svp2 = saturation_vapor_pressure_over_water_empirical(T)
  print('svp1, svp2 at 298.15:', svp1, svp2)

  T = T00 - 20.0
  pvi1 = saturation_vapor_pressure_over_ice(T)
  pvi2 = saturation_vapor_pressure_over_ice_empirical(T)
  print('pvi1, pvi2 at 253.15:', pvi1, pvi2)

  # dew point
  pv = 1200.0
  print(dew_point(pv))

  # Dynamic viscosity of air
  T = 300.0
  eta1 = dynamic_viscosity_theory(3.673e-10, 28.966e-3, T)
  eta2 = dynamic_viscosity_air_Sutherland(T)
  print('Dynamic viscosity of air with theory: ', eta1)
  print('Dynamic viscosity of air with Sutherland equation: ', eta2)
