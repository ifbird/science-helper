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
# Read data from npz data file
#

##### data1_reg11.npz: lu2018_pi, lu2018_mh, lu2018_mhgsrd
# Dominant monthly average at regular 1x1 grid in Feb from Lu2018
# tv: 0 - 1 --> 0 - 100 to be comparable to tm5 veg
# Set the latitude to from south to north to be the same as tm5 veg2009
#####
data1 = np.load('data1_reg11.npz')

tv_pi     = data1['lu2018_pi'    ][()]['cv_dom_avg_reg11'][:, 1, ::-1, :] * 100
tv_mh     = data1['lu2018_mh'    ][()]['cv_dom_avg_reg11'][:, 1, ::-1, :] * 100
tv_mhgsrd = data1['lu2018_mhgsrd'][()]['cv_dom_avg_reg11'][:, 1, ::-1, :] * 100

lon_lu2018 = data1['lu2018_pi'][()]['lon_reg11']
lat_lu2018 = data1['lu2018_pi'][()]['lat_reg11']


##### data2_tm5veg_200902.npz: tv, cvh, cvl, lat, lon
# tv, cvh, cvl from tm5 veg input data in Feb, 2009
# tv: 0 - 100
# cvh: 0 - 1
# cvl: 0 - 1
#####
data2 = np.load('data2_tm5veg_200902.npz')

tv_2009  = data2['tv']
cvh_2009 = data2['cvh']
cvl_2009 = data2['cvl']

lon_2009 = data2['lon']
lat_2009 = data2['lat']

cv_2009 = np.copy(tv_2009)
cv_2009[lf.tm5_veg_high-1, :, :] = tv_2009[lf.tm5_veg_high-1, :, :] * cvh_2009[np.newaxis, :, :]
cv_2009[lf.tm5_veg_low -1, :, :] = tv_2009[lf.tm5_veg_low -1, :, :] * cvl_2009[np.newaxis, :, :]


##### data3_input.npz: tv, cvh, cvl, lat, lon for PI, MH, MH_gsrd
# tv: 0 - 100
# This input data should be comparable to tm5 veg 2009
#####
data3 = np.load('data3_input.npz')

input_pi     = data3['input_pi'    ][()]
input_mh     = data3['input_mh'    ][()]
input_mhgsrd = data3['input_mhgsrd'][()]

tv_pi_input     = input_pi['tv']
tv_mh_input     = input_mh['tv']
tv_mhgsrd_input = input_mhgsrd['tv']

cvh_pi_input = input_pi['cvh']
cvh_mh_input = input_mh['cvh']
cvh_mhgsrd_input = input_mhgsrd['cvh']

cvl_pi_input = input_pi['cvl']
cvl_mh_input = input_mh['cvl']
cvl_mhgsrd_input = input_mhgsrd['cvl']

# Real coverage percent of each veg type
cv_pi_input = np.copy(tv_pi_input)
cv_pi_input[lf.tm5_veg_high-1, :, :] = tv_pi_input[lf.tm5_veg_high-1, :, :] * cvh_pi_input[np.newaxis, :, :]
cv_pi_input[lf.tm5_veg_low -1, :, :] = tv_pi_input[lf.tm5_veg_low -1, :, :] * cvl_pi_input[np.newaxis, :, :]

cv_mh_input = np.copy(tv_mh_input)
cv_mh_input[lf.tm5_veg_high-1, :, :] = tv_mh_input[lf.tm5_veg_high-1, :, :] * cvh_mh_input[np.newaxis, :, :]
cv_mh_input[lf.tm5_veg_low -1, :, :] = tv_mh_input[lf.tm5_veg_low -1, :, :] * cvl_mh_input[np.newaxis, :, :]

cv_mhgsrd_input = np.copy(tv_mhgsrd_input)
cv_mhgsrd_input[lf.tm5_veg_high-1, :, :] = tv_mhgsrd_input[lf.tm5_veg_high-1, :, :] * cvh_mhgsrd_input[np.newaxis, :, :]
cv_mhgsrd_input[lf.tm5_veg_low -1, :, :] = tv_mhgsrd_input[lf.tm5_veg_low -1, :, :] * cvl_mhgsrd_input[np.newaxis, :, :]


##### Other data processing

# They should have the same lon and lat
lon, lat = lon_2009, lat_2009
nlon, nlat = lon.size, lat.size


##### onlinedust_4.nc

od_fdir = '../data/tm5_input_modified'
od_fname = od_fdir + '/onlinedust_4.nc'
od_fid, od_fattr, od_fdim, od_fvar = pf.ncdump(od_fname, verb=False)

