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

# inspired by http://nipunbatra.github.io/2014/08/latexify/
# params = {
#     'text.latex.preamble': ['\\usepackage{gensymb}'],
#     'image.origin': 'lower',
#     'image.interpolation': 'nearest',
#     'image.cmap': 'gray',
#     'axes.grid': False,
#     'savefig.dpi': 150,  # to adjust notebook inline plot size
#     'axes.labelsize': 8, # fontsize for x and y labels (was 10)
#     'axes.titlesize': 8,
#     'font.size': 8, # was 10
#     'legend.fontsize': 6, # was 10
#     'xtick.labelsize': 8,
#     'ytick.labelsize': 8,
#     'text.usetex': True,
#     'figure.figsize': [3.39, 2.10],
#     'font.family': 'serif',
# }

# mpl.rcParams.update(params)

# Global parameters
DPI = 200


#==============================================================================#
# Read the data
#==============================================================================#
def read_onlinedust_data():
  dstr_list = ['raw', 'pi', 'mh', 'mg']
  
  # Data directory
  fdir = '/homeappl/home/putian/scripts/tm5-mp/data/tm5_input_modified'
  
  # Data file names
  fname = {}
  fname['raw'] = fdir + '/onlinedust_4.nc'
  fname['pi'] = fdir + '/onlinedust_4_pi.nc'
  fname['mh'] = fdir + '/onlinedust_4_mh.nc'
  fname['mg'] = fdir + '/onlinedust_4_mhgsrd.nc'
  
  # Open data file
  fid = {}
  for d in dstr_list:
    fid[d] = Dataset(fname[d], 'r')
  
  # Read coordinate which is the same for all datasets
  # lon, lat = fid['raw'].variables['lon'][:], fid['raw'].variables['lat'][:]
  # nlon, nlat = lon.size, lat.size  # 360, 180
  
  return fid


def read_dustload_data():
  # High and low vegetation types
  # lu2018_pi = np.load('data1_pi.npz')
  # print('High vegetation types: ', lu2018_pi['vth_set'])
  # print('Low vegetation types: ', lu2018_pi['vtl_set'])
  
  # Read data from files for dust load
  fdir = {}
  fdir['pi'] = '/wrk/putian/tm5-mp-1850/rundir/output'
  fdir['mh'] = '/wrk/putian/tm5-mp-mh/rundir/output'
  fdir['mg'] = '/wrk/putian/tm5-mp-mhgsrd/rundir/output'
    
  fname = {}
  for c in lf.clist:
    fname[c] = fdir[c] + '/aerocom3_TM5_JPK_global_200902_monthly.nc'
    
  fid = {}
  for c in lf.clist:
    fid[c] = Dataset(fname[c], 'r')
  
  # loaddust = {}
  # for c in lf.clist:
  #   loaddust[c] = np.squeeze(fid[c].variables['loaddust'][:])*1.0e3  # [g m-2], [90, 120] after squeeze
  #   print('Max value of dust load in {0}: {1}'.format(c, np.amax(loaddust[c])))

  return fid

