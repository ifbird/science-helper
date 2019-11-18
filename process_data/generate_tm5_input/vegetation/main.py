#==============================================================================#
# Header
#==============================================================================#

import os
import sys
sys.path.insert(0, '/homeappl/home/putian/scripts/science-helper/pypack')

import numpy as np
from netCDF4 import Dataset

import lu2018
import netcdf
import tools
from local import *


#==============================================================================#
# Set parameters
#==============================================================================#

# Lu2018 veg data files in netcdf format
# fname_lu2018_veg_gxx = {}
# for c in case_list:
#   fname_lu2018_veg_gxx[c] = get_fname_lu2018_veg_gxx(c)

# Meteo vegetation sample files
# fname_sample_veg = get_fname_sample_veg('2009', '01', '01')

# Meteo srols monthly data sample file
# fname_sample_srols = get_fname_sample_srols('2009', '01')


#==============================================================================#
# Main program
#==============================================================================#

#
# Create monthly data file from Lu2018 veg data, use the last year (1859) as the
# default year.
#
year_str = '2009'  # sample year
year_str_new = '1859'  # use the Lu2018 veg data in 1859

for c in case_list:
  print('Creating input monthly veg data for {0} ...'.format(c))

  # Lu2018 veg gxx data
  print('Opening {0} ...'.format(get_fname_lu2018_veg_gxx(c)))
  fid_lu2018_veg_gxx = Dataset(get_fname_lu2018_veg_gxx(c), 'r')

  for m in range(nmon):
    mon_str = '{:02d}'.format(m+1)
    print('- month {0} ...'.format(mon_str))
  
    # Meteo vegetation sample file name
    fname_sample_veg = get_fname_sample_veg(year_str, mon_str, '01')
  
    # Meteo srols monthly data sample file name
    fname_sample_srols = get_fname_sample_srols(year_str, mon_str)
  
    # New input veg data 
    fname_new_veg = get_fname_new_veg(c, year_str_new, mon_str)
  
  
    # Meteo veg sample data
    print('-- Opening {0} ...'.format(fname_sample_veg))
    fid_sample_veg, fattrs_sample_veg, fdims_sample_veg, fvars_sample_veg = \
      netcdf.ncdump(fname_sample_veg, verb=False, log_file='sample_veg.txt')
  
    # Meteo srols sample data
    print('-- Opening {0} ...'.format(fname_sample_srols))
    fid_sample_srols, fattrs_sample_srols, fdims_sample_srols, fvars_sample_srols = \
      netcdf.ncdump(fname_sample_srols, verb=False, log_file='sample_srols.txt')
  
    # Create a new netcdf file to save the Lu2018 veg data in the sample format
    fid_new_veg = Dataset(fname_new_veg, 'w')
  
    # Copy global attributes from srols sample files
    netcdf.copy_global_attributes(fid_sample_srols, fid_new_veg)
  
    # Copy dimensions
    for dname in fdims_sample_srols:
      netcdf.copy_dimension(fid_sample_srols, fid_new_veg, dname)
  
    # Copy variables except 'srols'
    for vname in [ \
      'lon', 'lon_bounds', 'lat', 'lat_bounds', \
      'cell_area', \
      'time', 'time_bounds', 'reftime', \
      'timevalues', 'timevalues_bounds', 'reftimevalues' \
      ]:
      netcdf.copy_variable(fid_sample_srols, fid_new_veg, vname)
  
    # Copy variables cvl, cvh, tv01 - tv20 from meteo veg sample file.
    # They share the same dimensions time, lat and lon, so it is OK.
    # In the original meteo veg files, there are only tv01-tv19, tv20 is not used.
    for vname in [ \
      'cvl', 'cvh', \
      'tv01', 'tv02', 'tv03', 'tv04', 'tv05', \
      'tv06', 'tv07', 'tv08', 'tv09', 'tv10', \
      'tv11', 'tv12', 'tv13', 'tv14', 'tv15', \
      'tv16', 'tv17', 'tv18', 'tv19', 'tv20',  \
      ]:
      # Some tv are not included in tm5 input veg files
      if vname in ['tv08', 'tv12', 'tv14', 'tv15', 'tv20']:
        continue

      # Copy variables, here the time dimensions will change to 4 from 1,
      # This should be fixed in the future
      netcdf.copy_variable(fid_sample_veg, fid_new_veg, vname)

      # Copy the values
      var_new = fid_new_veg.variables[vname]

      if vname in ['cvl', 'cvh']:
        # [last year (1859), current month, lon, lat] --> [lat, lon]
        var_gxx = np.transpose(np.squeeze(fid_lu2018_veg_gxx.variables[vname][-1, m][:, :]))

        # Only one time point for monthly data
        var_new[0, :, :] = var_gxx[:, :]
      else:  # vname = tv01 - tv19
        ind_tv = int(vname[-2:]) - 1

        # [last year (1859), current month, lon, lat] --> [lat, lon]
        var_gxx = np.transpose(np.squeeze(fid_lu2018_veg_gxx.variables['tv'][ind_tv, -1][:, :]))

        # Only one time point for monthly data
        # Lu2018 tv data are originally converted to [0, 100] which is consistent with the data
        # in hdf files. However, in nc files the unit is 1, so here we divide them by 100.
        var_new[0, :, :] = var_gxx[:, :]/100.0


    # Close files
    fid_sample_veg.close()
    fid_sample_srols.close()
    fid_new_veg.close()

  # Close Lu2018 veg gxx data file
  fid_lu2018_veg_gxx.close()