od_potsrc = od_fid.variables['potsrc'][:]  # [180, 360], 0 - 1
od_soilph = od_fid.variables['soilph'][:]  # [5, 180, 360], 0 - 1
od_cult = od_fid.variables['cult'][:]  # [180, 360], 0 - 1

od_lon, od_lat = od_fid.variables['lon'][:], od_fid.variables['lat'][:]  # 180, 360
od_nlon, od_nlat = od_lon.size, od_lat.size
od_nsoilph = 5


"""
cvh_new = np.zeros((nlat, nlon))
cvl_new = np.zeros((nlat, nlon))
for i in range(lf.nvt):
  tvstr = 'tv{:02d}'.format(int(i+1))
  # High
  if lf.tm5_veg_type[tvstr][1] == 'H':
    cvh_new += tv_2009[i, :, :]*lf.tm5_cveg[i]
  elif lf.tm5_veg_type[tvstr][1] == 'L':
    cvl_new += tv_2009[i, :, :]*lf.tm5_cveg[i]
  else:
    pass
tvh_2009 = np.sum(tv_2009[lf.tm5_veg_high-1, :, :], axis=0)
tvl_2009 = np.sum(tv_2009[lf.tm5_veg_low-1, :, :], axis=0)

tvh_pi = np.sum(tv_pi[lf.tm5_veg_high-1, :, :], axis=0)
tvl_pi = np.sum(tv_pi[lf.tm5_veg_low-1, :, :], axis=0)

# print(cvh_new[40,100:150])
# print(cvh_2009[40,100:150])
# print(np.max(np.abs(cvh_new - cvh_2009)))
# print(np.max(np.abs(cvl_new - cvl_2009)))
# print(cvh_2009[40, 100:150] + cvl_2009[40, 100:150])
print(tvh_2009[40, 100:150])
print(tvl_2009[40, 100:150])
print(tvh_pi[40, 100:150])
print(tvl_pi[40, 100:150])
print(np.max(tvh_pi), np.max(tvl_pi))
print(np.max( tvh_pi + tvl_pi ))
print(np.max(tvh_2009), np.max(tvl_2009))
print(np.max( tvh_2009 + tvl_2009 ))

sys.exit()
"""


#
# Plot the data
#
DPI = lf.DPI

##### Plot onlinedust_4.nc data
pm = 'cyl'

od_xpm, od_ypm = lf.ll_to_xy_for_map_pcolor(od_lon, od_lat, pm, lf.reg_glob)


#----- cult -----#
fg, ax = plt.subplots(1, 1, figsize=(12, 8), dpi=DPI)

m = lf.plot_map(ax, pm, lf.reg_glob)

# Mask small values
# The potsrc does not have effects when smaller than 0.5
# od_zm = od_potsrc  # [180, 360]
# od_zm = ma.array(od_potsrc, mask= od_potsrc == 0.00)
od_zm = ma.array(od_cult, mask= od_cult == 0.0)

# Plot pcolor
# h = m.pcolormesh(xpm, ypm, zm, vmin=cv_vmin, vmax=cv_vmax, zorder=3)
h = m.pcolormesh(od_xpm, od_ypm, od_zm, zorder=3)

# Set title
subtitle = 'cultivation'
ax.set_title(subtitle)

# Set colorbar
fg.tight_layout()
# fg.subplots_adjust(bottom=0.10)
# cax = fg.add_axes([0.20, 0.05, 0.6, 0.1])
# cb = fg.colorbar(h, ax=[ax[0,0], ax[0,1], ax[1,0], ax[1,1]], cax=cax, orientation='horizontal')
cb = fg.colorbar(h, orientation='horizontal')
# cb.ax.set_xticklabels(cb.ax.get_xticklabels(), fontsize=14)

# Save the figure
fg.savefig('./figures/onlinedust_cult.png', dpi=DPI)

# sys.exit()


#----- postsrc -----#
fg, ax = plt.subplots(1, 1, figsize=(12, 8), dpi=DPI)

m = lf.plot_map(ax, pm, lf.reg_glob)

# Mask small values
# The potsrc does not have effects when smaller than 0.5
# od_zm = od_potsrc  # [180, 360]
# od_zm = ma.array(od_potsrc, mask= od_potsrc == 0.00)
od_zm = ma.array(od_potsrc, mask= od_potsrc < 0.5)

# Plot pcolor
# h = m.pcolormesh(xpm, ypm, zm, vmin=cv_vmin, vmax=cv_vmax, zorder=3)
h = m.pcolormesh(od_xpm, od_ypm, od_zm, zorder=3)

