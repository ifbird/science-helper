import sys
sys.path.insert(0, '../../../pypack')

import pandas as pd
import numpy as np

# import local_functions as lf
import lu2018
import tools
import hdf

#==========================#
# Parameters
#==========================#
case_list = ['pi', 'mh1', 'mh2']


# Lu2018 lpjg data folder and file names
fdir_lu2018 = '/wrk/putian/DONOTREMOVE/tm5mp/tm5_meteo/lu2018_lpjg_monthly_veg'

fname_lu2018 = {}
fname_lu2018['pi'] = fdir_lu2018 + '/LPJ-GUESS_monthlyoutput_PI.txt'
fname_lu2018['mh1'] = fdir_lu2018 + '/LPJ-GUESS_monthlyoutput_MH.txt'
fname_lu2018['mh2'] = fdir_lu2018 + '/LPJ-GUESS_monthlyoutput_MHgsrd.txt'

#==========================#
# Read raw data as instances of class DatasetLu2018
#==========================#
data_lu2018 = {}
for c in case_list:
  print(c)
  data_lu2018[c] = lu2018.Lu2018(fname_lu2018[c])

#==========================#
# Interpolate data from land reduced Gaussian to regular 1x1 grid
#==========================#
xbeg, xend, dlon = -180.0, 180.0, 1.0
ybeg, yend, dlat = -90.0, 90.0, 1.0
lon_g11, lat_g11 = tools.calc_gxx_grid(xbeg, xend, dlon, ybeg, yend, dlat)

for c in case_list:
  print(c)
  # Calculate the interpolation and add data_gxx to the data dict
  data_lu2018[c].calc_data_gxx(lon_g11, lat_g11, debug=False)

# Save the original data and interpolated data to npz file
# for c in lf.clist:
#   data_lu2018[c].save_data('data1_{0}.npz'.format(c))


#==========================#
# Create tm5 input vegetation files
#==========================#

# Open original tm5 input files to copy
# Time: monthly data like srols
# Others: from veg files
print('Opening original tm5 files ...')
file_format = 'netcdf'
if file_format == 'netcdf4':
  fname_tm5_input_srols_200902_raw = '/homeappl/home/putian/scripts/tm5-mp/data/tm5_input_modified/ec-ei-an0tr6-sfc-glb100x100-veg_200902.hdf'
  fid_raw, fattr_raw, fdset_raw = hdf.h4dump(fname_tm5_input_veg_200902_raw, False, 'output_tm5_input_veg_200902_raw.txt')
elif file_format == 'hdf4':
  fname_tm5_input_veg_200902_raw = '/homeappl/home/putian/scripts/tm5-mp/data/tm5_input_modified/ec-ei-an0tr6-sfc-glb100x100-veg_200902.hdf'
  fid_raw, fattr_raw, fdset_raw = hdf.h4dump(fname_tm5_input_veg_200902_raw, False, 'output_tm5_input_veg_200902_raw.txt')

# Create new tm5 input veg files
print('Creating new tm5 input veg files ...')
fid, fattr, fdset = {}, {}, {}
fdir = '/homeappl/home/putian/scripts/tm5-mp/data/tm5_input_modified'
# fdir = '.'
fname = {'pi': 'ec-ei-an0tr6-sfc-glb100x100-veg_185002_pi.hdf', \
         'mh': 'ec-ei-an0tr6-sfc-glb100x100-veg_6kbp02_mh.hdf', \
         'mg': 'ec-ei-an0tr6-sfc-glb100x100-veg_6kbp02_mhgsrd.hdf'}
fout = {'pi': 'output_tm5_input_veg_pi.txt', \
        'mh': 'output_tm5_input_veg_mh.txt', \
        'mg': 'output_tm5_input_veg_mhgsrd.txt'}

fid[c], fattr[c], fdset[c] = lf.create_tm5_input_veg_file( \
  fdir+'/'+fname[c], data_lu2018[c]['lon_11'], data_lu2018[c]['lat_11'], \
  data_lu2018[c]['tv_dom_11'], data_lu2018[c]['cvh_dom_avg_11'][1, :, :], data_lu2018[c]['cvl_dom_avg_11'][1, :, :], \
  fid_raw, verb=True, output=fdir+'/'+fout[c])
