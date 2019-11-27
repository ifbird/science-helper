import os
import sys
sys.path.insert(0, '/home/pzzhou/Scripts/repos/science-helper/process_data')
sys.path.insert(0, '/home/pzzhou/Scripts/repos/science-helper/pypack')

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colorbar, colors

from netCDF4 import Dataset

from cartopy import config
import cartopy.crs as ccrs

import lu2018
import tools

from local import *

#======================================================#
# help
#======================================================#


levels_default = 10  # 10 level heights
cmap_default = plt.get_cmap('viridis')
ax_title_prefix = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)']

fname_tm5_grid_area = get_fname_tm5_grid_area()
print(fname_tm5_grid_area)
fid_tm5_grid_area = Dataset(fname_tm5_grid_area, 'r')
tm5_grid_area = fid_tm5_grid_area.variables['cell_area'][:]


def set_limit_to_nan(data, limits):
  data[ (data >= limits[0]) & (data <= limits[1]) ] = np.nan


def plot_base_3x2_5(fname, x, y, data_list, \
  levels=[levels_default]*5, \
  cmap=[cmap_default]*5, \
  ax_title=['']*5, \
  cb_label=None \
  ):

  # Create figure
  marlft=0.05
  marrgt=0.95
  martop=0.95
  marbot=0.20
  marwsp=0.05
  marhsp=0.05

  fg = plt.figure(figsize=(16, 12))

  fg.subplots_adjust(left  = marlft,  bottom = marbot, \
                     right = marrgt,  top    = martop, \
                     wspace= marwsp,  hspace = marhsp )

  # Create 2x2 axes with map projection and contourf plot
  ax = [None]*5

  for i in range(5):
    ax[i] = plt.subplot(3, 2, i+1, projection=ccrs.PlateCarree())
    ax[i].coastlines()
    ax[i].set_global()
    hc = ax[i].contourf(x, y, data_list[i], levels=levels[i], transform=ccrs.PlateCarree(), cmap=cmap[i], extend='both')

    # colorbar
    cbar = fg.colorbar(hc, ax=ax[i], label=cb_label)  # , ticks=levels[i])

    ax[i].set_title(ax_title_prefix[i] + ' ' + ax_title[i], fontsize=18)

  # fg.tight_layout()
  fg.savefig(fname, bbox_inches="tight", dpi=fg.dpi)


levels_default = 10  # 10 level heights
cmap_default = plt.get_cmap('viridis')
def plot_base_2x3(fname, x, y, data_list, \
  levels=[levels_default]*6, cmap=[cmap_default]*6, cb_label=None):

  # Create figure
  marlft=0.05
  marrgt=0.95
  martop=0.95
  marbot=0.20
  marwsp=0.05
  marhsp=0.12

  fg = plt.figure(figsize=(16, 10))

  fg.subplots_adjust(left  = marlft,  bottom = marbot, \
                     right = marrgt,  top    = martop, \
                     wspace= marwsp,  hspace = marhsp )

  # Create 3x1 axes with map projection and contourf plot
  ax_title = ['(a) Lu2018 pi', '(b) pio', '(c) pic', '(d) piz', '(e) mh1', '(f) mh2']
  ax = [None]*6

  for i in range(6):
    print(i)
    ax[i] = plt.subplot(2, 3, i+1, projection=ccrs.PlateCarree())
    ax[i].coastlines()
    ax[i].set_global()
    hc = ax[i].contourf(x, y, data_list[i], levels=levels[i], transform=ccrs.PlateCarree(), cmap=cmap[i], extend='both')

    # cmap, norm = matplotlib.colors.from_levels_and_colors(levels, colors, extend='both')
    cbar = fg.colorbar(hc, ax=ax[i], label=cb_label)  # , ticks=levels[i])

    ax[i].set_title(ax_title[i], fontsize=18)

  # fg.tight_layout()
  fg.savefig(fname, bbox_inches="tight", dpi=fg.dpi)


def plot_base_2x3_5(fname, x, y, data_list, \
  levels=[levels_default]*5, \
  cmap=[cmap_default]*5, \
  ax_title=['']*5, \
  cb_label=None \
  ):

  # Create figure
  marlft=0.05
  marrgt=0.95
  martop=0.95
  marbot=0.20
  marwsp=0.05
  marhsp=0.12

  fg = plt.figure(figsize=(16, 10))

  fg.subplots_adjust(left  = marlft,  bottom = marbot, \
                     right = marrgt,  top    = martop, \
                     wspace= marwsp,  hspace = marhsp )

  # Create 2x3 axes with map projection and contourf plot
  # ax_title = ['(a) pio', '(b) pic', '(c) piz', '(d) mh1', '(e) mh2']
  ax = [None]*5

  for i in range(5):
    print(i)
    ax[i] = plt.subplot(2, 3, i+1, projection=ccrs.PlateCarree())
    ax[i].coastlines()
    ax[i].set_global()
    hc = ax[i].contourf(x, y, data_list[i], levels=levels[i], transform=ccrs.PlateCarree(), cmap=cmap[i], extend='both')

    # cmap, norm = matplotlib.colors.from_levels_and_colors(levels, colors, extend='both')
    cbar = fg.colorbar(hc, ax=ax[i], label=cb_label)  # , ticks=levels[i])

    ax[i].set_title(ax_title_prefix[i] + ' ' + ax_title[i], fontsize=18)

  # fg.tight_layout()
  fg.savefig(fname, bbox_inches="tight", dpi=fg.dpi)


def plot_base_2x2(fname, x, y, data_list, \
  levels=[levels_default]*4, \
  cmap=[cmap_default]*4, \
  ax_title=['']*4, \
  cb_label=None \
  ):

  # Create figure
  marlft=0.05
  marrgt=0.95
  martop=0.95
  marbot=0.20
  marwsp=0.05
  marhsp=0.05

  fg = plt.figure(figsize=(16, 10))

  fg.subplots_adjust(left  = marlft,  bottom = marbot, \
                     right = marrgt,  top    = martop, \
                     wspace= marwsp,  hspace = marhsp )

  # Create 2x2 axes with map projection and contourf plot
  ax = [None]*4

  for i in range(4):
    print(i)
    ax[i] = plt.subplot(2, 2, i+1, projection=ccrs.PlateCarree())
    ax[i].coastlines()
    ax[i].set_global()
    hc = ax[i].contourf(x, y, data_list[i], levels=levels[i], transform=ccrs.PlateCarree(), cmap=cmap[i], extend='both')

    # colorbar
    cbar = fg.colorbar(hc, ax=ax[i], label=cb_label)  # , ticks=levels[i])

    ax[i].set_title(ax_title_prefix[i] + ' ' + ax_title[i], fontsize=18)

  # fg.tight_layout()
  fg.savefig(fname, bbox_inches="tight", dpi=fg.dpi)


