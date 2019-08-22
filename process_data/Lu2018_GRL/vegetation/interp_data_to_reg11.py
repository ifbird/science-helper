#==============================================================================#
#
# Prepare the input data for MH simulation with TM5-MP.
#
# Vegetation input
#
# Online dust input
#
#==============================================================================#

#
# Import header
#
import sys

import netCDF4 as netcdf

import numpy as np

from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.interpolate import griddata

import putian_functions as pf
import local_functions as lfunc


#==============================================================================#
#
# Helper functions
#
#==============================================================================#
def add_lon_lat(data):
  # lon and lat for each grid
  
  # Land RG grid
  lon_land = data['lon']
  lat_land = data['lat']
  
  # Global RG grid, west --> east, south --> north
  lon_globrg, lat_globrg = lfunc.generate_global_reduced_gaussian_grid(lfunc.nlon_N80, lfunc.lat_N80)

  data['lon_globrg'] = lon_globrg
  data['lat_globrg'] = lat_globrg
  
  # Global regular 1x1 grid, west --> east, south --> north
  lon_reg11 = np.linspace(-179.5, 179.5, 360)
  lat_reg11 = np.linspace(-89.5, 89.5, 180)
  
  nlon_reg11 = lon_reg11.size
  nlat_reg11 = lat_reg11.size
  
  data['lon_reg11'] = lon_reg11
  data['lat_reg11'] = lat_reg11
  
  # Global regular lon with reduced Gaussian lat, west --> east, south --> north
  lon_regrg = np.copy(lon_reg11)
  lat_regrg = np.copy(lat_globrg)
  
  nlon_regrg = lon_regrg.size
  nlat_regrg = lat_regrg.size
  
  data['lon_regrg'] = lon_regrg
  data['lat_regrg'] = lat_regrg

  # Land ind in global grid for RG grid
  land_ind = lfunc.get_land_ind_in_glob_reduced_gaussian_grid(lon_land, lat_land, lon_globrg, lat_globrg)

  data['land_ind'] = land_ind

  return data


def interp_data(data):
  # Set parameters
  nvt = 20
  nmon = 12

  # Get information of lon and lat
  lon_land, lat_land = data['lon'], data['lat']
  lon_globrg, lat_globrg = data['lon_globrg'], data['lat_globrg']
  lon_regrg, lat_regrg = data['lon_regrg'], data['lat_regrg']
  lon_reg11, lat_reg11 = data['lon_reg11'], data['lat_reg11']
  land_ind = data['land_ind']

  nlon_regrg, nlat_regrg = lon_regrg.size, lat_regrg.size
  nlon_reg11, nlat_reg11 = lon_reg11.size, lat_reg11.size

  print(nlon_regrg, nlat_regrg, nlon_reg11, nlat_reg11)

  # Initiate data array
  # The values of tv_dom_* should be 0 or 100
  # The values of cv_dom_avg_* should be 0 - 1
  data['tv_dom_regrg'] = np.zeros((nvt, nlat_regrg, nlon_regrg))
  data['tv_dom_reg11'] = np.zeros((nvt, nlat_reg11, nlon_reg11))
  data['cvh_dom_avg_regrg'] = np.zeros((nmon, nlat_regrg, nlon_regrg))
  data['cvh_dom_avg_reg11'] = np.zeros((nmon, nlat_reg11, nlon_reg11))
  data['cvl_dom_avg_regrg'] = np.zeros((nmon, nlat_regrg, nlon_regrg))
  data['cvl_dom_avg_reg11'] = np.zeros((nmon, nlat_reg11, nlon_reg11))
  
  # tv_dom_*
  # Loop for each veg type
  print('Interpolating tv_dom_reg* ...')
  for iv in range(nvt):
    print('veg: {0}'.format(iv+1))
    data['tv_dom_regrg'][int(iv), :, :], data['tv_dom_reg11'][int(iv), :, :] = \
      lfunc.interp_part_reduced_gaussian_regular_grid(lon_land, lat_land, data['land_ind'], data['tv_dom'][int(iv), :], \
      lon_globrg, lat_globrg, lon_regrg, lat_regrg, lon_reg11, lat_reg11, kind='nearest')

  # cvh_dom_avg_* and cvl_dom_avg_*
  # Loop for each month
  print('Interpolating cvl_dom_avg_reg* and cvh_dom_avg_reg* ...')
  for im in range(nmon):
    print('month: {0}'.format(im+1))
    data['cvh_dom_avg_regrg'][int(im), :, :], data['cvh_dom_avg_reg11'][int(im), :, :] = \
      lfunc.interp_part_reduced_gaussian_regular_grid(lon_land, lat_land, data['land_ind'], data['cvh_dom_avg'][int(im), :], \
      lon_globrg, lat_globrg, lon_regrg, lat_regrg, lon_reg11, lat_reg11, kind='linear')

    data['cvl_dom_avg_regrg'][int(im), :, :], data['cvl_dom_avg_reg11'][int(im), :, :] = \
      lfunc.interp_part_reduced_gaussian_regular_grid(lon_land, lat_land, data['land_ind'], data['cvl_dom_avg'][int(im), :], \
      lon_globrg, lat_globrg, lon_regrg, lat_regrg, lon_reg11, lat_reg11, kind='linear')

  return data