#==============================================================================#
# Plot potential sources
#==============================================================================#
def plot_potsrc(fid_od):
  # Parameters
  od_list = ['raw', 'pi', 'mh', 'mg']
  pm = 'cyl'  # Map projection
  reg = lf.reg_wafr
  # mon = 2  # Feb
  # imon = int(mon-1)  # index

  # Coordinates
  lon, lat = fid_od['raw']['lon'], fid_od['raw']['lat']
  nlon, nlat = lon.size, lat.size  # 360, 180
  
  # Get the x and y for pcolor plot, corners of the data points
  xpm, ypm = lf.ll_to_xy_for_map_pcolor(lon, lat, pm, reg)
  
  #
  # Plot the figure
  #
  # -------------
  # RAW | PI
  # -------------
  # MH  | MH_gsrd
  # -------------
  # 

  # Set colormap
  bounds = np.array([0.0, 0.25, 0.5, 0.75, 1])  # colormap boundaries
  cmap_tmp = mpl.cm.autumn_r( np.linspace(0.0, 1.0, bounds.size-1) )  # start point of colormap 'Greens'
  # cmap_tmp1 = np.concatenate( ([[237.0/255.0, 201.0/255.0, 175.0/255.0, 1.0]], cmap_tmp), axis=0 )  # add some other colors to the colormap
  cmap = colors.ListedColormap(cmap_tmp)  # create colormap object
  norm = colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)  # create norm index for pcolormesh

  # Initiate figure and ax
  fg, ax = plt.subplots(2, 2, figsize=(12, 8), dpi=DPI)
  
  titles = ['RAW', 'PI', 'MH', 'MH_gsrd']
  for a, c, t in zip(ax.flatten(), od_list, titles):
    z = fid_od[c]['potsrc'][:]
    zm = ma.array(z, mask=z==0)

    m = lf.plot_map(a, pm=pm, reg=reg)  # parallels=np.arange(-90, 91, 10.0), meridians=np.arange(-180.0, 181.0, 10.0) )
    h = m.pcolormesh(xpm, ypm, zm, norm=norm, cmap=cmap, zorder=2)
    
    # Set subtitles
    a.set_title(t, fontsize=30)
  
  # Set the colorbar for all
  fg.subplots_adjust(top=0.95, bottom=0.05, left=0.10, right=0.85, hspace=0.05)
  cbar_ax = fg.add_axes([0.88, 0.15, 0.02, 0.7])
  cbar = fg.colorbar(h, cax=cbar_ax, ticks=bounds)
  cbar.ax.tick_params(labelsize=18)
  cbar.set_label(label=r'potential source (effective when > 0.5)', size=20)
  
  # save the figure
  fg.savefig('./figures/onlinedust_potsrc.png', dpi=DPI)


#==============================================================================#
# Plot soilph3+4
#==============================================================================#
def plot_soilph34(fid_od):
  # Parameters
  od_list = ['raw', 'pi', 'mh', 'mg']
  pm = 'cyl'  # Map projection
  reg = lf.reg_wafr

  # Coordinates
  lon, lat = fid_od['raw']['lon'], fid_od['raw']['lat']
  nlon, nlat = lon.size, lat.size  # 360, 180
  
  # Get the x and y for pcolor plot, corners of the data points
  xpm, ypm = lf.ll_to_xy_for_map_pcolor(lon, lat, pm, reg)
  
  #
  # Plot the figure
  #
  # -------------
  # RAW | PI
  # -------------
  # MH  | MH_gsrd
  # -------------
  # 

  # Set colormap
  bounds = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1])  # colormap boundaries
  cmap_tmp = mpl.cm.autumn_r( np.linspace(0.0, 1.0, bounds.size-1) )  # start point of colormap 'Greens'
  # cmap_tmp1 = np.concatenate( ([[237.0/255.0, 201.0/255.0, 175.0/255.0, 1.0]], cmap_tmp), axis=0 )  # add some other colors to the colormap
  cmap = colors.ListedColormap(cmap_tmp)  # create colormap object
  norm = colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)  # create norm index for pcolormesh

  # Initiate figure and ax
  fg, ax = plt.subplots(2, 2, figsize=(12, 8), dpi=DPI)
  
  titles = ['RAW', 'PI', 'MH', 'MH_gsrd']
  for a, c, t in zip(ax.flatten(), od_list, titles):
    z = fid_od[c]['soilph'][2, :, :] + fid_od[c]['soilph'][3, :, :]
    zm = ma.array(z, mask=z==0)

    m = lf.plot_map(a, pm=pm, reg=reg)  # parallels=np.arange(-90, 91, 10.0), meridians=np.arange(-180.0, 181.0, 10.0) )
    h = m.pcolormesh(xpm, ypm, zm, norm=norm, cmap=cmap, zorder=2)
    
    # Set subtitles
    a.set_title(t, fontsize=30)
  
  # Set the colorbar for all
  fg.subplots_adjust(top=0.95, bottom=0.05, left=0.10, right=0.85, hspace=0.05)
  cbar_ax = fg.add_axes([0.88, 0.15, 0.02, 0.7])
  cbar = fg.colorbar(h, cax=cbar_ax, ticks=bounds)
  cbar.ax.tick_params(labelsize=18)
  cbar.set_label(label=r'soilph3+4', size=20)
  
  # save the figure
  fg.savefig('./figures/onlinedust_soilph34.png', dpi=DPI)


