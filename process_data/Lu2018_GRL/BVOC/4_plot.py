import sys

from pyhdf.SD import *
from netCDF4 import Dataset

import numpy as np
import numpy.ma as ma

from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors

import putian_functions as pf
import local_functions as lf

#==============================================================================#
# Read data
#==============================================================================#
# Lu2018 lpjg data folder and file names
fdir_lu2018 = '/homeappl/home/putian/scripts/tm5-mp/data/lu2018_lpjg_monthly_bvoc/'

# Load the npz files
lu2018_iso = {}
for c in lf.clist:
  lu2018_iso[c] = np.load('data1_iso_{0}.npz'.format(c))

# Load the npz files
lu2018_mon = {}
for c in lf.clist:
  lu2018_mon[c] = np.load('data1_mon_{0}.npz'.format(c))

# unit_conv = 68.12/60.0  # [mgC m-2 d-1] --> [mg m-2 d-1]
# unit_conv = 1.0  # [mgC m-2 d-1] --> [mg m-2 d-1]
unit_conv = 1.0e-3 * 68.12  # [umol m-2 d-1] --> [mg m-2 d-1]
# lf.show_statistics( lu2018_iso['mh']['emis_avg']*unit_conv )
# lf.show_statistics( lu2018_iso['mh']['emis_avg_11']*unit_conv )
# 
# lf.show_statistics( lu2018_mon['mh']['emis_avg']*unit_conv )
# lf.show_statistics( lu2018_mon['mh']['emis_avg_11']*unit_conv )

# sys.exit()


#==============================================================================#
# Plot
#==============================================================================#
# Global parameters
DPI = 200


#==============================================================================#
# Plot dust load
#==============================================================================#
def plot_iso_emis(data_dict):
  #
  # Plot the original land data
  #

  # Coordinates
  lon_land, lat_land = data_dict['pi']['lon_land'], data_dict['pi']['lat_land']
  nland = lon_land.size
  
  # Set colormap
  bounds = np.array([0.0, 1, 2, 5, 10, 20.0, 50.0, 80.0, 120.0])  # colormap boundaries
  # cmap_tmp = mpl.cm.autumn_r( np.linspace(0.0, 1.0, bounds.size-1) )  # start point of colormap 'Greens'
  cmap_tmp = mpl.cm.rainbow( np.linspace(0.0, 1.0, bounds.size-1) )  # start point of colormap 'Greens'
  # cmap_tmp1 = np.concatenate( ([[237.0/255.0, 201.0/255.0, 175.0/255.0, 1.0]], cmap_tmp), axis=0 )  # add some other colors to the colormap
  cmap = colors.ListedColormap(cmap_tmp)  # create colormap object
  norm = colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)  # create norm index for pcolormesh

  # cm = plt.get_cmap('Wistia')
  # cm = plt.get_cmap('autumn_r')
  # cm = plt.get_cmap('YlOrBr')
  # cm = plt.get_cmap('default')
  # cm_diff = plt.get_cmap('BrBG_r')
  # vmin, vmax = 0.1, 1.6
  # vmin_diff, vmax_diff = -0.04, 0.04
  # ticks_diff = [-0.04, -0.03, -0.02, -0.01, 0, 0.01, 0.02, 0.03, 0.04]
  # eps = vmin
  # eps_diff = 5.0e-4
  # alpha = 0.7
  pm = 'moll'
  plot_reg_glob = lf.reg_glob

  # Initiate figure
  fg, ax = plt.subplots(3, 1, figsize=(16, 24), dpi=DPI)
  
  # Plot dataset in subplots
  titles = ['PI', 'MH', 'MH_gsrd']
  for a, c, t in zip(ax.flatten(), lf.clist, titles):
    print('Plotting {0} ...'.format(c))
    z = np.nanmean(data_dict[c]['emis_avg']*unit_conv, axis=0)  # annual mean
    zm = ma.array(z, mask=z<bounds[0])

    # Set up the map
    m = lf.plot_map(pm='moll', reg=plot_reg_glob, ax=a)
    x, y = m(lon_land, lat_land)

    # Plot the scatter points

    h = m.scatter(x, y, s=4, c=zm, norm=norm, cmap=cmap, zorder=3)
    
    # Set subtitles
    a.set_title(t, fontsize=30)

  # Add one colorbar for all
  fg.subplots_adjust(left=0.05, right=0.85, bottom=0.05, top=0.95)
  cax = fg.add_axes([0.9, 0.25, 0.02, 0.5])
  cb = fg.colorbar(h, cax=cax, ticks=bounds, extend='both')
  cb.ax.tick_params(labelsize=20)
  cb.set_label(label=r'isoprene emission [mgC m$^{-2}$ d$^{-1}$]', size=20)

  # Save the figure
  fg.savefig('{0:s}{1:s}.png'.format('./figures/', 'isoprene_emission'), dpi=DPI)


