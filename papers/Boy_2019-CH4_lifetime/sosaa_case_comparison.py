import sys
sys.path.insert(0, '/users/putian/scripts/science-helper/')

import numpy as np
import xarray as xr

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# pypack
import pypack.sosaa as ppsosaa
import pypack.tools as pptools
import pypack.functions as ppfunc


# ==================================================== #
#
# Helper Functions
#
# ==================================================== #
def calculate_vertically_monthly_mean(xrds, var_name):
  # Calculate grid height weights 
  lev = xrds['lev'].values
  dlev = xrds['lev'].copy()
  dlev.values[0] = 0.0
  dlev.values[-1] = 0.0
  dlev.values[1:-1] = 0.5*(lev[2:] - lev[0:-2])

  # Calculate monthly mean
  # print(xrds[var_name].groupby('time.month').mean('time'))
  var_mavg = ppfunc.masked_average( xrds[var_name].groupby('time.month').mean('time'), \
      dim=('lev'), weights=dlev )
  var_mavg.name = var_name

  # Return a dataarray
  return dlev, var_mavg


def compare_two_cases():
  pass


# Read data
case_folder = '/scratch/project_2001025/sosaa/cases'
data_folder = '/scratch/project_2001025/putian/Boy_2019-CH4_lifetime'
case_list = ['BASE', 'E6C6', 'E6C0']

case_xrds = {}

case_xrds['BASE'] = xr.open_dataset(data_folder + '/BASE.nc')
case_xrds['E6C6'] = xr.open_dataset(data_folder + '/E6C6.nc')
case_xrds['E6C0'] = xr.open_dataset(data_folder + '/E6C0.nc')


# Monthly mean MT and relative changes
MT_mavg = {}
for c in case_list:
  dlev, MT_mavg[c] = calculate_vertically_monthly_mean(case_xrds[c], 'MT')

MT_mavg_rel = {}
MT_mavg_rel['E6C6-BASE'] = (MT_mavg['E6C6'].values - MT_mavg['BASE'].values) \
    / MT_mavg['BASE'].values * 100.0
MT_mavg_rel['E6C0-BASE'] = (MT_mavg['E6C0'].values - MT_mavg['BASE'].values) \
    / MT_mavg['BASE'].values * 100.0

# Monthly mean MT emission
emi_MT_mavg = {}
for c in case_list:
  dlev, emi_MT_mavg[c] = calculate_vertically_monthly_mean(case_xrds[c], 'emi_MT')

emi_MT_mavg_rel = {}
emi_MT_mavg_rel['E6C6-BASE'] = (emi_MT_mavg['E6C6'].values - emi_MT_mavg['BASE'].values) \
    / emi_MT_mavg['BASE'].values * 100.0
emi_MT_mavg_rel['E6C0-BASE'] = (emi_MT_mavg['E6C0'].values - emi_MT_mavg['BASE'].values) \
    / emi_MT_mavg['BASE'].values * 100.0

# Monthly mean C5H8
C5H8_mavg = {}
for c in case_list:
  dlev, C5H8_mavg[c] = calculate_vertically_monthly_mean(case_xrds[c], 'C5H8')

C5H8_mavg_rel = {}
C5H8_mavg_rel['E6C6-BASE'] = (C5H8_mavg['E6C6'].values - C5H8_mavg['BASE'].values) \
    / C5H8_mavg['BASE'].values * 100.0
C5H8_mavg_rel['E6C0-BASE'] = (C5H8_mavg['E6C0'].values - C5H8_mavg['BASE'].values) \
    / C5H8_mavg['BASE'].values * 100.0

# Monthly mean C5H8 emission
emi_C5H8_mavg = {}
for c in case_list:
  dlev, emi_C5H8_mavg[c] = calculate_vertically_monthly_mean(case_xrds[c], 'emi_C5H8')

emi_C5H8_mavg_rel = {}
emi_C5H8_mavg_rel['E6C6-BASE'] = \
    (emi_C5H8_mavg['E6C6'].values - emi_C5H8_mavg['BASE'].values) \
    / emi_C5H8_mavg['BASE'].values * 100.0
