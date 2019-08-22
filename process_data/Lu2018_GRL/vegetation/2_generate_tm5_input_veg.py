import os
import pandas as pd
import numpy as np

import putian_functions as pf  # used in CSC
import local_functions as lf

# Read data from processed dataset
print('Reading the data from data0 ...')
lu2018 = {}
for c in lf.clist:
  lu2018[c] = np.load('data0_{0}.npz'.format(c))
          
# print(lu2018['pi'])
# print(lu2018[c]['tv_dom_11'].shape)
# print(lu2018[c]['cvl_dom_avg_11'].shape)

# Open original tm5 veg file
print('Opening original tm5 veg file ...')
fname_tm5_input_veg_200902_raw = '/homeappl/home/putian/scripts/tm5-mp/data/tm5_input_modified/ec-ei-an0tr6-sfc-glb100x100-veg_200902.hdf'
fid_raw, fattr_raw, fdset_raw = pf.h4dump(fname_tm5_input_veg_200902_raw, False, 'output_tm5_input_veg_200902_raw.txt')

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

for c in lf.clist:
  fid[c], fattr[c], fdset[c] = lf.create_tm5_input_veg_file( \
    fdir+'/'+fname[c], lu2018[c]['lon_11'], lu2018[c]['lat_11'], \
    lu2018[c]['tv_dom_11'], lu2018[c]['cvh_dom_avg_11'][1, :, :], lu2018[c]['cvl_dom_avg_11'][1, :, :], \
    fid_raw, verb=True, output=fdir+'/'+fout[c])

fid_raw.end()