# Set title
subtitle = 'potential dust sources'
ax.set_title(subtitle)

# Set colorbar
fg.tight_layout()
# fg.subplots_adjust(bottom=0.10)
# cax = fg.add_axes([0.20, 0.05, 0.6, 0.1])
# cb = fg.colorbar(h, ax=[ax[0,0], ax[0,1], ax[1,0], ax[1,1]], cax=cax, orientation='horizontal')
cb = fg.colorbar(h, orientation='horizontal')
# cb.ax.set_xticklabels(cb.ax.get_xticklabels(), fontsize=14)

# Save the figure
fg.savefig('./figures/onlinedust_potsrc.png', dpi=DPI)


#----- soilph -----#
print('Plotting soilph ...')

# Initiate figure
fg, ax = plt.subplots(5, 1, figsize=(12, 30), dpi=DPI)

for i in range(od_nsoilph):
  print(i)

  # Create map
  m = lf.plot_map(ax[i], pm, lf.reg_glob)

  # Mask small values, e.g., smaller than 5%
  # od_zm = od_potsrc  # [180, 360]
  z = od_soilph[i, :, :]
  od_zm = ma.array(z, mask= z == 0.00)

  # Plot pcolor
  # h = m.pcolormesh(xpm, ypm, zm, vmin=cv_vmin, vmax=cv_vmax, zorder=3)
  h = m.pcolormesh(od_xpm, od_ypm, od_zm, zorder=3)

  # Set title
  subtitle = 'soilph {0:2d}'.format(int(i+1))
  ax[i].set_title(subtitle)

# Set colorbar
fg.tight_layout()
fg.subplots_adjust(bottom=0.10)
cax = fg.add_axes([0.20, 0.05, 0.6, 0.1])
# cb = fg.colorbar(h, ax=[ax[0,0], ax[0,1], ax[1,0], ax[1,1]], cax=cax, orientation='horizontal')
cb = fg.colorbar(h, cax=cax, ax=ax, orientation='horizontal')
# cb.ax.set_xticklabels(cb.ax.get_xticklabels(), fontsize=14)

# Save the figure
fg.savefig('./figures/onlinedust_soilph.png', dpi=DPI)

# sys.exit()


##### Plot the monthly mean tv contours for 4 periods to compare
##### 
#####     tvxx
##### ---------------
##### | pi | 2009   |
##### ---------------
##### | mh | mhgsrd |
##### ---------------


#
# Set some general parameters
#
first_time = True
month = 2
tv_vmin, tv_vmax = 0, 100
cv_vmin, cv_vmax = 0, 1

# Calculate x and y from lon and lat
pm = 'cyl'  # map projection

m_base = lf.create_basemap(pm, lf.reg_glob)
# Calculate x, y from lon and lat only once
# Extend lon and lat to the corners for pcolor
dlon = lon[1] - lon[0]
dlat = lat[1] - lat[0]
lonp = np.concatenate( (lon-dlon, [lon[-1]+dlon]) )
latp = np.concatenate( (lat-dlat, [lat[-1]+dlat]) )

# Generate 2D mesh grid
xp, yp = np.meshgrid(lonp, latp)
xpm, ypm = m_base(xp, yp)


# Helper function
def plot_tv_map(ax, tv, xpm, ypm, subtitle):
  m = lf.plot_map(ax, pm, lf.reg_glob)

  # Mask small values, e.g., smaller than 5%
  zm = ma.array(tv, mask= tv < 5)

  # Plot pcolor
  # h = m.pcolormesh(xpm, ypm, zm, vmin=tv_vmin, vmax=tv_vmax, zorder=3)
  h = m.pcolormesh(xpm, ypm, zm, zorder=3)

  # Set title
  ax.set_title(subtitle)

  return m, h


def plot_cv_map(ax, cv, xpm, ypm, subtitle):
  m = lf.plot_map(ax, pm, lf.reg_glob)

  # Mask small values, e.g., smaller than 5%
  zm = ma.array(cv, mask= cv < 0.01)

  # Plot pcolor
  # h = m.pcolormesh(xpm, ypm, zm, vmin=cv_vmin, vmax=cv_vmax, zorder=3)
  h = m.pcolormesh(xpm, ypm, zm, zorder=3)

  # Set title
  ax.set_title(subtitle)

  return m, h


#
# Plot tv or cv for mh_gsrd, mh, pi, 2009 in Feb
#