def plot_base_3x1(fname, x, y, data_list, \
  ax_title = ['pio', 'mh2', 'mh2 - pio'], \
  levels=[levels_default]*3, cmap=[cmap_default]*3, cb_label=None, map_extent=None):

  # Create figure
  marlft=0.05
  marrgt=0.95
  martop=0.95
  marbot=0.20
  marwsp=0.05
  marhsp=0.22

  fg = plt.figure(figsize=(8, 12))

  fg.subplots_adjust(left  = marlft,  bottom = marbot, \
                     right = marrgt,  top    = martop, \
                     wspace= marwsp,  hspace = marhsp )

  # Create 3x1 axes with map projection and contourf plot
  ax = [None]*3

  for i in range(3):
    ax[i] = plt.subplot(3, 1, i+1, projection=ccrs.PlateCarree())
    ax[i].coastlines()
    if map_extent is None:
      ax[i].set_global()
    else:
      ax[i].set_extent(map_extent, crs=ccrs.PlateCarree())
    gl = ax[i].gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False

    # divnorm = colors.DivergingNorm(vmin=levels[i][0], vcenter=0.5*(levels[i][0]+levels[i][-1]), vmax=levels[i][-1])
    # cnorm = plt.Normalize(vmin=levels[i][0],vmax=levels[i][-1])
    # levels = [-32, -16,-8, -4, -2, 0, 2, 4, 8, 16, 32]
    if not np.isscalar(levels[i]):
      norm = mpl.colors.BoundaryNorm(boundaries=levels[i], ncolors=256)  # len(levels[i])-1)
    cmap_tmp = cmap[i]
    if i<2:
      cmap_tmp.set_under('white')
    hc = ax[i].contourf(x, y, data_list[i], levels=levels[i], transform=ccrs.PlateCarree(), cmap=cmap_tmp, norm=norm, extend='both')
    # hc = ax[i].contourf(x, y, data_list[i], transform=ccrs.PlateCarree(), cmap=cmap[i], extend='both')
    # print(levels[i][0], levels[i][-1])
    # hc = ax[i].pcolormesh(x, y, data_list[i], vmin=levels[i][0], vmax=levels[i][-1], transform=ccrs.PlateCarree(), cmap=cmap[i])

    # Plot colorbar
    # bounds = levels[i]
    # norm = mpl.colors.BoundaryNorm(bounds, cmap[i].N)
    # cbar = mpl.colorbar.ColorbarBase( \
    #   ax[i], cmap=cmap[i], \
    #   norm=norm, \
    #   boundaries=bounds, \
      # extend='both',
      # extendfrac='auto',
      # ticks=bounds,
      # spacing='uniform',
      # orientation='horizontal' \
   #  )
    # cbar.set_label(cb_label, fontsize=18)
    # cbar_ax = fg.add_axes(bar_pos)
    # cbar = fg.colorbar(ax[3], cax=cbar_ax)
    # cbar.ax.tick_params(labelsize=12)
    # cbar.set_label('elevation (m)', fontsize=12)
    # cbar = fg.colorbar(hc, ax=ax[i], label=cb_label, norm=norm, cmap=cmap)
    # cnorm = plt.Normalize(vmin=levels[i][0],vmax=levels[i][-1])
    # clevels = levels[i]
    # colors=plt.cm.RdYlBu(cnorm(clevels))

    # cmap, norm = matplotlib.colors.from_levels_and_colors(levels, colors, extend='both')
    cbar = fg.colorbar(hc, ax=ax[i], label=cb_label)  # , ticks=levels[i])
    # cbar.set_clim(levels[i][0], levels[i][-1])

    ax[i].set_title(ax_title_prefix[i] + ' ' + ax_title[i], fontsize=18)

  # Set colorbar
  ## bar_pos = [0.05, 0.12, 0.9, 0.07]  # [left,bottom,width,height]
  ## bar_orientation = "horizontal"     # or "vertical"  or "none" (to skip)
  ## bar_ticklen  = 0
  ## bar_ticklabs = None    # Use defaults
  ## bar_label    = u"data"
  ## 
  ## bar_axes = fg.add_axes(bar_pos)
  ## cbar = colorbar.ColorbarBase(bar_axes, \
  ##   orientation=bar_orientation, \
  ##   # cmap=plt.get_cmap('coolwarm'),
  ##   norm=colors.Normalize(vmin=0.0, vmax=1.0)) # set min, max of colorbar
  ## cbar.set_clim(0.0, 1.0) # set limits of color map

  # Set colorbar
  # cbar_ax = fg.add_axes(bar_pos)
  # cbar = fg.colorbar(ax[3], cax=cbar_ax)
  # cbar.ax.tick_params(labelsize=12)
  # cbar.set_label('elevation (m)', fontsize=12)
  
  # fg.tight_layout()
  fg.savefig(fname, bbox_inches="tight", dpi=fg.dpi)


def plot_vegetation_tm52009_Lu2018(month_range):
  #
  # Read veg data and calculate the average value for the second half year
  #
  cvl = {}
  cvh = {}
  m0 = month_range[0]
  m1 = month_range[1]
  nmonth = m1 - m0 + 1

  ##### Lu2018 raw data
  fname_lu2018_veg_lrg = get_fname_lu2018_veg_raw('pi')

  data_lu2018_veg_lrg = lu2018.Lu2018(fname_lu2018_veg_lrg)
  lon_lu2018 = data_lu2018_veg_lrg.data_lrg['lon']
  lat_lu2018 = data_lu2018_veg_lrg.data_lrg['lat']
  cvl['lu2018_pi'] = np.nanmean(data_lu2018_veg_lrg.data_lrg['cvl'][-1, :, :], axis=0)  # [year, mon, grid]
  cvh['lu2018_pi'] = np.nanmean(data_lu2018_veg_lrg.data_lrg['cvh'][-1, :, :], axis=0)

  ##### pio
  fname_input_veg_pio = get_fname_input_veg_sample('2009')
  fid_input_veg_pio = Dataset(fname_input_veg_pio, 'r')

  # Avg from month m0 to m1 --> [lat, lon]
  cvl['pio'] = np.mean(fid_input_veg_pio.variables['cvl'][(m0-1):m1, :, :], axis=0)
  cvh['pio'] = np.mean(fid_input_veg_pio.variables['cvh'][(m0-1):m1, :, :], axis=0)
  set_limit_to_nan(cvl['pio'], [0.0, 0.0])
  set_limit_to_nan(cvh['pio'], [0.0, 0.0])

  ##### pic, piz, mh1, mh2
  for c in ['pic', 'piz', 'mh1', 'mh2']:
    print('case: ', c)
    first_loop = True
    for im in range(m0, m1+1):
      print('month: ', im)
      m_str = '{:02d}'.format(im)
      fname_input_veg = get_fname_input_veg(c, '1859', m_str)
      fid_input_veg = Dataset(fname_input_veg, 'r')
      if first_loop:
        lon = fid_input_veg.variables['lon'][:]
        lat = fid_input_veg.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        cvl[c] = np.zeros( (nlat, nlon) )
        cvh[c] = np.zeros( (nlat, nlon) )
        first_loop = False
      cvl[c] += fid_input_veg.variables['cvl'][0, :, :]
      cvh[c] += fid_input_veg.variables['cvh'][0, :, :]
      
      fid_input_veg.close()
    cvl[c] = cvl[c] / nmonth
    cvh[c] = cvh[c] / nmonth
    set_limit_to_nan(cvl[c], [0.0, 0.0])
    set_limit_to_nan(cvh[c], [0.0, 0.0])
    tools.show_statistics(cvl[c])
    tools.show_statistics(cvh[c])

  # Plot and save the figure
  # plot_base_2x3_5( 'figures/cvl_5case.png', lon, lat, \
  #   [cvl['pio'], cvl['pic'], cvl['piz'], cvl['mh1'], cvl['mh2']], \
  #   levels = [ np.arange(0.0, 1.1, 0.1), np.arange(0.0, 1.1, 0.1), np.arange(0.0, 1.1, 0.1), np.arange(0.0, 1.1, 0.1), np.arange(0.0, 1.1, 0.1) ], \
  #   cmap = [cmap_default, cmap_default, cmap_default, cmap_default, cmap_default], \
  #   cb_label=r'cvl [-]', \
  #   )

  plot_base_2x2( 'figures/cvl-2009_pi_mh1_mh2.png', lon, lat, \
    [cvl['pio'], cvl['pic'], cvl['mh1'], cvl['mh2']], \
    levels = [ np.arange(0.0, 1.1, 0.1), np.arange(0.0, 1.1, 0.1), np.arange(0.0, 1.1, 0.1), np.arange(0.0, 1.1, 0.1), np.arange(0.0, 1.1, 0.1) ], \
    cmap = [cmap_default, cmap_default, cmap_default, cmap_default], \
    ax_title = ['TM5 2009', 'Lu2018 Pi', 'Lu2018 MH', 'Lu2018 MHgsrd'], \
    cb_label=r'cvl [-]', \
    )

  plot_base_2x2( 'figures/cvh-2009_pi_mh1_mh2.png', lon, lat, \
    [cvh['pio'], cvh['pic'], cvh['mh1'], cvh['mh2']], \
    levels = [ np.arange(0.0, 1.1, 0.1), np.arange(0.0, 1.1, 0.1), np.arange(0.0, 1.1, 0.1), np.arange(0.0, 1.1, 0.1), np.arange(0.0, 1.1, 0.1) ], \
    cmap = [cmap_default, cmap_default, cmap_default, cmap_default], \
    ax_title = ['TM5 2009', 'Lu2018 Pi', 'Lu2018 MH', 'Lu2018 MHgsrd'], \
    cb_label=r'cvh [-]', \
    )

  # plot_base_2x2( 'figures/cvl.png', lon, lat, [cvl['pio'], cvl['pic'], cvl['mh1'], cvl['mh2']], \
  #   levels=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
  # plot_base_2x2( 'figures/cvh.png', lon, lat, [cvh['pio'], cvh['pic'], cvh['mh1'], cvh['mh2']], \
  #   levels=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )


