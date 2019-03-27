import pandas as pd
import numpy as np

import local_functions as lf

# Lu2018 lpjg data folder and file names
fdir_lu2018 = '/homeappl/home/putian/scripts/tm5-mp/data/lu2018_lpjg_monthly_veg'

fname_lu2018 = {}
fname_lu2018['pi'] = fdir_lu2018 + '/LPJ-GUESS_monthlyoutput_PI.txt'
fname_lu2018['mh'] = fdir_lu2018 + '/LPJ-GUESS_monthlyoutput_MH.txt'
fname_lu2018['mg'] = fdir_lu2018 + '/LPJ-GUESS_monthlyoutput_MHgsrd.txt'

# Read raw data as instances of class DatasetLu2018
lu2018 = {}
for c in lf.clist:
  lu2018[c] = lf.DatasetLu2018(fname_lu2018[c])

# Interpolate data from land reduced Gaussian to regular 1x1 grid
for c in lf.clist:
  lu2018[c].get_data_on_regular_grid()

# Save the original data and interpolated data to npz file
# for c in lf.clist:
#   lu2018[c].save_data('data1_{0}.npz'.format(c))
