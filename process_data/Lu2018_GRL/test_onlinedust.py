#==============================================================================#
#
# Header
#
#==============================================================================#
import os
import sys
import shutil

import numpy as np
import numpy.ma as ma
from pyhdf.SD import *
from netCDF4 import Dataset

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import putian_functions as pf
import local_functions as lf

# Data directory
fdir = '../data/tm5_input_modified'

# Data file names
fname_raw = fdir + '/onlinedust_4.nc'
fname_pi = fdir + '/onlinedust_4_pi.nc'
fname_mh = fdir + '/onlinedust_4_mh.nc'
fname_mhgsrd = fdir + '/onlinedust_4_mhgsrd.nc'

# Open data file
fid_raw = Dataset(fname_raw, 'r')
fid_pi = Dataset(fname_pi, 'r')
fid_mh = Dataset(fname_mh, 'r')
fid_mhgsrd = Dataset(fname_mhgsrd, 'r')

# Read coordinate which is the same for all datasets
lon, lat = fid_raw.variables['lon'][:], fid_raw.variables['lat'][:]
nlon, nlat = lon.size, lat.size  # 360, 180

#
# Plot figures
#
# Global maps for potsrc, cult, soilph[2] + soilph[3] (namely soilph3 and soilph4 in the onlinedust files)
# Four subplots of raw, pi, mh, and mhgsrd
# Same figures for North African region
#

DPI = 200
pm = 'cyl'
dlist = ['raw', 'pi', 'mh', 'mhgsrd']  # data name list
file_prefix = './figures/'


def plot_global_wafr(data, vmin=0, vmax=1, fg_title='onlinedust', fprefix='onlindust', cmap=None):
  ## Global ##
  print('Ploting in global ...')
  
  # Create the figure and subplots
  fg, ax = plt.subplots(2, 2, figsize=(16, 16), dpi=DPI)
  
  # Plot dataset in subplots
  for a, dstr in zip(ax.flatten(), dlist):
    z = data[dstr]
    zm = ma.array(z, mask=z==0)
    m, h = lf.plotax_pcolormesh(a, lon, lat, zm, vmin=vmin, vmax=vmax, pm=pm, reg=lf.reg_glob, cmap=cmap)
    
    # Set subtitles
    a.set_title(dstr)
    
  
  # Add one colorbar for all
  fg.subplots_adjust(left=0.05, right=0.85, bottom=0.1, top=0.9, wspace=0.1, hspace=0.01)
  cax = fg.add_axes([0.9, 0.15, 0.02, 0.5])
  cb = fg.colorbar(h, cax=cax)
    
  # Set figure title
  fg.suptitle('{0:s}'.format(fg_title))
    
  # Save the figure
  fg.savefig('{0:s}{1:s}.png'.format(fprefix, '_global'), dpi=DPI)
  
  # Close the figure
  plt.clf()
  
  
  ## West Africa ##
  print('Ploting in west Africa ...')
  
  # Create the figure and subplots
  fg, ax = plt.subplots(2, 2, figsize=(16, 16), dpi=DPI)
  
  # Plot dataset in subplots
  for a, dstr in zip(ax.flatten(), dlist):
    z = data[dstr]
    zm = ma.array(z, mask=z==0)
    m, h = lf.plotax_pcolormesh(a, lon, lat, zm, vmin=vmin, vmax=vmax, pm=pm, reg=lf.reg_wafr, cmap=cmap)
    
    # Set subtitles
    a.set_title(dstr)
  
  # Add one colorbar for all
  fg.subplots_adjust(left=0.05, right=0.85, bottom=0.1, top=0.9, wspace=0.1, hspace=0.01)
  cax = fg.add_axes([0.9, 0.15, 0.02, 0.5])
  cb = fg.colorbar(h, cax=cax)
    
  # Set figure title
  fg.suptitle('{0:s}'.format(fg_title))
    
  # Save the figure
  fg.savefig('{0:s}{1:s}.png'.format(fprefix, '_wafr'), dpi=DPI)
  
  # Close the figure
  plt.clf()

  
##### Potential dust source
print('Ploting potential dust source ...')

# Read the data
potsrc = {}
potsrc['raw'] = fid_raw.variables['potsrc'][:]  # [nlat, nlon]
potsrc['pi'] = fid_pi.variables['potsrc'][:]  # [nlat, nlon]
potsrc['mh'] = fid_mh.variables['potsrc'][:]  # [nlat, nlon]
potsrc['mhgsrd'] = fid_mhgsrd.variables['potsrc'][:]  # [nlat, nlon]

# plot_global_wafr(potsrc, vmin=0, vmax=1, fg_title='Potential dust source', fprefix='./figures/onlinedust_potsrc')


##### cult
print('Ploting cult ...')

# Read the data
cult = {}
cult['raw'] = fid_raw.variables['cult'][:]  # [nlat, nlon]
cult['pi'] = fid_pi.variables['cult'][:]  # [nlat, nlon]
cult['mh'] = fid_mh.variables['cult'][:]  # [nlat, nlon]
cult['mhgsrd'] = fid_mhgsrd.variables['cult'][:]  # [nlat, nlon]

lf.show_statistics(cult['raw'])

# plot_global_wafr(cult, vmin=0, vmax=1, fg_title='Cultivation', fprefix='./figures/onlinedust_cult')


##### soilph
print('Ploting soilph...')

# Read the data
soilph = {}
soilph['raw']    = fid_raw.variables['soilph'][:][2, :, :]    + fid_raw.variables['soilph'][:][3, :, :]  # [nlat, nlon]
soilph['pi']     = fid_pi.variables['soilph'][:][2, :, :]     + fid_pi.variables['soilph'][:][3, :, :]  # [nlat, nlon]
soilph['mh']     = fid_mh.variables['soilph'][:][2, :, :]     + fid_mh.variables['soilph'][:][3, :, :]  # [nlat, nlon]
soilph['mhgsrd'] = fid_mhgsrd.variables['soilph'][:][2, :, :] + fid_mhgsrd.variables['soilph'][:][3, :, :]  # [nlat, nlon]

lf.show_statistics(soilph['raw'])

plot_global_wafr(soilph, vmin=0, vmax=1, fg_title='Soilph (3 + 4)', fprefix='./figures/onlinedust_soilph34', cmap=plt.get_cmap('Wistia'))