#==============================================================================#
#
# Read LPJ-GUESS veg data obtained from Lu2018 (GRL)
#
# Lu2018:
#   They simulated three cases with different climate forcing.
#   PI: preindustrial with standard CMIP5 (Taylor2012)
#   MH: insolation, greenhouse gas in MH
#   MHgsrd: MH case with green Sahara and 80% reduced dust concentration (Pausata2016)
#
#==============================================================================#

# Lu2018 lpjg veg data folder
dir_lu2018_data = '../data/lu2018_lpjg_monthly_veg'

# Read data
print('Reading Lu2018 data for PI ...')
lu2018_pi     = lfunc.read_Lu2018_lpjg_data(dir_lu2018_data + '/LPJ-GUESS_monthlyoutput_PI.txt'    )
print('Reading Lu2018 data for MH ...')
lu2018_mh     = lfunc.read_Lu2018_lpjg_data(dir_lu2018_data + '/LPJ-GUESS_monthlyoutput_MH.txt'    )
print('Reading Lu2018 data for MHgsrd ...')
lu2018_mhgsrd = lfunc.read_Lu2018_lpjg_data(dir_lu2018_data + '/LPJ-GUESS_monthlyoutput_MHgsrd.txt')


#==============================================================================#
# Interpolate the scattered data to regular lon-lat coordinates
#
# Now the bi-linear interpolation is used to get the coverage for the grid cells:
# describe the interpolation method ...
#
# 1. Read the land grid ll: lon_land, lat_land
# 2. Generate the global grid ll: lon_glob, lat_glob
# 3. Generate regular global grid for reduced Gaussian latitudes and 1 degree lat
# 4. Obtain the indices of lon and lat for each land grid in the global grid: land_ind
# 5. Interpolation:
#    (1) Loop for each latitude
#    (2) Put the land data to global grid for reduced Gaussian grid
#    (3) Interpolate every latitude from global reduced Gaussian to global regular grid
#    (4) Interpolate for every longitude in the regular grid
#==============================================================================#

nvt = 20
nmon = 12

#
# Add lon and lat to data
#

print('Add globrg, regrg, reg11 lat and lon to lu2018_pi ...')
add_lon_lat(lu2018_pi)

print('Add globrg, regrg, reg11 lat and lon to lu2018_mh ...')
add_lon_lat(lu2018_mh)

print('Add globrg, regrg, reg11 lat and lon to lu2018_mhgsrd ...')
add_lon_lat(lu2018_mhgsrd)


#
# Start interpolation
#

print('Interpolating lu2018_pi ...')
interp_data(lu2018_pi)

print('Interpolating lu2018_mh ...')
interp_data(lu2018_mh)

print('Interpolating lu2018_mhgsrd ...')
interp_data(lu2018_mhgsrd)


#
# Save the data
#
np.savez('data1_reg11.npz', lu2018_pi=lu2018_pi, lu2018_mh=lu2018_mh, lu2018_mhgsrd=lu2018_mhgsrd) 


sys.exit()


#
# Check the data
#
DPI = 200

def plot_tv_dom_avg_for_raw_interpolated(data):
  """
  " Plot tv_dom_avg and tv_dom_avg_reg11 for comparison for each veg type and month
  " Loop veg type --> loop month
  " ax[0]; raw tv_dom_avg
  " ax[1]: interpolated tv_dom_avg at regular 1x1 grid
  """
  # Set parameters
  lon_raw, lat_raw = data['lon'], data['lat']
  lon_int, lat_int = data['lon_reg11'], data['lat_reg11']

  # Loop for each veg type existed in lpjg or Lu2018 dataset
  for v in data['vt_set']:
    # Array index of veg type
    iv = int(v-1)
    
    # Set string for tv##
    tvname = lf.tm5_tvname[ivt]
    
    # Name of veg type
    vtname = lf.tm5_vtname[ivt]
    
    # Print info on the screen
    print('Ploting {0} {1} ...'.format(tvname, vtname))
    
    # Skip if the max coverage is 0
    if np.max(data['tv_dom_avg'][ivt, :, :]) <= 0:
      print('No {0} cover.'.format(tvname))
      continue
    
    for mm in range(1, nmon+1):
      imm = int(mm-1)

      # Show some info
      print('-- Month {0:2.0f}'.format(mm))
  
      # Initiate figure
      fg, ax = plt.subplots(2, 1, figsize=(12, 16), dpi=DPI)
  
      # Plot the scatter plot for the raw data
      z = data['tv_dom_avg'][ivt, imm, :]
      zm1 = ma.array(z, mask=z==0)
      m1, h1 = lf.plotax_scatter(ax[0], lon_raw, lat_raw, zm1, vmin=0, vmax=1, pm='cyl', reg=reg_glob, file_prefix='./wow', cmap = plt.get_cmap('Greens'))

      # Plot the pcolor plot for the interpolated
      # m1, h1 = lf.plotax_scatter(ax[0], lon, lat, datam, vmin=0, vmax=1, pm='cyl', reg=reg_glob, file_prefix='./wow', cmap = plt.get_cmap('Greens'):
  
      # Set figure title
      fg.suptitle('{0:s} {1:s} month {2:2.0f}'.format(tvname, vtname, im+1))  # , y=1.08)
  
  # Save the figure
  fg.tight_layout()
  fg.savefig('{0:s}_{1:s}_mon{2:02.0f}.png'.format(file_prefix, tvname, im+1), dpi=DPI)



##### Compare tv_dom_avg and interpolated tv_dom_avg_reg11 in PI

data = lu2018_pi

plot_tv_dom_avg_for_raw_interpolated(data)
