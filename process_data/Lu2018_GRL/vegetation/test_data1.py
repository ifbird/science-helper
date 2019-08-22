#
# Import header
#
import sys

import netCDF4 as netcdf

import numpy as np
import numpy.ma as ma

from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.interpolate import griddata

import putian_functions as pf
import local_functions as lf


#
# Check the data
#
DPI = 200
nmon = 12

def plot_tv_dom_for_raw_and_interpolated(data, file_prefix):
  """
  " Plot tv_dom and tv_dom_reg11 for comparison for each veg type
  " Loop veg type --> loop month
  " ax[0]; raw tv_dom
  " ax[1]: interpolated tv_dom at regular 1x1 grid
  """
  # Set parameters
  lon_raw, lat_raw = data['lon'], data['lat']
  lon_int, lat_int = data['lon_reg11'], data['lat_reg11']

  # Loop for each veg type existed in lpjg or Lu2018 dataset
  for v in data['vt_set']:
    # Array index of veg type
    iv = int(v-1)
    
    # Set string for tv##
    tvname = lf.tm5_tvname[iv]
    
    # Name of veg type
    vtname = lf.tm5_vtname[iv]
    
    # Print info on the screen
    print('Ploting {0} {1} ...'.format(tvname, vtname))
    
    # Skip if the max coverage is 0
    if np.max(data['tv_dom'][iv, :]) <= 0:
      print('No {0} cover.'.format(tvname))
      continue
    
    # Initiate figure
    fg, ax = plt.subplots(2, 1, figsize=(12, 16), dpi=DPI)
  
    # Plot the scatter plot for the raw data
    z1 = data['tv_dom'][iv, :]
    zm1 = ma.array(z1, mask=z1==0)
    m1, h1 = lf.plotax_scatter(ax[0], lon_raw, lat_raw, zm1, vmin=0, vmax=100, pm='cyl', reg=lf.reg_glob, cmap = plt.get_cmap('Greens'))

    # Plot the pcolor plot for the interpolated
    z2 = data['tv_dom_reg11'][iv, :, :]
    zm2 = ma.array(z2, mask=z2==0)
    m2, h2 = lf.plotax_pcolormesh(ax[1], lon_int, lat_int, zm2, vmin=0, vmax=100, pm='cyl', reg=lf.reg_glob, cmap = plt.get_cmap('Greens'))
  
    # Set figure title
    fg.suptitle('{0:s} {1:s}'.format(tvname, vtname))  # , y=1.08)
  
    # Save the figure
    fg.tight_layout()
    fg.savefig('{0:s}_{1:s}.png'.format(file_prefix, tvname), dpi=DPI)