def plot_vegetation_Lu2018_lrg_gxx():
  case_list = ['pi', 'mh1', 'mh2']
  ##### Lu2018 data in lrg grid
  fname_lu2018_veg_lrg = {}
  data_lu2018_veg_lrg = {}

  # Read dataset
  for c in case_list:
    fname_lu2018_veg_lrg[c] = get_fname_lu2018_veg_raw(c)
    data_lu2018_veg_lrg[c] = lu2018.Lu2018(fname_lu2018_veg_lrg[c])

  # lon and lat
  lon_lrg = data_lu2018_veg_lrg['pi'].data_lrg['lon']
  lat_lrg = data_lu2018_veg_lrg['pi'].data_lrg['lat']

  # Annual mean cvl and cvh in the last year
  cvl_lrg = {}
  cvh_lrg = {}
  for c in case_list:
    cvl_lrg[c] = np.nanmean(data_lu2018_veg_lrg[c].data_lrg['cvl'][-1, :, :], axis=0)  # [year, mon, grid]
    cvh_lrg[c] = np.nanmean(data_lu2018_veg_lrg[c].data_lrg['cvh'][-1, :, :], axis=0)

    set_limit_to_nan(cvl_lrg[c], [0.0, 0.0])
    set_limit_to_nan(cvh_lrg[c], [0.0, 0.0])

  ##### Lu2018 data in gxx grid
  m0 = 1
  m1 = 12
  nmonth = m1 - m0 + 1
  cvl_gxx = {}
  cvh_gxx = {}
  for c in ['pic', 'mh1', 'mh2']:
    first_loop = True
    for im in range(m0, m1+1):
      m_str = '{:02d}'.format(im)
      fname_input_veg = get_fname_input_veg(c, '1859', m_str)
      fid_input_veg = Dataset(fname_input_veg, 'r')
      if first_loop:
        lon_gxx = fid_input_veg.variables['lon'][:]
        lat_gxx = fid_input_veg.variables['lat'][:]
        nlon = len(lon_gxx)
        nlat = len(lat_gxx)
        cvl_gxx[c] = np.zeros( (nlat, nlon) )
        cvh_gxx[c] = np.zeros( (nlat, nlon) )
        first_loop = False
      cvl_gxx[c] += fid_input_veg.variables['cvl'][0, :, :]
      cvh_gxx[c] += fid_input_veg.variables['cvh'][0, :, :]
      
      # Close the file
      fid_input_veg.close()

    # Calculate the annual average
    cvl_gxx[c] = cvl_gxx[c] / nmonth
    cvh_gxx[c] = cvh_gxx[c] / nmonth
    set_limit_to_nan(cvl_gxx[c], [0.0, 0.0])
    set_limit_to_nan(cvh_gxx[c], [0.0, 0.0])

  ##### Plot the figures
  # Parameters
  cmap = [cmap_default, cmap_default, cmap_default, cmap_default, cmap_default, cmap_default]
  levels = [ \
    np.arange(0.0, 1.1, 0.1), np.arange(0.0, 1.1, 0.1), \
    np.arange(0.0, 1.1, 0.1), np.arange(0.0, 1.1, 0.1), \
    np.arange(0.0, 1.1, 0.1), np.arange(0.0, 1.1, 0.1), \
    ]
  marlft=0.05
  marrgt=0.95
  martop=0.95
  marbot=0.20
  marwsp=0.05
  marhsp=0.12

  vmin, vmax = 0.0, 1.0

  #
  # cvl
  #

  cb_label = 'cvl [-]'
  fname = 'figures/cvl-Lu2018_lrg_gxx.png'
  fg = plt.figure(figsize=(16, 12))

  fg.subplots_adjust(left  = marlft,  bottom = marbot, \
                     right = marrgt,  top    = martop, \
                     wspace= marwsp,  hspace = marhsp )

  # Create 3x1 axes with map projection and contourf plot
  ax_title = ['(a) pi lrg', '(b) pi gxx', '(c) mh1 lrg', '(d) mh1 gxx', '(e) mh2 lrg', '(f) mh2 gxx']
  ax = [None]*6
  hc = [None]*6

  for i in range(6):
    ax[i] = plt.subplot(3, 2, i+1, projection=ccrs.PlateCarree())
    ax[i].coastlines()
    ax[i].set_global()
    
  # Left column: lrg
  i = 0
  hc[i] = ax[i].scatter(lon_lrg, lat_lrg, c=cvl_lrg['pi'], s=2.0, vmin=vmin, vmax=vmax, cmap=cmap[i])

  i = 2
  hc[i] = ax[i].scatter(lon_lrg, lat_lrg, c=cvl_lrg['mh1'], s=2.0, vmin=vmin, vmax=vmax, cmap=cmap[i])

  i = 4
  hc[i] = ax[i].scatter(lon_lrg, lat_lrg, c=cvl_lrg['mh2'], s=2.0, vmin=vmin, vmax=vmax, cmap=cmap[i])

  # Right column: gxx
  i = 1
  hc[i] = ax[i].contourf(lon_gxx, lat_gxx, cvl_gxx['pic'], levels=levels[i], \
    transform=ccrs.PlateCarree(), cmap=cmap[i])
  i = 3
  hc[i] = ax[i].contourf(lon_gxx, lat_gxx, cvl_gxx['mh1'], levels=levels[i], \
    transform=ccrs.PlateCarree(), cmap=cmap[i])
  i = 5
  hc[i] = ax[i].contourf(lon_gxx, lat_gxx, cvl_gxx['mh2'], levels=levels[i], \
    transform=ccrs.PlateCarree(), cmap=cmap[i])

  for i in range(6):
    cbar = fg.colorbar(hc[i], ax=ax[i], label=cb_label)
    ax[i].set_title(ax_title[i], fontsize=18)

  # fg.tight_layout()
  fg.savefig(fname, bbox_inches="tight", dpi=fg.dpi)

  #
  # cvh
  #

  cb_label = 'cvh [-]'
  fname = 'figures/cvh-Lu2018_lrg_gxx.png'
  fg = plt.figure(figsize=(16, 12))

  fg.subplots_adjust(left  = marlft,  bottom = marbot, \
                     right = marrgt,  top    = martop, \
                     wspace= marwsp,  hspace = marhsp )

  # Create 3x1 axes with map projection and contourf plot
  ax_title = ['(a) pi lrg', '(b) pi gxx', '(c) mh1 lrg', '(d) mh1 gxx', '(e) mh2 lrg', '(f) mh2 gxx']
  ax = [None]*6
  hc = [None]*6

  for i in range(6):
    ax[i] = plt.subplot(3, 2, i+1, projection=ccrs.PlateCarree())
    ax[i].coastlines()
    ax[i].set_global()
    
  # Left column: lrg
  i = 0
  hc[i] = ax[i].scatter(lon_lrg, lat_lrg, c=cvh_lrg['pi'], s=2.0, vmin=vmin, vmax=vmax, cmap=cmap[i])

  i = 2
  hc[i] = ax[i].scatter(lon_lrg, lat_lrg, c=cvh_lrg['mh1'], s=2.0, vmin=vmin, vmax=vmax, cmap=cmap[i])

  i = 4
  hc[i] = ax[i].scatter(lon_lrg, lat_lrg, c=cvh_lrg['mh2'], s=2.0, vmin=vmin, vmax=vmax, cmap=cmap[i])

  # Right column: gxx
  i = 1
  hc[i] = ax[i].contourf(lon_gxx, lat_gxx, cvh_gxx['pic'], levels=levels[i], \
    transform=ccrs.PlateCarree(), cmap=cmap[i])
  i = 3
  hc[i] = ax[i].contourf(lon_gxx, lat_gxx, cvh_gxx['mh1'], levels=levels[i], \
    transform=ccrs.PlateCarree(), cmap=cmap[i])
  i = 5
  hc[i] = ax[i].contourf(lon_gxx, lat_gxx, cvh_gxx['mh2'], levels=levels[i], \
    transform=ccrs.PlateCarree(), cmap=cmap[i])

  for i in range(6):
    cbar = fg.colorbar(hc[i], ax=ax[i], label=cb_label)
    ax[i].set_title(ax_title[i], fontsize=18)

  # fg.tight_layout()
  fg.savefig(fname, bbox_inches="tight", dpi=fg.dpi)