# Loop for veg types
# for ivt in range(lf.nvt):
for ivt in range(lf.nvt):
  # Set parameters
  ind = int(ivt)
  tvstr = lf.tm5_tvname[ind]
  vtname = lf.tm5_vtname[ind]

  print('Plotting {0} ...'.format(tvstr))

  # Create figure and axes array
  fg, ax = plt.subplots(2, 2, figsize=(30, 20), dpi=DPI)

  #----- MH_gsrd -----#
  m, h = plot_tv_map(ax[0,0], cv_mhgsrd_input[ind, :, :], xpm, ypm, 'MH_gsrd')

  #----- MH -----#
  m, h = plot_tv_map(ax[0,1], cv_mh_input[ind, :, :], xpm, ypm, 'MH')

  #----- PI -----#
  m, h = plot_tv_map(ax[1,0], cv_pi_input[ind, :, :], xpm, ypm, 'PI')

  #----- 2009 -----#
  m, h = plot_tv_map(ax[1,1], cv_2009[ind, :, :], xpm, ypm, '2009')

  # Set colorbar
  fg.tight_layout()
  fg.subplots_adjust(bottom=0.10)
  cax = fg.add_axes([0.20, 0.05, 0.6, 0.1])
  cb = fg.colorbar(h, ax=[ax[0,0], ax[0,1], ax[1,0], ax[1,1]], cax=cax, orientation='horizontal')
  cb.ax.set_xticklabels(cb.ax.get_xticklabels(), fontsize=14)

  # Set figure title
  fg.suptitle('{0:s} {1:s} month {2:2d}'.format(tvstr, vtname, month))

  # Save the figure
  # file_prefix = './figures/tv_4period'
  fg.savefig('./figures/tm5input_cv{0:02d}_4period_mon{1:02d}.png'.format(ind+1, month), dpi=DPI)


#
# Plot cvh and cvl for mh_gsrd, mh, pi, 2009 in Feb
#

print('Plotting cvh ...')

# Create figure and axes array
fg, ax = plt.subplots(2, 2, figsize=(30, 20), dpi=DPI)

#----- MH_gsrd -----#
m, h = plot_cv_map(ax[0,0], cvh_mhgsrd_input[:, :], xpm, ypm, 'MH_gsrd')

#----- MH -----#
m, h = plot_cv_map(ax[0,1], cvh_mh_input[:, :], xpm, ypm, 'MH')

#----- PI -----#
m, h = plot_cv_map(ax[1,0], cvh_pi_input[:, :], xpm, ypm, 'PI')

#----- 2009 -----#
m, h = plot_cv_map(ax[1,1], cvh_2009[:, :], xpm, ypm, '2009')

# Set colorbar
fg.tight_layout()
fg.subplots_adjust(bottom=0.10)
cax = fg.add_axes([0.20, 0.05, 0.6, 0.1])
cb = fg.colorbar(h, ax=[ax[0,0], ax[0,1], ax[1,0], ax[1,1]], cax=cax, orientation='horizontal')
cb.ax.set_xticklabels(cb.ax.get_xticklabels(), fontsize=14)

# Set figure title
fg.suptitle('cvh month {0:2d}'.format(month))

# Save the figure
# file_prefix = './figures/tv_4period'
fg.savefig('./figures/tm5input_cvh_4period_mon{0:02d}.png'.format(month), dpi=DPI)


print('Plotting cvl ...')

# Create figure and axes array
fg, ax = plt.subplots(2, 2, figsize=(30, 20), dpi=DPI)

#----- MH_gsrd -----#
m, h = plot_cv_map(ax[0,0], cvl_mhgsrd_input[:, :], xpm, ypm, 'MH_gsrd')

#----- MH -----#
m, h = plot_cv_map(ax[0,1], cvl_mh_input[:, :], xpm, ypm, 'MH')

#----- PI -----#
m, h = plot_cv_map(ax[1,0], cvl_pi_input[:, :], xpm, ypm, 'PI')

#----- 2009 -----#
m, h = plot_cv_map(ax[1,1], cvl_2009[:, :], xpm, ypm, '2009')

# Set colorbar
fg.tight_layout()
fg.subplots_adjust(bottom=0.10)
cax = fg.add_axes([0.20, 0.05, 0.6, 0.1])
cb = fg.colorbar(h, ax=[ax[0,0], ax[0,1], ax[1,0], ax[1,1]], cax=cax, orientation='horizontal')
cb.ax.set_xticklabels(cb.ax.get_xticklabels(), fontsize=14)

# Set figure title
fg.suptitle('cvl month {0:2d}'.format(month))

# Save the figure
# file_prefix = './figures/tv_4period'
fg.savefig('./figures/tm5input_cvl_4period_mon{0:02d}.png'.format(month), dpi=DPI)

