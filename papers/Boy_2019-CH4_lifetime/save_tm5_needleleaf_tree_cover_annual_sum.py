import sys
sys.path.insert(0, '/users/putian/scripts/science-helper/pypack')

import xarray as xr
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# tm5 vegetation data
tm5_meteo_folder = '/scratch/project_2001025/tm5mp/TM5_METEO/2009'
tm5_veg_files = 'ec-ei-an0tr6-sfc-glb100x100-2009-veg_2009*.nc'
tm5_veg_xrds = xr.open_mfdataset(tm5_meteo_folder + '/' + tm5_veg_files)

# tm5 needle leaf vegetation cover sum dataarray
tm5_veg_nltc_sum = (tm5_veg_xrds['tv03'] + tm5_veg_xrds['tv04']).sum(dim='time')

# Rename the xarray dataarray name
tm5_veg_nltc_sum.name = 'needleleaf_tree_cover_annual_sum'

# Save the data
data_folder = '/scratch/project_2001025/putian/Boy_2019-CH4_lifetime'
tm5_veg_nltc_sum.to_netcdf(data_folder + '/tm5_needleleaf_tree_cover_annual_sum.nc')