#==============================================================================#
# Plot vegetation cover
#==============================================================================#
def plot_vegetation_cover():
  # Parameters
  pm = 'cyl'  # Map projection
  reg = lf.reg_wafr
  mon = 2  # Feb
  imon = int(mon-1)  # index
  
  # Read data
  lu2018 = {}
  for c in lf.clist:
    lu2018[c] = np.load('data1_{0}.npz'.format(c))
  
  lon, lat = lu2018['pi']['lon_11'], lu2018['pi']['lat_11']
  
  # Get the x and y for pcolor plot, corners of the data points
  xpm, ypm = lf.ll_to_xy_for_map_pcolor(lon, lat, pm, reg)
  
  fg, ax = plt.subplots(3, 2, figsize=(12, 12), dpi=DPI)
  
  #===== pi =====#
  c = 'pi'
  irow = 0
  
  # annual mean total vegetation cover, the overlap not considered here
  cvall = np.mean(lu2018[c]['cvh_dom_avg_11'] + lu2018[c]['cvl_dom_avg_11'], axis=0)  
  
  ##### cvh
  m = lf.plot_map( ax[irow,0], pm, reg, parallels=np.arange(-90, 91, 10.0), meridians=np.arange(-180.0, 181.0, 10.0) )
  z = np.mean(lu2018[c]['cvh_dom_avg_11'], axis=0)
  zm = ma.array(z, mask= cvall<0.2)  # region where cvall<0.2 is considered as desert (or bare soil)
  
  # Set colormap
  bounds = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1])  # colormap boundaries
  cmap_tmp = mpl.cm.Greens( np.linspace(0.1, 1.0, bounds.size-1) )  # start point of colormap 'Greens'
  # cmap_tmp1 = np.concatenate( ([[237.0/255.0, 201.0/255.0, 175.0/255.0, 1.0]], cmap_tmp), axis=0 )  # add some other colors to the colormap
  cmap = colors.ListedColormap(cmap_tmp)  # create colormap object
  norm = colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)  # create norm index for pcolormesh
  
  # Plot
  h = m.pcolormesh(xpm, ypm, zm, norm=norm, cmap=cmap, zorder=3)
  
  # Set the colorbar
  # fg.colorbar(h, ax=ax[irow,0], extend='both', orientation='vertical', ticks=bounds)
  
  # Set the title
  ax[irow, 0].set_title('PI high vegetation')
  
  ##### cvl
  m = lf.plot_map( ax[irow,1], pm, reg, parallels=np.arange(-90, 91, 10.0), meridians=np.arange(-180.0, 181.0, 10.0) )
  z = np.mean(lu2018[c]['cvl_dom_avg_11'], axis=0)
  zm = ma.array(z, mask= cvall<0.2)  # region where cvall<0.2 is considered as desert (or bare soil)
  
  # Set colormap
  bounds = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1])  # colormap boundaries
  cmap_tmp = mpl.cm.Greens( np.linspace(0.1, 1.0, bounds.size-1) )  # start point of colormap 'Greens'
  # cmap_tmp1 = np.concatenate( ([[237.0/255.0, 201.0/255.0, 175.0/255.0, 1.0]], cmap_tmp), axis=0 )  # add some other colors to the colormap
  cmap = colors.ListedColormap(cmap_tmp)  # create colormap object
  norm = colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)  # create norm index for pcolormesh
  
  # Plot
  h = m.pcolormesh(xpm, ypm, zm, norm=norm, cmap=cmap, zorder=3)
  
  # Set the colorbar
  # fg.colorbar(h, ax=ax[irow,1], extend='both', orientation='vertical', ticks=bounds)
  
  # Set the title
  ax[irow, 1].set_title('PI low vegetation')
  
  
  #===== mh =====#
  c = 'mh'
  irow = 1
  
  # annual mean total vegetation cover, the overlap not considered here
  cvall = np.mean(lu2018[c]['cvh_dom_avg_11'] + lu2018[c]['cvl_dom_avg_11'], axis=0)  
  
  ##### cvh
  m = lf.plot_map( ax[irow,0], pm, reg, parallels=np.arange(-90, 91, 10.0), meridians=np.arange(-180.0, 181.0, 10.0) )
  z = np.mean(lu2018[c]['cvh_dom_avg_11'], axis=0)
  zm = ma.array(z, mask= cvall<0.2)  # region where cvall<0.2 is considered as desert (or bare soil)
  
  # Set colormap
  bounds = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1])  # colormap boundaries
  cmap_tmp = mpl.cm.Greens( np.linspace(0.1, 1.0, bounds.size-1) )  # start point of colormap 'Greens'
  # cmap_tmp1 = np.concatenate( ([[237.0/255.0, 201.0/255.0, 175.0/255.0, 1.0]], cmap_tmp), axis=0 )  # add some other colors to the colormap
  cmap = colors.ListedColormap(cmap_tmp)  # create colormap object
  norm = colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)  # create norm index for pcolormesh
  
  # Plot
  h = m.pcolormesh(xpm, ypm, zm, norm=norm, cmap=cmap, zorder=3)
  
  # Set the colorbar
  # fg.colorbar(h, ax=ax[irow,0], extend='both', orientation='vertical', ticks=bounds)
  
  # Set the title
  ax[irow, 0].set_title('MH high vegetation')
  
  ##### cvl
  m = lf.plot_map( ax[irow,1], pm, reg, parallels=np.arange(-90, 91, 10.0), meridians=np.arange(-180.0, 181.0, 10.0) )
  z = np.mean(lu2018[c]['cvl_dom_avg_11'], axis=0)
  zm = ma.array(z, mask= cvall<0.2)  # region where cvall<0.2 is considered as desert (or bare soil)
  
  # Set colormap
  bounds = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1])  # colormap boundaries
  cmap_tmp = mpl.cm.Greens( np.linspace(0.1, 1.0, bounds.size-1) )  # start point of colormap 'Greens'
  # cmap_tmp1 = np.concatenate( ([[237.0/255.0, 201.0/255.0, 175.0/255.0, 1.0]], cmap_tmp), axis=0 )  # add some other colors to the colormap
  cmap = colors.ListedColormap(cmap_tmp)  # create colormap object
  norm = colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)  # create norm index for pcolormesh
  
  # Plot
  h = m.pcolormesh(xpm, ypm, zm, norm=norm, cmap=cmap, zorder=3)
  
  # Set the colorbar
  # fg.colorbar(h, ax=ax[irow,1], extend='both', orientation='vertical', ticks=bounds)
  
  # Set the title
  ax[irow, 1].set_title('MH low vegetation')
  
  
  #===== mhgsrd =====#
  c = 'mg'
  irow = 2
  
  # annual mean total vegetation cover, the overlap not considered here
  cvall = np.mean(lu2018[c]['cvh_dom_avg_11'] + lu2018[c]['cvl_dom_avg_11'], axis=0)  
  
  ##### cvh
  m = lf.plot_map( ax[irow,0], pm, reg, parallels=np.arange(-90, 91, 10.0), meridians=np.arange(-180.0, 181.0, 10.0) )
  z = np.mean(lu2018[c]['cvh_dom_avg_11'], axis=0)
  zm = ma.array(z, mask= cvall<0.2)  # region where cvall<0.2 is considered as desert (or bare soil)
  
  # Set colormap
  bounds = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1])  # colormap boundaries
  cmap_tmp = mpl.cm.Greens( np.linspace(0.1, 1.0, bounds.size-1) )  # start point of colormap 'Greens'
  # cmap_tmp1 = np.concatenate( ([[237.0/255.0, 201.0/255.0, 175.0/255.0, 1.0]], cmap_tmp), axis=0 )  # add some other colors to the colormap
  cmap = colors.ListedColormap(cmap_tmp)  # create colormap object
  norm = colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)  # create norm index for pcolormesh
  
  # Plot
  h = m.pcolormesh(xpm, ypm, zm, norm=norm, cmap=cmap, zorder=3)
  
  # Set the colorbar
  # fg.colorbar(h, ax=ax[irow,0], extend='both', orientation='vertical', ticks=bounds)
  
  # Set the title
  ax[irow, 0].set_title('MH_gsrd high vegetation')
  
  ##### cvl
  m = lf.plot_map( ax[irow,1], pm, reg, parallels=np.arange(-90, 91, 10.0), meridians=np.arange(-180.0, 181.0, 10.0) )
  z = np.mean(lu2018[c]['cvl_dom_avg_11'], axis=0)
  zm = ma.array(z, mask= cvall<0.2)  # region where cvall<0.2 is considered as desert (or bare soil)
  
  # Set colormap
  bounds = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1])  # colormap boundaries
  cmap_tmp = mpl.cm.Greens( np.linspace(0.1, 1.0, bounds.size-1) )  # start point of colormap 'Greens'
  # cmap_tmp1 = np.concatenate( ([[237.0/255.0, 201.0/255.0, 175.0/255.0, 1.0]], cmap_tmp), axis=0 )  # add some other colors to the colormap
  cmap = colors.ListedColormap(cmap_tmp)  # create colormap object
  norm = colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)  # create norm index for pcolormesh
  
  # Plot
  h = m.pcolormesh(xpm, ypm, zm, norm=norm, cmap=cmap, zorder=3)
  
  # Set the colorbar
  # fg.colorbar(h, ax=ax[irow,1], extend='both', orientation='vertical', ticks=bounds)
  
  # Set the title
  ax[irow, 1].set_title('MH_gsrd low vegetation')
  
  # Set the colorbar for all
  fg.subplots_adjust(top=0.95, bottom=0.05, left=0.05, right=0.85)
  cbar_ax = fg.add_axes([0.88, 0.15, 0.02, 0.7])
  cbar = fg.colorbar(h, cax=cbar_ax, extend='both', ticks=bounds)
  cbar.ax.tick_params(labelsize=16)
  
  # save the figure
  # fg.subplots_adjust(hspace=0.2, wspace=0.2)
  # fg.tight_layout()
  fg.savefig('./figures/poster_cvh_cvl.png', dpi=DPI)



