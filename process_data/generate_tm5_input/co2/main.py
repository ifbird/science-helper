#==============================================================================#
# Header
#==============================================================================#

import os
import sys
sys.path.insert(0, '/homeappl/home/putian/scripts/science-helper/pypack')

from shutil import copyfile

import numpy as np
from netCDF4 import Dataset

# Sample CO2 file
fname_sample_co2 = '/proj/atm/EC-Earth/input-tags-3.3.1.1/ifs/cmip6-data/mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_CMIP_UoM-CMIP-1-2-0_gr1-GMNHSH_0000-2014.nc'

# New CO2 file for MH
fname_new_co2_mh = '/homeappl/home/putian/scripts/tm5-mp/data/tm5_input_modified/co2/mh-co2.nc'

# Copy the sample file to the new one
copyfile(fname_sample_co2, fname_new_co2_mh)

# Open the new file and set all the CO2 value to MH value (264.4 ppm)
fid_new_co2_mh = Dataset(fname_new_co2_mh, 'r+')
var = fid_new_co2_mh.variables['mole_fraction_of_carbon_dioxide_in_air']
var[:] = 264.4

# Close the file
fid_new_co2_mh.close()
