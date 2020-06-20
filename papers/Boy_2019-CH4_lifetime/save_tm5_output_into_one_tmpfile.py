import os
import sys
sys.path.insert(0, '/users/putian/scripts/science-helper/')

from datetime import datetime
from datetime import timedelta

import numpy as np
import xarray as xr
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import pypack.functions as ppfunc


# ---------------------------------------------------------------------- #
#
# Helper Functions
#
# ---------------------------------------------------------------------- #
# Saved data folder
savedir = '/scratch/project_2001025/putian/Boy_2019-CH4_lifetime'


# ----- Save deltaz3d from aerocom3 project ----- #
def save_aerocom3_deltaz3d():
  print('======================================')
  
  case = 'BASE'
  print('Processing case {0} for deltaz3d data'.format(case))
  
  first_time = True
  
  for i in range(0, 12):
    leg = 'output-2009-{0:02d}'.format(i)
    print('-- Reading data from leg {0}'.format(leg))
  
    file_path = \
      '{0}/{1}-{2}-deltaz3d-aerocom3_output.nc'.format( \
      savedir, case, leg)
  
    # Continue the loop if the file does not exist
    if not os.path.exists(file_path):
      print('skip {0}'.format(leg))
      continue
  
    # Read the data
    tmp_ds = xr.open_dataset(file_path)
  
    # Modify the time so the datasets can be merged,
    # leap year is not considered here since it will not affect the results.
    tmp_ds = tmp_ds.assign_coords( \
        {'time': tmp_ds['time'] + np.timedelta64((i-8)*365, 'D')})
  
    if first_time:
      ds_deltaz3d = tmp_ds.copy(deep=True)
      first_time = False
    else:
      ds_deltaz3d = ds_deltaz3d.merge(tmp_ds)
  
  # Save the data
  print('-- Saving the datasets')
  ds_deltaz3d.to_netcdf( \
    '{0}/{1}-output-deltaz3d-aerocom3_output.nc'.format( \
    savedir, case) )



# ----- Save meteorological variables ----- #
def save_general_meteo():
  print('======================================')
  
  case = 'BASE'
  print('Processing case {0} for meteorological data'.format(case))
  
  first_time = True
  
  for i in range(0, 12):
    leg = '2009-{0:02d}'.format(i)
    print('-- Reading data from leg output-{0}'.format(leg))
  
    file_path = \
      '{0}/{1}-output-{2}-temp_airmass_pressure_gph3D_ps-general_output.nc'.format( \
      savedir, case, leg)
  
    # Continue the loop if the file does not exist
    if not os.path.exists(file_path):
      print('skip {0}'.format(leg))
      continue
  
    # Read the data
    tmp_ds = xr.open_dataset(file_path)
  
    # Modify the time so the datasets can be merged,
    # leap year is not considered here since it will not affect the results.
    tmp_ds = tmp_ds.assign_coords( \
        {'time': tmp_ds['time'] + np.timedelta64((i-8)*365, 'D')})
  
    if first_time:
      ds_meteo = tmp_ds.copy(deep=True)
      first_time = False
    else:
      ds_meteo = ds_meteo.merge(tmp_ds)
  
  # Save the data
  print('-- Saving the datasets')
  ds_meteo.to_netcdf( \
    '{0}/{1}-output-temp_airmass_pressure_gph3D_ps-general_output.nc'.format( \
    savedir, case) )


# ----- Save chemical compounds ----- #
def save_general_chem():
  ds = {}
  for case in ['BASE', 'E0C6', 'E6C6']:
    print('======================================')
    print('Processing case {0}'.format(case))
  
    first_time = True
  
    for i in range(0, 12):
      leg = '2009-{0:02d}'.format(i)
      print('-- Reading data from leg output-{0}'.format(leg))
  
      file_path = '{0}/{1}-output-{2}-GAS_CH4_GAS_TERP_GAS_OH-general_output.nc'.format( \
          savedir, case, leg)
  
      # Continue the loop if the file does not exist
      if not os.path.exists(file_path):
        print('skip {0}'.format(leg))
        continue
  
      # Read the data
      tmp_ds = xr.open_dataset(file_path)
  
      # Modify the time so the datasets can be merged,
      # leap year is not considered here since it will not affect the results.
      # tmp_ds = tmp_ds.assign_coords( \
      #     {'time': tmp_ds['time'].values.astype('datetime64[M]') + \
      #     np.timedelta64((i-8)*12, 'M')})
      tmp_ds = tmp_ds.assign_coords( \
          {'time': tmp_ds['time'] + np.timedelta64((i-8)*365, 'D')})
  
      if first_time:
        ds[case] = tmp_ds.copy(deep=True)
        first_time = False
      else:
        ds[case] = ds[case].merge(tmp_ds)
  
    # Save the data
    print('-- Saving the datasets')
    ds[case].to_netcdf('{0}/{1}-output-GAS_CH4_GAS_TERP_GAS_OH-general_output.nc'.format( \
        savedir, case))

save_general_chem()
# save_general_meteo()
# save_aerocom3_deltaz3d()
