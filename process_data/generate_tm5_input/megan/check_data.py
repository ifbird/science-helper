#==============================================================================#
# Header
#==============================================================================#

import os
import sys
sys.path.insert(0, '/homeappl/home/putian/scripts/science-helper/pypack')

import numpy as np
import numpy.ma as ma
from netCDF4 import Dataset

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

import lu2018
import netcdf
import plot
import tools

from local import *


#==============================================================================#
# Set parameters
#==============================================================================#

#==============================================================================#
# Helper functions
#==============================================================================#

def plot_lu2018_lrg_gxx_megan_new( \
  data_lu2018_lrg, lon_lu2018_lrg, lat_lu2018_lrg, \
  data_lu2018_gxx, lon_lu2018_gxx, lat_lu2018_gxx, \
  data_megan_new, lon_megan_new, lat_megan_new, \
  fg_title, fname):

  def plot_local_basemap(ax):
    # Parameters
    pm = 'moll'
    reg = [-90, 90, -180, 180]
    parallels = np.arange(-90.0, 91.0, 15.0)
    meridians = np.arange(-180.0, 181.0, 30.0)

    # Create basemap
    m = Basemap( \
      projection=pm, \
      lon_0=0, lat_0=0, \
      llcrnrlat=reg[0], urcrnrlat=reg[1], llcrnrlon=reg[2], urcrnrlon=reg[3], \
      resolution='c', \
      ax=ax \
      )

    # Draw coastlines
    m.drawcoastlines(linewidth=0.5)

    # Draw parallels and meridians (labels = [left,right,top,bottom])
    m.drawparallels(parallels, labels=[True, False, False, False], fontsize=18)
    m.drawmeridians(meridians, labels=[False, False, False, True], fontsize=18)
    
    return m

  # Set parameters
  bounds = np.linspace(0.0, 600.0, 21)  # colormap boundaries
  cmap, norm = plot.create_cmap_norm_from_bounds('Greens', bounds)
  # cm.set_under('white')
  # cm_diff = plt.get_cmap('BrBG_r')
  # vmin, vmax = 0.1, 1.6
  # vmin_diff, vmax_diff = -0.04, 0.04
  # ticks_diff = [-0.04, -0.03, -0.02, -0.01, 0, 0.01, 0.02, 0.03, 0.04]
  # eps = vmin
  # eps_diff = 5.0e-4
  # alpha = 0.9
  DPI = 150

  # Initiate figure
  fg, ax = plt.subplots(3, 1, figsize=(16, 24), dpi=150)

  # lu2018 data_lrg
  m0 = plot_local_basemap(ax[0])
  x0, y0 = m0(lon_lu2018_lrg, lat_lu2018_lrg)
  z0 = data_lu2018_lrg
  zm0 = ma.array(z0, mask=z0==0.0)
  h0 = m0.scatter(x0, y0, s=4, c=zm0, norm=norm, cmap=cmap, zorder=3)
  m0.colorbar(h0, extend='both')
  ax[0].set_title('Lu2018 data_lrg', fontsize=20)

  # lu2018 data_gxx
  m1 = plot_local_basemap(ax[1])
  x1, y1 = plot.ll2xy_for_map_pcolor(lon_lu2018_gxx, lat_lu2018_gxx, m1)
  z1 = data_lu2018_gxx.transpose()
  zm1 = ma.array(z1, mask=z1==0.0)
  h1 = m1.pcolormesh(x1, y1, zm1, alpha=0.7, zorder=3, cmap=cmap, norm=norm)
  m1.colorbar(h1, extend='both')
  ax[1].set_title('Lu2018 data_gxx', fontsize=20)

  # megan new
  m2 = plot_local_basemap(ax[2])
  x2, y2 = plot.ll2xy_for_map_pcolor(lon_megan_new, lat_megan_new, m2)
  z2 = data_megan_new
  zm2 = ma.array(z2, mask=z2==0.0)
  h2 = m2.pcolormesh(x2, y2, zm2, alpha=0.7, zorder=3, cmap=cmap, norm=norm)
  m2.colorbar(h2, extend='both')
  ax[2].set_title('MEGAN new', fontsize=20)

  # Save the figure
  # fg.tight_layout()
  fg.suptitle(fg_title, fontsize=20)
  fg.savefig(fname, dpi=150)


