import pandas as pd
import numpy as np

import local_functions as lf

# Lu2018 lpjg data folder
fdir_lu2018 = '/homeappl/home/putian/scripts/tm5-mp/data/lu2018_lpjg_monthly_bvoc/'

#
# Isoprene
#

# # Lu2018 lpjg data file names
# fname_lu2018_iso = {}
# fname_lu2018_iso['pi'] = fdir_lu2018 + '/out_bvoc_pi/miso_1850_1859.txt'
# fname_lu2018_iso['mh'] = fdir_lu2018 + '/out_bvoc_mh/miso_1850_1859.txt'
# fname_lu2018_iso['mg'] = fdir_lu2018 + '/out_bvoc_mhgsrd/miso_1850_1859.txt'
# 
# # Read raw data as instances of class DatasetLu2018
# lu2018_iso = {}
# for c in lf.clist:
#   lu2018_iso[c] = lf.DatasetLu2018Bvoc(fname_lu2018_iso[c])
# 
# # Interpolate data from land reduced Gaussian to regular 1x1 grid
# for c in lf.clist:
#   lu2018_iso[c].get_data_on_regular_grid()
# 
# # Save the original data and interpolated data to npz file
# for c in lf.clist:
#   lu2018_iso[c].save_data('data1_iso_{0}.npz'.format(c))

#
# Monoterpenes
#

# Lu2018 lpjg data file names
fname_lu2018_mon = {}
fname_lu2018_mon['pi'] = fdir_lu2018 + '/out_bvoc_pi/mmon_1850_1859.txt'
fname_lu2018_mon['mh'] = fdir_lu2018 + '/out_bvoc_mh/mmon_1850_1859.txt'
fname_lu2018_mon['mg'] = fdir_lu2018 + '/out_bvoc_mhgsrd/mmon_1850_1859.txt'

# Read raw data as instances of class DatasetLu2018
lu2018_mon = {}
for c in lf.clist:
  lu2018_mon[c] = lf.DatasetLu2018Bvoc(fname_lu2018_mon[c])

# Interpolate data from land reduced Gaussian to regular 1x1 grid
for c in lf.clist:
  lu2018_mon[c].get_data_on_regular_grid()

# Save the original data and interpolated data to npz file
for c in lf.clist:
  lu2018_mon[c].save_data('data1_mon_{0}.npz'.format(c))
