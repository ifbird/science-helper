import sys
sys.path.insert(0, '../../../pypack')

import pandas as pd
import numpy as np

# import local_functions as lf
import lu2018
import tools

#==========================#
# Parameters
#==========================#
case_list = ['pi', 'mh', 'mg']


# Lu2018 lpjg data folder and file names
fdir_lu2018 = '/wrk/putian/DONOTREMOVE/tm5mp/tm5_meteo/lu2018_lpjg_monthly_veg'

fname_lu2018 = {}
fname_lu2018['pi'] = fdir_lu2018 + '/LPJ-GUESS_monthlyoutput_PI.txt'
fname_lu2018['mh'] = fdir_lu2018 + '/LPJ-GUESS_monthlyoutput_MH.txt'
fname_lu2018['mg'] = fdir_lu2018 + '/LPJ-GUESS_monthlyoutput_MHgsrd.txt'

# Read raw data as instances of class DatasetLu2018
lu2018 = {}
for c in case_list:
  print(c)
  lu2018[c] = lu2018.Lu2018(fname_lu2018[c])

# Interpolate data from land reduced Gaussian to regular 1x1 grid
xbeg, xend, dlon = -180.0, 180.0, 1.0
ybeg, yend, dlat = -90.0, 90.0, 1.0
lon_g11, lat_g11 = tools.calc_gxx_grid(xbeg, xend, dlon, ybeg, yend, dlat)
print(lon_g11, lat_g11)

for c in case_list:
  print(c)
  # data_gxx = lu2018[c].calc_data_gxx(lon_gxx, lat_gxx, debug=False)

# Save the original data and interpolated data to npz file
# for c in lf.clist:
#   lu2018[c].save_data('data1_{0}.npz'.format(c))