def plot_onlinedust():
  pass


def plot_iso_emission_tm52009_Lu2018():
  data = {}
  for c in ['pio', 'pic', 'mh1', 'mh2']:
    # File name
    fname_input = get_fname_input_iso(c, '1859')

    # File id
    fid_input = Dataset(fname_input, 'r')

    # Data
    data[c] = np.mean(fid_input.variables['MEGAN_MACC'], axis=0) * 1.0e9  # [kg m-2 s-1] --> [ug m-2 s-1]
    set_limit_to_nan(data[c], [0, 1.0e-3])

    # lon and lat
    lon = fid_input.variables['lon'][:]
    lat = fid_input.variables['lat'][:]

  plot_base_2x2( 'figures/iso_emiss-2009_pi_mh1_mh2.png', lon, lat, \
    [data['pio'], data['pic'], data['mh1'], data['mh2']], \
    levels = [ np.arange(0.0, 0.9, 0.1), np.arange(0.0, 0.9, 0.1), np.arange(0.0, 0.9, 0.1), np.arange(0.0, 0.9, 0.1)], \
    cmap = [cmap_default, cmap_default, cmap_default, cmap_default], \
    ax_title = ['TM5 2009', 'Lu2018 PI', 'Lu2018 MH', 'Lu2018 MHgsrd'], \
    cb_label=r'isoprene emission [$\mu$g m$^{-2}$ s$^{-1}$]', \
    )


def plot_iso_emission_tm52009_mh2():
  data = {}
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    fname_input = get_fname_input_iso(c, '1859')
    fid_input = Dataset(fname_input, 'r')
    data[c] = np.mean(fid_input.variables['MEGAN_MACC'], axis=0) * 1.0e9  # [kg m-2 s-1] --> [ug m-2 s-1]
    lon = fid_input.variables['lon'][:]
    lat = fid_input.variables['lat'][:]
  data_diff = data['mh2'] - data[pi_case]

  # set limit to nan
  for c in [pi_case, 'mh2']:
    set_limit_to_nan(data[c], [0, 1.0e-3])
  set_limit_to_nan(data_diff, [-1.0e-3, 1.0e-3])

  plot_base_3x1( 'figures/iso.png', lon, lat, [data[pi_case], data['mh2'], data_diff], \
    levels = [ np.arange(0.0, 0.9, 0.1), np.arange(0.0, 0.9, 0.1), np.arange(-0.8, 0.9, 0.2) ], \
    cmap = [cmap_default, cmap_default, plt.get_cmap('RdBu_r')], \
    cb_label=r'isoprene emission [$\mu$g m$^{-2}$ s$^{-1}$]', \
    )


def plot_mon_emission_tm52009_Lu2018():
  data = {}
  for c in ['pio', 'pic', 'mh1', 'mh2']:
    # File name
    fname_input = get_fname_input_mon(c, '1859')

    # File id
    fid_input = Dataset(fname_input, 'r')

    # Data
    data[c] = np.mean(fid_input.variables['MEGAN_MACC'], axis=0) * 1.0e9  # [kg m-2 s-1] --> [ug m-2 s-1]
    set_limit_to_nan(data[c], [0, 1.0e-3])

    # lon and lat
    lon = fid_input.variables['lon'][:]
    lat = fid_input.variables['lat'][:]

  plot_base_2x2( 'figures/mon_emiss-2009_pi_mh1_mh2.png', lon, lat, \
    [data['pio'], data['pic'], data['mh1'], data['mh2']], \
    levels = [ np.arange(0.0, 0.09, 0.01), np.arange(0.0, 0.09, 0.01), np.arange(0.0, 0.09, 0.01), np.arange(0.0, 0.09, 0.01)], \
    cmap = [cmap_default, cmap_default, cmap_default, cmap_default], \
    ax_title = ['TM5 2009', 'Lu2018 PI', 'Lu2018 MH', 'Lu2018 MHgsrd'], \
    cb_label=r'monoterpenes emission [$\mu$g m$^{-2}$ s$^{-1}$]', \
    )