def plot_mon_emis(data_dict):
  #
  # Plot the original land data
  #

  # Coordinates
  lon_land, lat_land = data_dict['pi']['lon_land'], data_dict['pi']['lat_land']
  nland = lon_land.size
  
  # Set colormap
  bounds = np.array([0.0, 1, 2, 4, 6, 8, 10])  # colormap boundaries
  # cmap_tmp = mpl.cm.autumn_r( np.linspace(0.0, 1.0, bounds.size-1) )  # start point of colormap 'Greens'
  cmap_tmp = mpl.cm.rainbow( np.linspace(0.0, 1.0, bounds.size-1) )  # start point of colormap 'Greens'
  # cmap_tmp1 = np.concatenate( ([[237.0/255.0, 201.0/255.0, 175.0/255.0, 1.0]], cmap_tmp), axis=0 )  # add some other colors to the colormap
  cmap = colors.ListedColormap(cmap_tmp)  # create colormap object
  norm = colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)  # create norm index for pcolormesh

  # cm = plt.get_cmap('Wistia')
  # cm = plt.get_cmap('autumn_r')
  # cm = plt.get_cmap('YlOrBr')
  # cm = plt.get_cmap('default')
  # cm_diff = plt.get_cmap('BrBG_r')
  # vmin, vmax = 0.1, 1.6
  # vmin_diff, vmax_diff = -0.04, 0.04
  # ticks_diff = [-0.04, -0.03, -0.02, -0.01, 0, 0.01, 0.02, 0.03, 0.04]
  # eps = vmin
  # eps_diff = 5.0e-4
  # alpha = 0.7
  pm = 'moll'
  plot_reg_glob = lf.reg_glob

  # Initiate figure
  fg, ax = plt.subplots(3, 1, figsize=(16, 24), dpi=DPI)
  
  # Plot dataset in subplots
  titles = ['PI', 'MH', 'MH_gsrd']
  for a, c, t in zip(ax.flatten(), lf.clist, titles):
    print('Plotting {0} ...'.format(c))
    z = np.nanmean(data_dict[c]['emis_avg']*unit_conv, axis=0)  # annual mean
    zm = ma.array(z, mask=z<bounds[0])

    # Set up the map
    m = lf.plot_map(pm='moll', reg=plot_reg_glob, ax=a)
    x, y = m(lon_land, lat_land)

    # Plot the scatter points

    h = m.scatter(x, y, s=4, c=zm, norm=norm, cmap=cmap, zorder=3)
    
    # Set subtitles
    a.set_title(t, fontsize=30)

  # Add one colorbar for all
  fg.subplots_adjust(left=0.05, right=0.85, bottom=0.05, top=0.95)
  cax = fg.add_axes([0.9, 0.25, 0.02, 0.5])
  cb = fg.colorbar(h, cax=cax, ticks=bounds, extend='both')
  cb.ax.tick_params(labelsize=20)
  cb.set_label(label=r'monoterpene emission [mgC m$^{-2}$ d$^{-1}$]', size=20)

  # Save the figure
  fg.savefig('{0:s}{1:s}.png'.format('./figures/', 'monoterpene_emission'), dpi=DPI)


#==============================================================================#
# Start main code
#==============================================================================#
# Plot
plot_iso_emis(lu2018_iso)
plot_mon_emis(lu2018_mon)