def plot_megan_sample_iso_mon( \
  data_megan_sample_iso, data_megan_sample_mon, lon_megan_sample, lat_megan_sample, \
  fg_title, fname):

  def plot_local_basemap(ax):
    # Parameters
    pm = 'moll'
    reg = [-90, 90, -180, 180]
    parallels = np.arange(-90.0, 91.0, 15.0)
    meridians = np.arange(-180.0, 181.0, 30.0)

    # Create basemap
    m = Basemap( \
      projection=pm, \
      lon_0=0, lat_0=0, \
      llcrnrlat=reg[0], urcrnrlat=reg[1], llcrnrlon=reg[2], urcrnrlon=reg[3], \
      resolution='c', \
      ax=ax \
      )

    # Draw coastlines
    m.drawcoastlines(linewidth=0.5)

    # Draw parallels and meridians (labels = [left,right,top,bottom])
    m.drawparallels(parallels, labels=[True, False, False, False], fontsize=18)
    m.drawmeridians(meridians, labels=[False, False, False, True], fontsize=18)
    
    return m

  # Set parameters
  bounds = np.linspace(0.0, 600.0, 21)  # colormap boundaries
  cmap, norm = plot.create_cmap_norm_from_bounds('Greens', bounds)
  # cm.set_under('white')
  # cm_diff = plt.get_cmap('BrBG_r')
  # vmin, vmax = 0.1, 1.6
  # vmin_diff, vmax_diff = -0.04, 0.04
  # ticks_diff = [-0.04, -0.03, -0.02, -0.01, 0, 0.01, 0.02, 0.03, 0.04]
  # eps = vmin
  # eps_diff = 5.0e-4
  # alpha = 0.9
  DPI = 150

  # Initiate figure
  fg, ax = plt.subplots(2, 1, figsize=(16, 24), dpi=150)

  # megan sample
  m_iso = plot_local_basemap(ax[0])
  x_iso, y_iso = plot.ll2xy_for_map_pcolor(lon_megan_sample, lat_megan_sample, m_iso)
  z_iso = data_megan_sample_iso
  zm_iso = ma.array(z_iso, mask=z_iso==0.0)
  h_iso = m_iso.pcolormesh(x_iso, y_iso, zm_iso, alpha=0.7, zorder=3)  #, cmap=cmap, norm=norm)
  m_iso.colorbar(h_iso, extend='both')
  ax[0].set_title('MEGAN sample iso', fontsize=20)

  m_mon = plot_local_basemap(ax[1])
  x_mon, y_mon = plot.ll2xy_for_map_pcolor(lon_megan_sample, lat_megan_sample, m_mon)
  z_mon = data_megan_sample_mon
  zm_mon = ma.array(z_mon, mask=z_mon==0.0)
  h_mon = m_mon.pcolormesh(x_mon, y_mon, zm_mon, alpha=0.7, zorder=3)  # , cmap=cmap, norm=norm)
  m_mon.colorbar(h_mon, extend='both')
  ax[1].set_title('MEGAN sample mon', fontsize=20)

  # Save the figure
  # fg.tight_layout()
  fg.suptitle(fg_title, fontsize=20)
  fg.savefig(fname, dpi=150)


def check_lu2018_megansample(label1, data1, label2, data2):
  #===== Print statistics =====#
  print(label1)
  tools.show_statistics(data1)
  print(label2)
  tools.show_statistics(data2)

  return