def plot_mon_emission_tm52009_mh2():
  data = {}
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    fname_input = get_fname_input_mon(c, '1859')
    fid_input = Dataset(fname_input, 'r')
    data[c] = np.mean(fid_input.variables['MEGAN_MACC'], axis=0) * 1.0e9  # [kg m-2 s-1] --> [ug m-2 s-1]
    lon = fid_input.variables['lon'][:]
    lat = fid_input.variables['lat'][:]
  data_diff = data['mh2'] - data[pi_case]

  for c in [pi_case, 'mh2']:
    set_limit_to_nan(data[c], [0, 1.0e-4])
  set_limit_to_nan(data_diff, [-1.0e-4, 1.0e-4])

  plot_base_3x1( 'figures/mon.png', lon, lat, [data[pi_case], data['mh2'], data_diff], \
    levels = [ np.arange(0.0, 0.09, 0.01), np.arange(0.0, 0.09, 0.01), np.arange(-0.05, 0.06, 0.01) ], \
    cmap = [cmap_default, cmap_default, plt.get_cmap('RdBu_r')], \
    cb_label=r'monoterpene emission [$\mu$g m$^{-2}$ s$^{-1}$]', \
    )


def plot_loaddust_5case():
  case_list_5case = ['pio', 'pic', 'piz', 'mh1', 'mh2']
  m0 = 1
  m1 = 12
  nmonth = m1 - m0 + 1
  data = {}
  for c in case_list_5case:
    first_loop = True
    for m in range(m0, m1+1):
      # month index: 0 - 11
      im = m - 1
      m_str = '{:02d}'.format(m)

      fname_output = get_fname_output(c, '1y', 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')

      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False

      data[c] += fid_output.variables['loaddust'][0, :, :] * 1.0e6  # [kg m-2] --> [mg m-2]

    data[c] /= nmonth

  # dust load
  plot_base_3x2_5( 'figures/loaddust_am-5case.png', lon, lat, \
    [data['pio'], data['pic'], data['piz'], data['mh1'], data['mh2']], \
    levels = [ np.arange(0, 440, 40)] * 5, \
    cmap=[cmap_default]*5, \
    ax_title=['pio', 'pic', 'piz', 'mh1', 'mh2'], \
    cb_label=r'Dust load [mg m$^{-2}$]'\
    )

  # dust load diff
  plot_base_3x2_5( 'figures/loaddust_am-5case_minus_pic.png', lon, lat, \
    [data['pio']-data['pic'], data['pic'], data['piz']-data['pic'], data['mh1']-data['pic'], data['mh2']-data['pic']], \
    # levels = [ np.arange(0, 440, 40)] * 5, \
    cmap=[cmap_default]*5, \
    ax_title=['pio', 'pic', 'piz', 'mh1', 'mh2'], \
    cb_label=r'Dust load [mg m$^{-2}$]'\
    )


def plot_loaddust_pi_mh2(month_range):
  m0 = month_range[0]
  m1 = month_range[1]
  nmonth = m1 - m0 + 1

  data = {}
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(m0, m1+1):
      # im = m - 1
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, '1y', 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False
      data[c] += fid_output.variables['loaddust'][0, :, :] * 1.0e6

    data[c] /= nmonth

  data_diff = data['mh2'] - data[pi_case]

  plot_base_3x1( 'figures/loaddust-pio_mh2.png', lon, lat, [data[pi_case], data['mh2'], data_diff], \
    levels = [ np.arange(40, 440, 40), np.arange(40, 440, 40), np.arange(-200, 210, 40) ], \
    cmap = [cmap_default, cmap_default, plt.get_cmap('RdBu_r')], \
    cb_label=r'Dust load [mg m$^{-2}$]', \
    )


def plot_emidust_5case():
  case_list_5case = ['pio', 'pic', 'piz', 'mh1', 'mh2']
  m0 = 1
  m1 = 12
  nmonth = m1 - m0 + 1
  data = {}
  for c in case_list_5case:
    print(c)
    first_loop = True
    for m in range(m0, m1+1):
      # month index: 0 - 11
      im = m - 1
      m_str = '{:02d}'.format(m)

      fname_output = get_fname_output(c, '1y', 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')

      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False

      # Add up to get [g m-2 -1]
      # data[c] += fid_output.variables['emidust'][0, :, :] * 1.0e6  # [kg m-2 s-1] --> [mg m-2 s-1]
      data[c] += fid_output.variables['emidust'][0, :, :] * 1.0e3 * month_day[im]*86400.0 # [kg m-2 s-1] --> [g m-2 m-1]

    # Average for the whole year
    # data[c] /= nmonth

    # Limit the data
    set_limit_to_nan(data[c], [0, 0])

    # Show data info
    tools.show_statistics(data[c])

  # dust emission
  plot_base_3x2_5( 'figures/emidust_am-5case.png', lon, lat, \
    [data['pio'], data['pic'], data['piz'], data['mh1'], data['mh2']], \
    levels = [ np.arange(0, 250, 25)] * 5, \
    cmap=[cmap_default]*5, \
    ax_title=['pio', 'pic', 'piz', 'mh1', 'mh2'], \
    cb_label=r'Dust emission [g m$^{-2}$ a$^{-1}$]'\
    )

  # dust emission diff
  plot_base_3x2_5( 'figures/emidust_am-5case_minus_pic.png', lon, lat, \
    [data['pio']-data['pic'], data['pic'], data['piz']-data['pic'], data['mh1']-data['pic'], data['mh2']-data['pic']], \
    # levels = [ np.arange(0, 440, 40)] * 5, \
    cmap=[cmap_default]*5, \
    ax_title=['pio', 'pic', 'piz', 'mh1', 'mh2'], \
    cb_label=r'Dust emission [g m$^{-2}$ a$^{-1}$]' \
    )


def plot_emidust_pi_mh2(month_range):
  m0, m1 = month_range[0], month_range[1]
  nmonth = m1 - m0 + 1
  data = {}
  total_emidust_global = {}
  total_emidust_na = {}
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(m0, m1+1):
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, '1y', 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False

      # Add up to get [g m-2 a-1]
      data[c] += fid_output.variables['emidust'][0, :, :] * 1.0e3 * month_day[m-1]*86400.0  # [g m-2 mon-1]

    # Calculate global emission flux [Tg a-1]
    total_emidust_global[c] = np.nansum( data[c] * tm5_grid_area ) * 1.0e-12

    # Calculate North Africa emission flux [Tg a-1], [-17, 40, 10, 30]
    regm_lat = (lat>=10) & (lat<=30)
    regm_lon = (lon>=-17) & (lon<=40)
    total_emidust_na[c] = np.nansum( data[c][np.ix_(regm_lat, regm_lon)] * tm5_grid_area[np.ix_(regm_lat, regm_lon)] ) * 1.0e-12
    # print( data[c][np.ix_(regm_lat, regm_lon)] )
    # print( tm5_grid_area[np.ix_(regm_lat, regm_lon)] )
    print('{0}: global dust emission flux per year: {1}'.format(c, total_emidust_global[c]))
    print('{0}: North Africa dust emission flux per year: {1}'.format(c, total_emidust_na[c]))

    set_limit_to_nan(data[c], (0.0, 0.0))

    # emidust[c] /= nmonth

  data_diff = data['mh2'] - data[pi_case]

  plot_base_3x1( 'figures/emidust_am-pio_mh2.png', lon, lat, [data[pi_case], data['mh2'], data_diff], \
    levels = [ [0, 0.1, 0.2, 0.7, 2.1, 7.0, 21.0, 70, 210], [0, 0.1, 0.2, 0.7, 2.1, 7.0, 21.0, 70, 210], \
    np.arange(-80, 90, 20) ], \
    cmap = [plt.get_cmap('YlOrBr'), plt.get_cmap('YlOrBr'), plt.get_cmap('RdBu_r')], \
    cb_label=r'Dust emission [g m$^{-2}$ a$^{-1}$]', \
    )


# total deposition of dust
def plot_depdust_pi_mh2(month_range):
  m0, m1 = month_range[0], month_range[1]
  nmonth = m1 - m0 + 1
  data = {}
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(m0, m1+1):
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, '1y', 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False

      # Add up to get [g m-2 a-1]
      data[c] += fid_output.variables['drydust'][0, :, :] * 1.0e3 * month_day[m-1]*86400.0  # [g m-2 mon-1]
      data[c] += fid_output.variables['wetdust'][0, :, :] * 1.0e3 * month_day[m-1]*86400.0  # [g m-2 mon-1]

    set_limit_to_nan(data[c], (0.0, 0.0))

    # emidust[c] /= nmonth

  data_diff = data['mh2'] - data[pi_case]

  plot_base_3x1( 'figures/depdust_am-pio_mh2.png', lon, lat, [data[pi_case], data['mh2'], data_diff], \
    levels = [ [0, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0], \
    [0, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0], \
    np.arange(-15, 16, 3) ], \
    cmap = [plt.get_cmap('YlOrBr'), plt.get_cmap('YlOrBr'), plt.get_cmap('RdBu_r')], \
    cb_label=r'Dust deposition flux [g m$^{-2}$ a$^{-1}$]', \
    )


def plot_loadsoa_pi_mh2(month_range):
  m0 = month_range[0]
  m1 = month_range[1]
  nmonth = m1 - m0 + 1

  data = {}
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(m0, m1+1):
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, '1y', 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False
      data[c] += fid_output.variables['loadsoa'][0, :, :] * 1.0e6 * month_day[m-1]/365.0

  data_diff = data['mh2'] - data[pi_case]

  # set limit to nan
  ## for c in [pi_case, 'mh2']:
  ##   set_limit_to_nan(data[c], [0, 5.0e-3])
  ## set_limit_to_nan(data_diff, [-5.0e-3, 5.0e-3])

  plot_base_3x1( 'figures/loadsoa-pio_mh2.png', lon, lat, [data[pi_case], data['mh2'], data_diff], \
    levels = [ np.arange(2, 20, 2), np.arange(2, 20, 2), np.arange(-12, 13, 3) ], \
    cmap = [cmap_default, cmap_default, plt.get_cmap('RdBu_r')], \
    cb_label=r'SOA load [mg m$^{-2}$]', \
    )


def plot_od550soa():
  data = {}
  nmonth = 6
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(7, 13):
      im = m - 7
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False
      data[c] += fid_output.variables['od550soa'][0, :, :]

    data[c] /= nmonth
    # set_limit_to_nan(data[c], (0, 0.005*1.0e-2))

  data_diff = data['mh2'] - data[pi_case]

  # set limit to nan
  ## for c in [pi_case, 'mh2']:
  ##   set_limit_to_nan(data[c], [0, 2.0e-5])
  ## set_limit_to_nan(data_diff, [-2.0e-5, 2.0e-5])

  plot_base_3x1( 'figures/od550soa.png', lon, lat, [data[pi_case], data['mh2'], data_diff], \
    levels = [ np.arange(0.0, 0.12, 0.02), np.arange(0.0, 0.12, 0.02), np.arange(-0.08, 0.09, 0.02) ], \
    cmap = [cmap_default, cmap_default, plt.get_cmap('RdBu_r')], \
    cb_label=r'SOA AOD at 550 nm', \
    )


def plot_od550dust_pi_mh2(month_range):
  m0, m1 = month_range[0], month_range[1]
  nmonth = m1 - m0 + 1

  data = {}
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(m0, m1+1):
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, '1y', 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False

      # Add month length weighted data
      data[c] += fid_output.variables['od550dust'][0, :, :] * month_day[m-1]/365.0
      set_limit_to_nan(data[c], (0.0, 0.0))

    # data[c] /= nmonth

  data_diff = data['mh2'] - data[pi_case]

  # set limit to nan
  ## for c in [pi_case, 'mh2']:
  ##   set_limit_to_nan(data[c], [0, 1.0e-4])
  ## set_limit_to_nan(data_diff, [-1.0e-4, 1.0e-4])

  plot_base_3x1( 'figures/od550dust_am-pio_mh2.png', lon, lat, [data[pi_case], data['mh2'], data_diff], \
    levels = [ np.arange(0.1, 0.8, 0.1), np.arange(0.1, 0.8, 0.1), np.arange(-0.5, 0.6, 0.1) ], \
    cmap = [plt.get_cmap('viridis'), plt.get_cmap('viridis'), plt.get_cmap('RdBu_r')], \
    cb_label=r'Dust AOD at 550 nm', \
    )

  reg_na = [-90.0, 130.0, -30.0, 75.0]
  plot_base_3x1( 'figures/od550dust_am_na-pio_mh2.png', \
    lon, lat, [data[pi_case], data['mh2'], data_diff], \
    levels = [ np.arange(0.1, 0.8, 0.1), np.arange(0.1, 0.8, 0.1), np.arange(-0.4, 0.45, 0.05) ], \
    cmap = [plt.get_cmap('viridis'), plt.get_cmap('viridis'), plt.get_cmap('RdBu_r')], \
    cb_label=r'Dust AOD at 550 nm', \
    map_extent=reg_na, \
    )


def plot_od550aer_pi_mh2(month_range):
  m0, m1 = month_range[0], month_range[1]
  nmonth = m1 - m0 + 1

  data = {}
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(m0, m1+1):
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, '1y', 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False

      # Add month length weighted data
      data[c] += fid_output.variables['od550aer'][0, :, :] * month_day[m-1]/365.0
    set_limit_to_nan(data[c], (0.0, 0.0))

    # data[c] /= nmonth

  data_diff = data['mh2'] - data[pi_case]

  # set limit to nan
  ## for c in [pi_case, 'mh2']:
  ##   set_limit_to_nan(data[c], [0, 1.0e-4])
  ## set_limit_to_nan(data_diff, [-1.0e-4, 1.0e-4])

  plot_base_3x1( 'figures/od550aer_am-pio_mh2.png', lon, lat, [data[pi_case], data['mh2'], data_diff], \
    levels = [ np.arange(0.1, 0.8, 0.1), np.arange(0.1, 0.8, 0.1), np.arange(-0.5, 0.6, 0.1) ], \
    cmap = [plt.get_cmap('viridis'), plt.get_cmap('viridis'), plt.get_cmap('RdBu_r')], \
    cb_label=r'Dust AOD at 550 nm', \
    )

  reg_na = [-90.0, 130.0, -30.0, 75.0]
  plot_base_3x1( 'figures/od550aer_am_na-pio_mh2.png', \
    lon, lat, [data[pi_case], data['mh2'], data_diff], \
    levels = [ np.arange(0.1, 0.8, 0.1), np.arange(0.1, 0.8, 0.1), np.arange(-0.4, 0.5, 0.1) ], \
    cmap = [plt.get_cmap('viridis'), plt.get_cmap('viridis'), plt.get_cmap('RdBu_r')], \
    cb_label=r'Aerosol AOD at 550 nm', \
    map_extent=reg_na, \
    )


def plot_prod_elvoc(lev=0):
  data = {}
  nmonth = 6
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(7, 13):
      im = m - 7
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False
      data[c] += fid_output.variables['prod_elvoc'][0, lev, :, :]*1.0e12  # [kg m-2 s-1] --> [ng m-2 s-1]

    data[c] /= nmonth

  data_diff = data['mh2'] - data[pi_case]

  plot_base_3x1( 'figures/prod_elvoc_{0:02d}.png'.format(lev), \
    lon, lat, [data[pi_case], data['mh2'], data_diff], \
    levels=[ np.arange(0.0, 3.5, 0.5), np.arange(0.0, 3.5, 0.5), np.arange(-2.5, 2.6, 0.5) ], \
    cmap = [cmap_default, cmap_default, plt.get_cmap('RdBu_r')], \
    cb_label=r'Production of ELVOC [ng m$^{-2}$ s$^{-1}$]', \
    )


def plot_prod_svoc(lev=0):
  data = {}
  nmonth = 6
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(7, 13):
      im = m - 7
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False
      data[c] += fid_output.variables['prod_svoc'][0, lev, :, :]*1.0e12

    data[c] /= nmonth

  data_diff = data['mh2'] - data[pi_case]

  plot_base_3x1( 'figures/prod_svoc_{0:02d}.png'.format(lev), \
    lon, lat, [data[pi_case], data['mh2'], data_diff], \
    levels=[ np.arange(0.0, 8.1, 1), np.arange(0.0, 8.1, 1), np.arange(-6, 7, 2) ], \
    cmap = [cmap_default, cmap_default, plt.get_cmap('RdBu_r')], \
    cb_label=r'Production of SVOC [ng m$^{-2}$ s$^{-1}$]', \
    )


def plot_CCN02_pi_mh2(month_range, lev=0):
  m0, m1 = month_range[0], month_range[1]
  nmonth = m1 - m0 + 1

  data = {}
  pi_case = 'piz'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(m0, m1+1):
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, '1y', 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False
      # CCN0.20: [cm-3]
      data[c] += fid_output.variables['CCN0.20'][0, lev, :, :] * month_day[m-1]/365.0

  data_diff = data['mh2'] - data[pi_case]

  plot_base_3x1( 'figures/CCN02_{0:02d}-{1}_mh2.png'.format(lev, pi_case), \
    lon, lat, [data[pi_case], data['mh2'], data_diff], \
    ax_title = [pi_case, 'mh2', 'mh2 - {0}'.format(pi_case)], \
    levels=[ np.arange(100.0, 1000.0, 100.0), np.arange(100.0, 1000.0, 100), np.arange(-40, 41, 5) ], \
    cmap = [cmap_default, cmap_default, plt.get_cmap('RdBu_r')], \
    cb_label=r'CCN at 0.2% [molec cm$^{-3}$]', \
    )


def plot_CCN10_pi_mh2(month_range, lev=0):
  m0, m1 = month_range[0], month_range[1]
  nmonth = m1 - m0 + 1

  data = {}
  pi_case = 'piz'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(m0, m1+1):
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, '1y', 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False
      data[c] += fid_output.variables['CCN1.00'][0, lev, :, :] * month_day[m-1]/365.0

  data_diff = data['mh2'] - data[pi_case]
  tools.show_statistics(data_diff)

  plot_base_3x1( 'figures/CCN10_{0:02d}-{1}_mh2.png'.format(lev, pi_case), \
    lon, lat, [data[pi_case], data['mh2'], data_diff], \
    ax_title = [pi_case, 'mh2', 'mh2 - {0}'.format(pi_case)], \
    levels=[ np.arange(200, 1400, 200), np.arange(200, 1400, 200), np.arange(-50, 55, 10) ], \
    cmap = [cmap_default, cmap_default, plt.get_cmap('RdBu_r')], \
    cb_label=r'CCN at 1.0% [molec cm$^{-3}$]', \
    )


def plot_gr1_2(lev):
  data = {}
  nmonth = 6
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(7, 13):
      im = m - 7
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False
      data[c] += fid_output.variables['prod_elvoc'][0, lev, :, :]

    data[c] /= nmonth

  data_diff = data['mh2'] - data[pi_case]

  plot_base_3x1( 'figures/gr1_2_{0:02d}.png'.format(lev), \
    lon, lat, [data[pi_case], data['mh2'], data_diff], \
    levels=[ np.arange(0.0, 3.3e-12, 0.4e-12), np.arange(0.0, 3.3e-12, 0.4e-12), np.arange(-2.5e-12, 2.6e-12, 0.5e-12) ], \
    cmap = [cmap_default, cmap_default, plt.get_cmap('RdBu_r')], \
    cb_label=r'growth of mode 1 into 2 [molec cm$^{-3}$ s$^{-1}$]', \
    )


def plot_pressure(lev):
  data = {}
  nmonth = 6
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(7, 13):
    # for m in range(7, 8):
      im = m - 7
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False
      
      data[c] += fid_output.variables['pressure'][0, lev, :, :]

    data[c] /= nmonth

  data_diff = data['mh2'] - data[pi_case]

  plot_base_3x1( 'figures/pressure_{0:02d}.png'.format(lev), \
    lon, lat, [data[pi_case], data['mh2'], data_diff], \
    # levels=[ np.arange(0.0, 0.11, 0.01), np.arange(0.0, 0.11, 0.01), np.arange(-0.05, 0.06, 0.01) ], \
    cmap = [cmap_default, cmap_default, plt.get_cmap('RdBu_r')], \
    cb_label=r'Pressure [Pa]', \
    )


def plot_ps():
  data = {}
  nmonth = 6
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(7, 13):
      im = m - 7
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False

      data[c] += fid_output.variables['ps'][0, :, :]

    data[c] /= nmonth

  data_diff = data['mh2'] - data[pi_case]

  plot_base_3x1( 'figures/ps.png', lon, lat, [data[pi_case], data['mh2'], data_diff], \
    # levels=[ np.arange(0.0, 0.11, 0.01), np.arange(0.0, 0.11, 0.01), np.arange(-0.05, 0.06, 0.01) ], \
    cmap = [cmap_default, cmap_default, plt.get_cmap('RdBu_r')], \
    cb_label=r'Surface pressure [Pa]', \
    )
#       fname_output = get_fname_output(c, 'general', '2009', m_str)


def plot_gph3D(lev):
  data = {}
  nmonth = 6
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(7, 13):
    # for m in range(7, 8):
      im = m - 7
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False
      
      data[c] += fid_output.variables['gph3D'][0, lev, :, :]

    data[c] /= nmonth

  data_diff = data['mh2'] - data[pi_case]

  plot_base_3x1( 'figures/gph3D_{0:02d}.png'.format(lev), \
    lon, lat, [data[pi_case], data['mh2'], data_diff], \
    # levels=[ np.arange(0.0, 0.11, 0.01), np.arange(0.0, 0.11, 0.01), np.arange(-0.05, 0.06, 0.01) ], \
    cmap = [cmap_default, cmap_default, plt.get_cmap('RdBu_r')], \
    cb_label=r'gph3D [m]', \
    )


def plot_delta_gph3D(lev):
  data = {}
  nmonth = 6
  pi_case = 'pio'
  for c in [pi_case, 'mh2']:
    first_loop = True
    for m in range(7, 13):
    # for m in range(7, 8):
      im = m - 7
      m_str = '{:02d}'.format(m)
      fname_output = get_fname_output(c, 'general', '2009', m_str)
      fid_output = Dataset(fname_output, 'r')
      if first_loop:
        lon = fid_output.variables['lon'][:]
        lat = fid_output.variables['lat'][:]
        nlon = len(lon)
        nlat = len(lat)
        data[c] = np.zeros( (nlat, nlon) )
        first_loop = False
      
      data[c] += fid_output.variables['gph3D'][0, lev+1, :, :] - fid_output.variables['gph3D'][0, lev, :, :]

    data[c] /= nmonth

  data_diff = data['mh2'] - data[pi_case]

  plot_base_3x1( 'figures/delta_gph3D_{0:02d}.png'.format(lev), \
    lon, lat, [data[pi_case], data['mh2'], data_diff], \
    # levels=[ np.arange(0.0, 0.11, 0.01), np.arange(0.0, 0.11, 0.01), np.arange(-0.05, 0.06, 0.01) ], \
    cmap = [cmap_default, cmap_default, plt.get_cmap('RdBu_r')], \
    cb_label=r'delta gph3D [m]', \
    )


def plot_onlinedust():
  potsrc = {}
  soilph = {}

  first_loop = True
  for c in ['pio', 'pic', 'mh1', 'mh2']:
    fname = get_fname_onlinedust(c, '1850_1859_mean')
    fid = Dataset(fname, 'r')
    if first_loop:
      lon = fid.variables['lon'][:]
      lat = fid.variables['lat'][:]
      nlon = len(lon)
      nlat = len(lat)
      nsoilph = len(fid.dimensions['nsoilph'])
      first_loop = False

    potsrc[c] = fid.variables['potsrc'][:]
    soilph[c] = fid.variables['soilph'][2, :, :] + fid.variables['soilph'][3, :, :]

    # set_limit_to_nan(data[c], [0, 1.0e-3])

  plot_base_2x2( 'figures/potsrc-1850_1859_mean-2009_pi_mh1_mh2.png', lon, lat, \
    [potsrc['pio'], potsrc['pic'], potsrc['mh1'], potsrc['mh2']], \
    # levels = [ np.arange(0.0, 0.9, 0.1), np.arange(0.0, 0.9, 0.1), np.arange(0.0, 0.9, 0.1), np.arange(0.0, 0.9, 0.1)], \
    # cmap = [cmap_default, cmap_default, cmap_default, cmap_default], \
    ax_title = ['TM5 2009', 'Lu2018 PI', 'Lu2018 MH', 'Lu2018 MHgsrd'], \
    cb_label=r'Potential dust source', \
    )

  plot_base_2x2( 'figures/soilph-1850_1859_mean-2009_pi_mh1_mh2.png', lon, lat, \
    [soilph['pio'], soilph['pic'], soilph['mh1'], soilph['mh2']], \
    # levels = [ np.arange(0.0, 0.9, 0.1), np.arange(0.0, 0.9, 0.1), np.arange(0.0, 0.9, 0.1), np.arange(0.0, 0.9, 0.1)], \
    # cmap = [cmap_default, cmap_default, cmap_default, cmap_default], \
    ax_title = ['TM5 2009', 'Lu2018 PI', 'Lu2018 MH', 'Lu2018 MHgsrd'], \
    cb_label=r'soilph ', \
    )


if __name__ == '__main__':
  month_range = (1, 12)
  ##### Input data

  #
  # vegetation
  #

  # plot_vegetation_Lu2018_lrg_gxx()
  # plot_vegetation_tm52009_Lu2018( (1, 12) )

  #
  # BVOC emissions
  #

  # isoprene emission
  # plot_iso_emission_tm52009_Lu2018()
  # plot_iso_emission_tm52009_mh2()

  # monoterpe emission
  # plot_mon_emission_tm52009_Lu2018()
  # plot_mon_emission_tm52009_mh2()

  #
  # Online dust (onlinedust_4.nc)
  #
  plot_onlinedust()

  # Potential source
  # plot_pot

  ##### Output data

  # Dust load
  # plot_loaddust_5case()
  # plot_loaddust_pi_mh2( (1, 12) )

  # Dust emission and deposition
  # plot_emidust_5case()
  # plot_emidust_pi_mh2( (1, 12) )
  # plot_depdust_pi_mh2( (1, 12) )

  # AOD
  # plot_od550dust_pi_mh2( (1, 12) )
  # plot_od550aer_pi_mh2( month_range )

  # SOA load
  # plot_loadsoa_pi_mh2( month_range )
  # plot_od550soa()
  # plot_od550dust()
  # plot_od550aer()

  # CCN
  # lev = 0
  # plot_CCN02_pi_mh2(month_range, lev)
  # plot_CCN10_pi_mh2(month_range, lev)

  # lev = 1
  # plot_CCN02_pi_mh2(month_range, lev)
  # plot_CCN10_pi_mh2(month_range, lev)

  # lev = 2
  # plot_CCN02_pi_mh2(month_range, lev)
  # plot_CCN10_pi_mh2(month_range, lev)
  
  # plot_prod_elvoc(0)
  # plot_prod_svoc(0)
  # plot_gr1_2(0)

  # plot_pressure(0)
  # plot_ps()
  
  # lev = 0
  # plot_prod_elvoc(lev)
  # plot_prod_svoc(lev)
  # plot_gr1_2(lev)
  # plot_CCN02(lev)
  # plot_CCN10(lev)
  # plot_pressure(lev)
  
  # plot_gph3D(lev)
  # plot_delta_gph3D(4)