#==============================================================================#
# Plot dust load
#==============================================================================#
def plot_dust_load(fid_dl):
  # Dimensions, the same for different cases
  lon120 = fid_dl['pi'].variables['lon'][:]
  lat90  = fid_dl['pi'].variables['lat'][:]
  
  nlon120 = lon120.size
  nlat90  = lat90.size
  
  # Dust load
  loaddust = {}
  for c in lf.clist:
    loaddust[c] = np.squeeze(fid_dl[c].variables['loaddust'][:])*1.0e3  # [g m-2], [90, 120] after squeeze
    
  #
  # Show some information
  #

  # Region mask for west Africa to calculate the difference
  comp_reg_wafr = [-10, 20, 5, 20]
  regm_lon = (lon120>=comp_reg_wafr[0]) & (lon120<=comp_reg_wafr[1])
  regm_lat = (lat90>=comp_reg_wafr[2]) & (lat90<=comp_reg_wafr[3])
  
  # Total dustload in [g m-2] within the region reg_wafr
  total_loaddust_wafr_pi = np.sum(loaddust['pi'][np.ix_(regm_lat, regm_lon)])
  total_loaddust_wafr_mg = np.sum(loaddust['mg'][np.ix_(regm_lat, regm_lon)])
  rel_total_loaddust_wafr = (total_loaddust_wafr_mg - total_loaddust_wafr_pi) / total_loaddust_wafr_pi
  # diff_mhgsrd_pi = loaddust['mhgsrd'] - loaddust['pi']
  # abs_diff_wafr = np.sum(diff_mhgsrd_pi[np.ix_(regm_lat, regm_lon)])
  # rel_diff_wafr = np.sum(loaddust['mhgsrd'][np.ix_(regm_lat, regm_lon)]) - np.sum(loaddust['pi'][np.ix_(regm_lat, regm_lon)])
  print('Relative total dust load change: ', rel_total_loaddust_wafr)  # -0.3498154 ~ -35%
  
  # Set colormap
  bounds = np.array([0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5])  # colormap boundaries
  cmap_tmp = mpl.cm.autumn_r( np.linspace(0.1, 1.0, bounds.size-1) )  # start point of colormap 'Greens'
  cmap = colors.ListedColormap(cmap_tmp)  # create colormap object
  norm = colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)  # create norm index for pcolormesh

  # cm = plt.get_cmap('Wistia')
  # cm = plt.get_cmap('autumn_r')
  # cm = plt.get_cmap('YlOrBr')
  # cm = plt.get_cmap('default')
  # cm_diff = plt.get_cmap('BrBG_r')
  vmin, vmax = 0.1, 1.6
  vmin_diff, vmax_diff = -0.04, 0.04
  ticks_diff = [-0.04, -0.03, -0.02, -0.01, 0, 0.01, 0.02, 0.03, 0.04]
  eps = vmin
  eps_diff = 5.0e-4
  alpha = 0.7
  pm = 'cyl'
  # plot_reg_nafr = (-5, 40, -30, 50)
  plot_reg_nafr = lf.reg_wafr

  xpm, ypm = lf.ll_to_xy_for_map_pcolor(lon120, lat90, pm, plot_reg_nafr)
  
  # Initiate figure
  fg, ax = plt.subplots(3, 1, figsize=(16, 24), dpi=DPI)
  
  # Plot dataset in subplots
  titles = ['PI', 'MH', 'MH_gsrd']
  for a, c, t in zip(ax.flatten(), lf.clist, titles):
    z = loaddust[c]
    zm = ma.array(z, mask=z<bounds[0])

    m = lf.plot_map(a, pm=pm, reg=plot_reg_nafr, parallels=np.arange(-90, 91, 10.0), meridians=np.arange(-180.0, 181.0, 10.0) )
    h = m.pcolormesh(xpm, ypm, zm, norm=norm, cmap=cmap, zorder=2, alpha=alpha)
    
    # Set subtitles
    a.set_title(t, fontsize=30)

  # Add one colorbar for all
  # fg.subplots_adjust(left=0.05, right=0.85, bottom=0.1, top=0.9, wspace=0.1, hspace=0.01)
  fg.subplots_adjust(left=0.05, right=0.85, bottom=0.05, top=0.95)
  cax = fg.add_axes([0.88, 0.25, 0.02, 0.5])
  cb = fg.colorbar(h, cax=cax, ticks=bounds)
  cb.ax.tick_params(labelsize=20)
  cb.set_label(label=r'Dust load [g m$^{-2}$]', size=20)

  # Set figure title
  # fg.suptitle('{0:s}'.format('loaddust [g m-2]'), fontsize=20)

  # Save the figure
  fg.savefig('{0:s}{1:s}.png'.format('./figures/', 'loaddust_pi_mh_mhgsrd'), dpi=DPI)


#==============================================================================#
# Start main code
#==============================================================================#
#
# Print some information
#


#
# Read the data
#
fid_od = read_onlinedust_data()
fid_dl = read_dustload_data()


#
# Plot
#

# print('Plotting potsrc ...')
# plot_potsrc(fid_od)

print('Plotting soilph3+4 ...')
plot_soilph34(fid_od)

# print('Plotting dust load ...')
# plot_dust_load(fid_dl)
