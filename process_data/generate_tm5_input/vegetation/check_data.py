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

# Lu2018 vegetation data files
fname_lu2018_veg_lrg = {}
for c in case_list:
  fname_lu2018_veg_lrg[c] = get_fname_lu2018_veg_lrg(c)


# New netcdf files
fname_lu2018_veg_gxx = {}
for c in case_list:
  fname_lu2018_veg_gxx[c] = get_fname_lu2018_veg_gxx(c)


# Meteo vegetation sample files
fname_sample_veg = get_fname_sample_veg('2009', '01', '01')


#==============================================================================#
# Main program
#==============================================================================#
#
# Read data
#

# Raw Lu2018 veg data
data_lu2018_veg_lrg = {}
for c in case_list:
  print('----- Lu2018 veg lrg -----: ', c)
  data_lu2018_veg_lrg[c] = lu2018.Lu2018(fname_lu2018_veg_lrg[c])
  tools.show_statistics(data_lu2018_veg_lrg[c].data_lrg['cvl'])
  tools.show_statistics(data_lu2018_veg_lrg[c].data_lrg['cvh'])
  tools.show_statistics(data_lu2018_veg_lrg[c].data_lrg['tv'][5, :, :])

# Meteo veg sample data
fid_sample_veg, fattrs_sample_veg, fdims_sample_veg, fvars_sample_veg = \
  netcdf.ncdump(fname_sample_veg, verb=False, log_file='sample_veg.txt')
print('----- Meteo veg sample -----')
tools.show_statistics(fid_sample_veg.variables['cvl'][:])
tools.show_statistics(fid_sample_veg.variables['cvh'][:])
tools.show_statistics(fid_sample_veg.variables['tv06'][:])

# Lu2018 veg data in gxx grid
fid_lu2018_veg_gxx = {}
for c in case_list:
  print('----- Lu2018 veg gxx: -----', c)
  fid_lu2018_veg_gxx[c] = Dataset(fname_lu2018_veg_gxx[c], 'r')
  tools.show_statistics(fid_lu2018_veg_gxx[c].variables['cvl'][:])
  tools.show_statistics(fid_lu2018_veg_gxx[c].variables['cvh'][:])
  tools.show_statistics(fid_lu2018_veg_gxx[c].variables['tv'][5, -1, :, :])
  tools.show_statistics(fid_lu2018_veg_gxx[c].variables['tv'][5, -2, :, :])