def plot_cv_for_raw_and_interpolated(data, file_prefix):
  """
  " Plot cvh_dom_avg and cvh_dom_avg_reg11 for comparison for each veg type
  " Plot cvl_dom_avg and cvl_dom_avg_reg11 for comparison for each veg type
  " ax[0]; raw cv_dom_avg
  " ax[1]: interpolated cv_dom_avg_reg11 at regular 1x1 grid
  """
  # Set parameters
  lon_raw, lat_raw = data['lon'], data['lat']
  lon_int, lat_int = data['lon_reg11'], data['lat_reg11']

  #
  # cvl avg for the whole year
  #

  # Initiate figure
  fg, ax = plt.subplots(2, 1, figsize=(12, 16), dpi=DPI)
  
  # Plot the scatter plot for the raw data
  z1 = np.nanmean(data['cvl_dom_avg'][:, :], axis=0)
  zm1 = ma.array(z1, mask=z1==0)
  m1, h1 = lf.plotax_scatter(ax[0], lon_raw, lat_raw, zm1, vmin=0, vmax=1, pm='cyl', reg=lf.reg_glob, cmap = plt.get_cmap('Greens'))
  cb1 = fg.colorbar(h1, ax=ax[0])

  # Plot the pcolor plot for the interpolated
  z2 = np.nanmean(data['cvl_dom_avg_reg11'][:, :, :], axis=0)
  zm2 = ma.array(z2, mask=z2==0)
  m2, h2 = lf.plotax_pcolormesh(ax[1], lon_int, lat_int, zm2, vmin=0, vmax=1, pm='cyl', reg=lf.reg_glob, cmap = plt.get_cmap('Greens'))
  cb2 = fg.colorbar(h2, ax=ax[1])
  
  # Set figure title
  fg.suptitle('{0:s}'.format('Annual mean cvl'))  # , y=1.08)
  
  # Save the figure
  fg.tight_layout()
  fg.savefig('{0:s}_{1:s}.png'.format(file_prefix, 'cvl_annualmean'), dpi=DPI)

  #
  # cvh avg for the whole year
  #

  # Initiate figure
  fg, ax = plt.subplots(2, 1, figsize=(12, 16), dpi=DPI)
  
  # Plot the scatter plot for the raw data
  z1 = np.nanmean(data['cvh_dom_avg'][:, :], axis=0)
  zm1 = ma.array(z1, mask=z1==0)
  m1, h1 = lf.plotax_scatter(ax[0], lon_raw, lat_raw, zm1, vmin=0, vmax=1, pm='cyl', reg=lf.reg_glob, cmap = plt.get_cmap('Greens'))
  cb1 = fg.colorbar(h1, ax=ax[0])

  # Plot the pcolor plot for the interpolated
  z2 = np.nanmean(data['cvh_dom_avg_reg11'][:, :, :], axis=0)
  zm2 = ma.array(z2, mask=z2==0)
  m2, h2 = lf.plotax_pcolormesh(ax[1], lon_int, lat_int, zm2, vmin=0, vmax=1, pm='cyl', reg=lf.reg_glob, cmap = plt.get_cmap('Greens'))
  cb2 = fg.colorbar(h2, ax=ax[1])
  
  # Set figure title
  fg.suptitle('{0:s}'.format('Annual mean cvh'))  # , y=1.08)
  
  # Save the figure
  fg.tight_layout()
  fg.savefig('{0:s}_{1:s}.png'.format(file_prefix, 'cvh_annualmean'), dpi=DPI)


##### Compare tv_dom and interpolated tv_dom_reg11 in PI
data1 = np.load('data1_reg11.npz')
lu2018_pi = data1['lu2018_pi'][()]
lu2018_mh = data1['lu2018_mh'][()]
lu2018_mhgsrd = data1['lu2018_mhgsrd'][()]


# Make the lat of regular grids increasing
# lu2018_pi['lat_reg11'] = lu2018_pi['lat_reg11'][::-1]
# lu2018_pi['tv_dom_reg11'][:, :, :, :] = lu2018_pi['tv_dom_reg11'][:, :, ::-1, :]

# print('lon', lu2018_pi['lon'])
# print('lon_reg11', lu2018_pi['lon_reg11'])
# print('lat', lu2018_pi['lat'])
# print('lat_reg11', lu2018_pi['lat_reg11'])
# sys.exit()

# Plot tv
# plot_tv_dom_for_raw_and_interpolated(lu2018_pi, './figures/test_interp_pi')
# plot_tv_dom_for_raw_and_interpolated(lu2018_mh, './figures/test_interp_mh')
# plot_tv_dom_for_raw_and_interpolated(lu2018_mhgsrd, './figures/test_interp_mhgsrd')

# Plot cvl and cvh
print('Plotting cvl and cvh for pi ...')
plot_cv_for_raw_and_interpolated(lu2018_pi, './figures/test_interp_pi')
print('Plotting cvl and cvh for mh ...')
plot_cv_for_raw_and_interpolated(lu2018_mh, './figures/test_interp_mh')
print('Plotting cvl and cvh for mhgsrd ...')
plot_cv_for_raw_and_interpolated(lu2018_mhgsrd, './figures/test_interp_mhgsrd')