emi_C5H8_mavg_rel['E6C0-BASE'] = \
    (emi_C5H8_mavg['E6C0'].values - emi_C5H8_mavg['BASE'].values) \
    / emi_C5H8_mavg['BASE'].values * 100.0


# ----- Print information -----------------------------

with open('sosaa_case_comparison.txt', 'w') as f:
  print('sum of dlev: ', dlev.sum().values, file=f)
  
  print('{0:>4s}{1:>10s}{2:>10s}{3:>10s}{4:>10s}{5:>10s}{6:>10s}{7:>10s}{8:>10s}'.format( \
      'mon', 'M-E6C6', 'M-E6C0', 'eM-E6C6', 'eM-E6C0', 'I-E6C6', 'I-E6C0', 'eI-E6C6', 'eI-E6C0'), \
      file=f)
  for im in range(1, 13):
    i = im - 1
    print('{0:>4d}{1:10.1f}{2:10.1f}{3:10.1f}{4:10.1f}{5:10.1f}{6:10.1f}{7:10.1f}{8:10.1f}'.format( \
        im, \
        MT_mavg_rel['E6C6-BASE'][i], MT_mavg_rel['E6C0-BASE'][i], \
        emi_MT_mavg_rel['E6C6-BASE'][i], emi_MT_mavg_rel['E6C0-BASE'][i], \
        C5H8_mavg_rel['E6C6-BASE'][i], C5H8_mavg_rel['E6C0-BASE'][i], \
        emi_C5H8_mavg_rel['E6C6-BASE'][i], emi_C5H8_mavg_rel['E6C0-BASE'][i]), \
        file=f)


# ----- Plot -----------------------------

month = MT_mavg['BASE']['month']

# Time series of MT, emi_MT, C5H8, emi_C5H8
# fg, ax = plt.subplots(2, 2, figsize=(16, 12), dpi=150)
fg, ax = plt.subplots(2, 2, figsize=(8, 6), dpi=150)

# Vertically monthly mean of MT: molec cm-3
ax[0,0].plot(month, MT_mavg['BASE'], label='BASE')
ax[0,0].plot(month, MT_mavg['E6C6'], label='E6C6')
ax[0,0].plot(month, MT_mavg['E6C0'], label='E6C0')
ax[0,0].set_xlabel('month')
ax[0,0].set_ylabel(r'MT_mavg (molec cm$^{-3}$)')

# Total emission of MT: molec cm-2 -s = molec cm-3 s-1 * m * 1.0e2
ax[0,1].plot(month, emi_MT_mavg['BASE']*dlev.sum()*1.0e2, label='BASE')
ax[0,1].plot(month, emi_MT_mavg['E6C6']*dlev.sum()*1.0e2, label='E6C6')
ax[0,1].plot(month, emi_MT_mavg['E6C0']*dlev.sum()*1.0e2, label='E6C0')
ax[0,1].set_xlabel('month')
ax[0,1].set_ylabel(r'emi_MT_mavg (molec cm$^{-2}$ s$^{-1}$)')

# Vertically monthly mean of C5H8: molec cm-3
ax[1,0].plot(month, C5H8_mavg['BASE'], label='BASE')
ax[1,0].plot(month, C5H8_mavg['E6C6'], label='E6C6')
ax[1,0].plot(month, C5H8_mavg['E6C0'], label='E6C0')
ax[1,0].set_xlabel('month')
ax[1,0].set_ylabel(r'C5H8_mavg (molec cm$^{-3}$)')

# Total emission of C5H8: molec cm-2 -s = molec cm-3 s-1 * m * 1.0e2
ax[1,1].plot(month, emi_C5H8_mavg['BASE']*dlev.sum()*1.0e2, label='BASE')
ax[1,1].plot(month, emi_C5H8_mavg['E6C6']*dlev.sum()*1.0e2, label='E6C6')
ax[1,1].plot(month, emi_C5H8_mavg['E6C0']*dlev.sum()*1.0e2, label='E6C0')
ax[1,1].set_xlabel('month')
ax[1,1].set_ylabel(r'emi_C5H8_mavg (molec cm$^{-2}$ s$^{-1}$)')

for a in ax.flatten():
  a.legend()

# fg.subplots_adjust(wspace=0.2)
fg.tight_layout()
fg.savefig('sosaa_case_comparison.png', dpi=150)