#==============================================================================#
# Main program
#==============================================================================#
if __name__=='__main__':

  year = 1850
  c = 'pi'
  s = 'mon'
  y = '1850_1859_mean'  # '1850_1859_mean'
  molmass = {'iso': 68.0e-3, 'mon': 136.0e-3}
  weight_to_C = {'iso': 60.0/68.0, 'mon': 120.0/136.0}

  print(c, s, y)

  # Grid box area
  print('Reading grid area of 0.5x0.5 ...')
  fid_gridarea = Dataset(fname_gridarea_0p5x0p5, 'r')
  lon_gridarea = fid_gridarea.variables['lon'][:]
  lat_gridarea = fid_gridarea.variables['lat'][:]
  data_gridarea = fid_gridarea.variables['gridbox_area'][:]
  print('Dimension of data_gridarea: ', data_gridarea.shape)

  # Lu2018 data in lrg grid
  print('Reading data_lu2018_lrg...')
  datadict_lu2018_lrg = lu2018.read_bvoc_data_lrg(get_fname_lu2018_lrg(c, s))
  lon_lu2018_lrg, lat_lu2018_lrg = datadict_lu2018_lrg['lon'], datadict_lu2018_lrg['lat']
  data_lu2018_lrg = datadict_lu2018_lrg['er']
  # tools.show_statistics(data_lu2018_lrg)
  print('Dimension of data_lu2018_lrg: ', data_lu2018_lrg.shape)

  # Interpolated Lu2018 data in gxx grid
  print('Reading data_lu2018_gxx ...')
  fid_lu2018_gxx = Dataset(get_fname_lu2018_gxx(c, s), 'r')
  lon_lu2018_gxx = fid_lu2018_gxx.variables['lon'][:]
  lat_lu2018_gxx = fid_lu2018_gxx.variables['lat'][:]
  data_lu2018_gxx = fid_lu2018_gxx.variables['data_gxx'][:]
  for im in range(nmon):
    data_lu2018_gxx[:, im, :, :] *= unit_conv(molmass[s], month_day[im])
  data_lu2018_gxx_mean = np.mean(data_lu2018_gxx, axis=0)

  # Set the value in the north Africa to 0
  reg_nafr = (-20.0, 40.0, 10.0, 30.0)  # W, E, S, N
  regm_lon = (lon_lu2018_gxx>=reg_nafr[0]) & (lon_lu2018_gxx<=reg_nafr[1])
  regm_lat = (lat_lu2018_gxx>=reg_nafr[2]) & (lat_lu2018_gxx<=reg_nafr[3])
  data_lu2018_gxx_mean_withoutna = np.copy(data_lu2018_gxx_mean)  # do not consider the north africa
  for im in range(nmon):
    data_lu2018_gxx_mean_withoutna[im][np.ix_(regm_lon, regm_lat)] = 0.0

  data_lu2018_gxx_mean_global = np.zeros((nmon,))
  data_lu2018_gxx_mean_withoutna_global = np.zeros((nmon,))
  for im in range(nmon):
    data_lu2018_gxx_mean_global[im] = \
      np.sum(data_lu2018_gxx_mean[im, :, :]*np.transpose(data_gridarea)) * month_day[im] * 86400.0* 1.0e-9  # [kg -s] --> [Tg mon-1]
    data_lu2018_gxx_mean_withoutna_global[im] = \
      np.sum(data_lu2018_gxx_mean_withoutna[im, :, :]*np.transpose(data_gridarea)) * month_day[im] * 86400.0* 1.0e-9  # [kg -s] --> [Tg mon-1]
  print('Dimension of data_lu2018_gxx: ', data_lu2018_gxx.shape)
  print('Dimension of data_lu2018_gxx_mean: ', data_lu2018_gxx_mean.shape)

  # Input megan smaple data
  print('Reading data_megan_sample ...')
  # fid_megan_sample_iso  = Dataset(fname_megan_sample('iso', '2009'), 'r')
  # lon_megan_sample      = fid_megan_sample_iso.variables['lon'][:]
  # lat_megan_sample      = fid_megan_sample_iso.variables['lat'][:]
  # data_megan_sample_iso = fid_megan_sample_iso.variables['MEGAN_MACC'][:]

  # fid_megan_sample_mon  = Dataset(fname_megan_sample('mon', '2009'), 'r')
  # data_megan_sample_mon = fid_megan_sample_mon.variables['MEGAN_MACC'][:]

  fid_megan_sample  = Dataset(get_fname_megan_sample(s, '2009'), 'r')
  lon_megan_sample  = fid_megan_sample.variables['lon'][:]
  lat_megan_sample  = fid_megan_sample.variables['lat'][:]
  data_megan_sample = fid_megan_sample.variables['MEGAN_MACC'][:]
  data_megan_sample_global = np.zeros((nmon,))
  for im in range(nmon):
    data_megan_sample_global[im] = \
      np.sum(data_megan_sample[im, :, :]*data_gridarea) * month_day[im] * 86400.0* 1.0e-9  # [kg -s] --> [Tg mon-1]
  print('Dimension of data_megan_sample: ', data_megan_sample.shape)

  # New megan input data
  print('Reading data_megan_new...')
  fid_megan_new = Dataset(get_fname_megan_new(c, s, y), 'r')
  lon_megan_new = fid_megan_new.variables['lon'][:]
  lat_megan_new = fid_megan_new.variables['lat'][:]
  data_megan_new = fid_megan_new.variables['MEGAN_MACC'][:]
  data_megan_new_global = np.zeros((nmon,))
  for im in range(nmon):
    data_megan_new_global[im] = \
      np.sum(data_megan_new[im, :, :]*data_gridarea) * month_day[im] * 86400.0* 1.0e-9  # [kg -s] --> [Tg mon-1]
  print('Dimension of data_megan_new: ', data_megan_new.shape)

  #===== Check the data statistics =====#

  #===== Check the global carbon emission data =====#
  check_lu2018_megansample('lu2018 gxx:', data_lu2018_gxx, 'megan sample:', data_megan_sample)
  print('The global emission of lu2018_gxx per year [TgC yr-1]: ', \
    np.sum(data_lu2018_gxx_mean_global)*weight_to_C[s])
  print('The global emission of lu2018_gxx without NA per year [TgC yr-1]: ', \
    np.sum(data_lu2018_gxx_mean_withoutna_global)*weight_to_C[s])
  print('The global emission of megan_sample per year [TgC yr-1]: ', \
    np.sum(data_megan_sample_global)*weight_to_C[s])
  print('The global emission of megan_new per year [TgC yr-1]: ', \
    np.sum(data_megan_new_global)*weight_to_C[s])

  tools.show_statistics(data_lu2018_gxx_mean)
  tools.show_statistics(data_megan_new)


  # Plot Lu2018 lrg, Lu2018 gxx, megan new
  # for im in range(nmon):
  #   fg_title = '{0}_{1}_{2}_{3:02d}'.format(c, s, year, im+1)
  #   fname = '{0}_{1}_{2}_{3:02d}.png'.format(c, s, year, im+1)
  #   print('Plotting {0} ...'.format(fg_title))

  #   plot_lu2018_lrg_gxx_megan_new( \
  #     data_lu2018_lrg[year-1850, im, :], lon_lu2018_lrg, lat_lu2018_lrg, \
  #     data_lu2018_gxx[year-1850, im, :, :], lon_lu2018_gxx, lat_lu2018_gxx, \
  #     data_megan_new[im, :, :], lon_megan_new, lat_megan_new, \
  #     fg_title, fname)

  # Plot MEGAN sample
  # for im in range(nmon):
  #   fg_title = '2009_{0}_{1:02d}'.format(s, im+1)
  #   fname = '2009_{0}_{1:02d}.png'.format(s, im+1)
  #   print('Plotting {0} ...'.format(fg_title))

  #   plot_megan_sample_iso_mon( \
  #     data_megan_sample_iso[im, :, :], data_megan_sample_mon[im, :, :], lon_megan_new, lat_megan_new, \
  #     fg_title, fname)
