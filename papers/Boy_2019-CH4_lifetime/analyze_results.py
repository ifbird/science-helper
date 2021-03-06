import os
import sys
sys.path.insert(0, '/users/putian/scripts/science-helper/')

from datetime import datetime
from datetime import timedelta

import numpy as np
import xarray as xr

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import matplotlib.colors as colors

# Cartopy for the global map drawing
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import pypack.functions as ppfunc


# ---------------------------------------------------------------------- #
#
# Helper Functions
#
# ---------------------------------------------------------------------- #
def open_result_dataset(case, leg):
  results_dir = '/scratch/project_2001025/tm5mp/runs'

  case_dir = {}
  case_dir['BASE'] = 'boy2019-base/rundir'
  case_dir['E0C6'] = 'boy2019-E0C6/rundir'
  case_dir['E6C6'] = 'boy2019-E6C6/rundir'

  case_name = ['BASE', 'E0C6', 'E6C6']
  if case not in case_name:
    print('Wrong case name.')
    return None

  data = xr.open_mfdataset( \
      '{0}/{1}/output-{2}/general_TM5_general_output_2009*_monthly.nc'.format( \
      results_dir, case_dir[case], leg), \
      combine='by_coords')

  return data


# Grid area used as weights for average
area_path = '/projappl/project_2001025/tm5mp/data/tm5_input_modified/TM5_tropomi_griddef.nc'
area = xr.open_dataset(area_path)['area']

#
# results_dir = '/scratch/project_2001025/tm5mp/runs'
#
# case_dir = {}
# case_dir['BASE'] = 'boy2019-base/rundir'
# case_dir['E0C6'] = 'boy2019-E0C6/rundir'
# case_dir['E6C6'] = 'boy2019-E6C6/rundir'
#
# data = xr.open_mfdataset( \
    #   '{0}/{1}/output-*/general_TM5_general_output_2009*_monthly.nc'.format( \
    #   results_dir, case_dir['BASE']), \
    #   combine='by_coords')
#
# print(data)
#
# dataset = {}
# ch4_gm = {}
#
# for case in ['BASE', 'E0C6']:
#   dataset[case] = {}
#   ch4_gm[case] = {}
#   for i in range(2, 11):
#     leg = '2009-{0:02d}'.format(i)
#     dataset[case][leg] = open_result_dataset(case, leg)
#     ch4_gm[case][leg] = ppfunc.masked_average( \
    #       dataset[case][leg]['GAS_CH4'], \
    #       dim = ('lat', 'lon'), \
    #       weights = area)


# Saved data folder
savedir = '/scratch/project_2001025/putian/Boy_2019-CH4_lifetime'

# Gases
ds = {}
for case in ['BASE', 'E0C6', 'E6C6']:
  ds[case] = xr.open_dataset( \
    '{0}/{1}-output-GAS_CH4_GAS_TERP_GAS_OH-general_output.nc'.format( \
    savedir, case) )

# Meteo
ds_meteo = xr.open_dataset( \
  '{0}/BASE-output-temp_airmass_pressure_gph3D_ps-general_output.nc'.format( \
  savedir) )

# Layer thickness
ds_deltaz3d = xr.open_dataset( \
  '{0}/BASE-output-deltaz3d-aerocom3_output.nc'.format( \
  savedir) )

# Set consistent level coordinates with other datasets
ds_deltaz3d = ds_deltaz3d.rename({'alevel': 'lev'})
ds_deltaz3d = ds_deltaz3d.assign_coords({'lev': ds_meteo['lev'], 'time': ds_meteo['time']})

# Level index of tropopause, about 200 hPa
# print(ds_meteo['pressure'][0, 18:25, 45, 45].values)
ltropo = 20

# Total volume of troposphere
total_tropo_vol = (ds_deltaz3d['deltaz3d'][:, 0:ltropo+1, :, :] * area).sum( \
    dim=('lev', 'lat', 'lon') )

# Total air mass
ppb = 1.0e-9
ppt = 1.0e-12
to_ppb= 1.0/ppb
to_ppt= 1.0/ppt
Avog = 6.022e23
xmm_ch4 = 16.04e-3  # [kg mol-1]
xmm_mt = 136.0e-3  # [kg mol-1]
xmm_air = 28.97e-3  # [kg mol-1]
xmm_oh = 17.0e-3  # [kg mol-1]
total_air_mass = (ds_meteo['airmass'][:, 0:ltropo+1, :, :] * area).sum( \
    dim=('lev', 'lat', 'lon') )
air_avg_mconc = total_air_mass / total_tropo_vol
air_avg_nconc = air_avg_mconc / xmm_air * Avog * 1.0e-6  # [molec cm-3]

# Gas concentrations
gas_total_mass = {}
gas_avg_mconc = {}
gas_avg_nconc = {}
gas_avg_ppb = {}
gas_avg_ppt = {}
gas_havg_nconc = {}  # [molec cm-3], horizontal number concentration

print( ds[case]['GAS_CH4'][:, 0:ltropo+1, :, :] )
print( ds_deltaz3d['deltaz3d'][:, 0:ltropo+1, :, :])

for case in ['BASE', 'E0C6', 'E6C6']:
  gas_total_mass[case] = {}
  gas_avg_mconc[case] = {}
  gas_avg_nconc[case] = {}
  gas_avg_ppb[case] = {}
  gas_avg_ppt[case] = {}
  gas_havg_nconc[case] = {}

def calculate_gas_concentration(case, indt, gas, xmm):
  gas_total_mass[case][gas] = (ds[case][gas][:, 0:ltropo+1, :, :] * \
      ds_deltaz3d['deltaz3d'][:, 0:ltropo+1, :, :] * \
      area).sum( dim=('lev', 'lat', 'lon') )
  gas_avg_mconc[case][gas] = \
      gas_total_mass[case][gas] / total_tropo_vol[indt[0]:indt[1]]  # [kg m-3]
  gas_avg_nconc[case][gas] = gas_avg_mconc[case][gas] / xmm * Avog * 1.0e-6  # [molec cm-3]
  gas_avg_ppb[case][gas] = gas_avg_nconc[case][gas] / air_avg_nconc[indt[0]:indt[1]] * to_ppb
  gas_avg_ppt[case][gas] = gas_avg_nconc[case][gas] / air_avg_nconc[indt[0]:indt[1]] * to_ppt
  # gas_havg_nconc[case][gas] = ds[case][gas].mean(dim=('lat', 'lon')) / xmm * Avog * 1.0e-6  # [molec cm-3]
  gas_havg_nconc[case][gas] = ppfunc.masked_average( \
      ds[case][gas], \
      dim = ('lat', 'lon'), \
      weights = area)
  gas_havg_nconc[case][gas] = gas_havg_nconc[case][gas] / xmm * Avog * 1.0e-6

calculate_gas_concentration('BASE', (0, ds['BASE']['time'].size), 'GAS_CH4', xmm_ch4)
calculate_gas_concentration('BASE', (0, ds['BASE']['time'].size), 'GAS_TERP', xmm_mt)
calculate_gas_concentration('BASE', (0, ds['BASE']['time'].size), 'GAS_OH', xmm_oh)

calculate_gas_concentration('E0C6', (24, ds['BASE']['time'].size), 'GAS_CH4', xmm_ch4)
calculate_gas_concentration('E0C6', (24, ds['BASE']['time'].size), 'GAS_TERP', xmm_mt)
calculate_gas_concentration('E0C6', (24, ds['BASE']['time'].size), 'GAS_OH', xmm_oh)

calculate_gas_concentration('E6C6', (24, 60), 'GAS_CH4', xmm_ch4)
calculate_gas_concentration('E6C6', (24, 60), 'GAS_TERP', xmm_mt)
calculate_gas_concentration('E6C6', (24, 60), 'GAS_OH', xmm_oh)


# case = 'BASE'
# ch4_total_mass[case] = (ds[case]['GAS_CH4'][:, 0:ltropo+1, :, :] * \
    #   ds_deltaz3d['deltaz3d'][:, 0:ltropo+1, :, :] * \
    #   area).sum( dim=('lev', 'lat', 'lon') )
# ch4_avg_mconc[case] = ch4_total_mass[case] / total_tropo_vol  # [kg m-3]
# ch4_avg_nconc[case] = ch4_avg_mconc[case] / xmm_ch4 * Avog * 1.0e-6  # [molec cm-3]
# ch4_avg_ppb[case] = ch4_avg_nconc[case] / air_avg_nconc * to_ppb
# mt_total_mass[case] = (ds[case]['GAS_TERP'][:, 0:ltropo+1, :, :] * \
    #   ds_deltaz3d['deltaz3d'][:, 0:ltropo+1, :, :] * \
    #   area).sum( dim=('lev', 'lat', 'lon') )
# mt_avg_mconc[case] = mt_total_mass[case] / total_tropo_vol  # [kg m-3]
# mt_avg_nconc[case] = mt_avg_mconc[case] / xmm_mt * Avog * 1.0e-6  # [molec cm-3]
# mt_avg_ppb[case] = mt_avg_nconc[case] / air_avg_nconc * to_ppb
# mt_avg_ppt[case] = mt_avg_nconc[case] / air_avg_nconc * to_ppt
#
# case = 'E0C6'
# ch4_total_mass[case] = (ds[case]['GAS_CH4'][:, 0:ltropo+1, :, :] * \
    #   ds_deltaz3d['deltaz3d'][:, 0:ltropo+1, :, :] * \
    #   area).sum( dim=('lev', 'lat', 'lon') )
# ch4_avg_mconc[case] = ch4_total_mass[case] / total_tropo_vol[24:]
# ch4_avg_nconc[case] = ch4_avg_mconc[case] / xmm_ch4 * Avog * 1.0e-6  # [molec cm-3]
# ch4_avg_ppb[case] = ch4_avg_nconc[case] / air_avg_nconc[24:] * to_ppb
# mt_total_mass[case] = (ds[case]['GAS_TERP'][:, 0:ltropo+1, :, :] * \
    #   ds_deltaz3d['deltaz3d'][:, 0:ltropo+1, :, :] * \
    #   area).sum( dim=('lev', 'lat', 'lon') )
# mt_avg_mconc[case] = mt_total_mass[case] / total_tropo_vol[24:]  # [kg m-3]
# mt_avg_nconc[case] = mt_avg_mconc[case] / xmm_mt * Avog * 1.0e-6  # [molec cm-3]
# mt_avg_ppb[case] = mt_avg_nconc[case] / air_avg_nconc[24:] * to_ppb
# mt_avg_ppt[case] = mt_avg_nconc[case] / air_avg_nconc[24:] * to_ppt
#
# case = 'E6C6'
# ch4_total_mass[case] = (ds[case]['GAS_CH4'][:, 0:ltropo+1, :, :] * \
    #   ds_deltaz3d['deltaz3d'][:, 0:ltropo+1, :, :] * \
    #   area).sum( dim=('lev', 'lat', 'lon') )
# ch4_avg_mconc[case] = ch4_total_mass[case] / total_tropo_vol[24:60]
# ch4_avg_nconc[case] = ch4_avg_mconc[case] / xmm_ch4 * Avog * 1.0e-6  # [molec cm-3]
# ch4_avg_ppb[case] = ch4_avg_nconc[case] / air_avg_nconc[24:60] * to_ppb
# mt_total_mass[case] = (ds[case]['GAS_TERP'][:, 0:ltropo+1, :, :] * \
    #   ds_deltaz3d['deltaz3d'][:, 0:ltropo+1, :, :] * \
    #   area).sum( dim=('lev', 'lat', 'lon') )
# mt_avg_mconc[case] = mt_total_mass[case] / total_tropo_vol[24:60]  # [kg m-3]
# mt_avg_nconc[case] = mt_avg_mconc[case] / xmm_mt * Avog * 1.0e-6  # [molec cm-3]
# mt_avg_ppb[case] = mt_avg_nconc[case] / air_avg_nconc[24:60] * to_ppb
# mt_avg_ppt[case] = mt_avg_nconc[case] / air_avg_nconc[24:60] * to_ppt

# l = 10
# print( (ds['E6C6']['GAS_CH4'][:, l, :, :] - ds['E0C6']['GAS_CH4'][:, l, :, :]).sum(dim=('lat', 'lon')) / ds['E0C6']['GAS_CH4'][:, l, :, :].sum(dim=('lat', 'lon')) )

# sys.exit()


# --------------------------------------------------------------- #
#
# Plot figures
#
# --------------------------------------------------------------- #

# ----- Plot time series of gas compounds ----- #
# gs = fg.add_gridspec(1, 2, left=0.05, right=0.9, bottom=0.05, top=0.95, \
#   wspace=0.15, hspace=0.0)
#
# gs0 = gs[0].subgridspec(2, 1, hspace=0.0)
# gs1 = gs[1].subgridspec(12, 1, wspace=0.0, hspace=0.0)

def plot_time_series():
  fg = plt.figure(figsize=(10, 12), constrained_layout=False, dpi=150)
  
  nrow = 4
  ncol = 1
  
  ax1 = fg.add_subplot(nrow, ncol, 1)
  print('gas_avg_ppb: ', gas_avg_ppb)
  gas_avg_ppb['BASE']['GAS_CH4'].plot(ax=ax1, label='BASE')
  gas_avg_ppb['E0C6']['GAS_CH4'].plot(ax=ax1, label='E0C6', alpha=0.5, linewidth=3)
  gas_avg_ppb['E6C6']['GAS_CH4'].plot(ax=ax1, label='E6C6', alpha=0.5, linewidth=3)
  ax1.set_ylabel('Global mean CH4 (ppb)')
  ax1.grid(True)
  ax1.legend()
  
  ax2 = fg.add_subplot(nrow, ncol, 2)
  gas_avg_ppt['BASE']['GAS_TERP'].plot(ax=ax2, label='BASE')
  gas_avg_ppt['E0C6']['GAS_TERP'].plot(ax=ax2, label='E0C6', alpha=0.5, linewidth=3)
  gas_avg_ppt['E6C6']['GAS_TERP'].plot(ax=ax2, label='E6C6', alpha=0.5, linewidth=3)
  ax2.set_ylabel('Global mean monoterpenes (ppt)')
  ax2.grid(True)
  ax2.legend()
  
  ax3 = fg.add_subplot(nrow, ncol, 3)
  gas_avg_nconc['BASE']['GAS_OH'].plot(ax=ax3, label='BASE')
  gas_avg_nconc['E0C6']['GAS_OH'].plot(ax=ax3, label='E0C6', alpha=0.5, linewidth=3)
  gas_avg_nconc['E6C6']['GAS_OH'].plot(ax=ax3, label='E6C6', alpha=0.5, linewidth=3)
  ax3.set_ylabel('Global mean OH (molec cm-3)')
  ax3.grid(True)
  ax3.legend()
  
  ax4 = fg.add_subplot(nrow, ncol, 4)
  l = 0
  print(gas_havg_nconc['BASE']['GAS_OH'][30, :])
  gas_havg_nconc['BASE']['GAS_OH'][:, l].plot(ax=ax4, label='BASE')
  gas_havg_nconc['E0C6']['GAS_OH'][:, l].plot(ax=ax4, label='E0C6', alpha=0.5, linewidth=3)
  gas_havg_nconc['E6C6']['GAS_OH'][:, l].plot(ax=ax4, label='E6C6', alpha=0.5, linewidth=3)
  ax4.set_ylabel('Surface OH (molec cm-3)')
  ax4.grid(True)
  ax4.legend()
  
  fg.tight_layout()
  fg.savefig('ch4_mt_oh.png')


# ----- Plot global patterns of gas compounds ----- #
# gas: CH4, TERP, OH
# level: 0, 2, 5, 10, 20, 33
# plots: 3x2
#   BASE     E0C6-BASE
#   E0C6     E6C6-BASE
#   E6C6     E6C6-E0C6

# gas_list = ['GAS_CH4', 'GAS_OH', 'GAS_TERP']
# level = 9
# cmap = plt.get_cmap('YlGn')
# norm = BoundaryNorm([0, 1, 2, 3, 4, 5, 8, 11, 15, 20], ncolors=cmap.N, clip=True)
# ax.coastlines(color='gray')
# ax.set_extent([lon_bounds[0],lon_bounds[1],15.0,80.0])
# gl = ax.gridlines(draw_labels=True)
# gl.ylocator = mticker.MultipleLocator(20)
# gl.top_labels = False
# 
# levs = np.arange(-10,11)
# norm = colors.TwoSlopeNorm(vmin=min(levs),vcenter=0,vmax=max(levs)) #make 0 midpoint of diverging colors
# cta = ax.contourf(lons,lats,tadv,levs[levs!=0],extend='both',cmap='bwr',norm=norm)
# plt.colorbar(cta,orientation='horizontal',pad=0.1,aspect=30,shrink=0.85)
# #erase the first '0' in the pressure levels smaller than 1000 hPa to plot the title
# if int(plevel[0])==0:
#     plevelstr = plevel[1:]
# else:
#     plevelstr = plevel

def plot_global_gas(gas, level, unit_label, unit_convert=1.0):
  # ----- Set parameters
  data_crs = projection=ccrs.PlateCarree()
  map_proj = projection=ccrs.PlateCarree()

  for i in range(12):
    im = i + 1
  
    # ----- Calculate data
    gas_month_base = ds['BASE'][gas][24 + i, level, :, :] * unit_convert
    gas_month_e0c6 = ds['E0C6'][gas][i, level, :, :] * unit_convert
    gas_month_e6c6 = ds['E6C6'][gas][i, level, :, :] * unit_convert
    gas_month_diff1 = (gas_month_e0c6 - gas_month_base)/gas_month_base * 100.0  # [%]
    gas_month_diff2 = (gas_month_e6c6 - gas_month_base)/gas_month_base * 100.0  # [%]
    gas_month_diff3 = (gas_month_e6c6 - gas_month_e0c6)/gas_month_e0c6 * 100.0  # [%]

    # ---- Start ploting figures

    # Create a figure
    fg = plt.figure(figsize=(10, 8), constrained_layout=False, dpi=150)
  
    # Set axes structure
    nrow = 3
    ncol = 2
  
    ax_base = fg.add_subplot(nrow, ncol, 1, projection=map_proj)
    ax_e0c6 = fg.add_subplot(nrow, ncol, 3, projection=map_proj)
    ax_e6c6 = fg.add_subplot(nrow, ncol, 5, projection=map_proj)

    ax_diff1 = fg.add_subplot(nrow, ncol, 2, projection=map_proj)
    ax_diff2 = fg.add_subplot(nrow, ncol, 4, projection=map_proj)
    ax_diff3 = fg.add_subplot(nrow, ncol, 6, projection=map_proj)

    ax_list = [ax_base, ax_diff1, ax_e0c6, ax_diff2, ax_e6c6, ax_diff3]


    # Plot the data
    hpcm_base = gas_month_base.plot.pcolormesh(ax=ax_base, label='BASE', \
      add_colorbar=False)
    ax_base.set_title('BASE')
  
    hpcm_e0c6 = gas_month_e0c6.plot.pcolormesh(ax=ax_e0c6, label='E0C6', \
      add_colorbar=False)
    ax_e0c6.set_title('E0C6')
  
    hpcm_e6c6 = gas_month_e6c6.plot.pcolormesh(ax=ax_e6c6, label='E6C6', \
      add_colorbar=False)
    ax_e6c6.set_title('E6C6')

    hpcm_diff1 = gas_month_diff1.plot.pcolormesh(ax=ax_diff1, label='(E0C6-BASE)/BASE', \
      add_colorbar=False)
    ax_diff1.set_title('(E0C6-BASE)/BASE')

    hpcm_diff2 = gas_month_diff2.plot.pcolormesh(ax=ax_diff2, label='(E6C6-BASE)/BASE', \
      add_colorbar=False)
    ax_diff2.set_title('(E6C6-BASE)/BASE')

    hpcm_diff3 = gas_month_diff3.plot.pcolormesh(ax=ax_diff3, label='(E6C6-E0C6)/E0C6', \
      add_colorbar=False)
    ax_diff3.set_title('(E6C6-E0C6)/E0C6')
  
    # Set general axes properties
    for a in ax_list:
      a.set_global()
      a.add_feature(cfeature.COASTLINE, linestyle='-')

    # Set figure properties
    fg.suptitle('{0}, Month: {1:02d}, Level: {2:02d}'.format(gas, im, level))
    # fg.tight_layout()

    # Adjust the figure structure and the axes positions
    fg.subplots_adjust(left=0.02, right=0.88, bottom=0.05, top=0.95, \
      wspace=0.21, hspace=0.05)

    # Left colorbar axes
    l, b, w, h = ax_e0c6.get_position().bounds
    cax_left = fg.add_axes([l+w+0.01, b-0.2*h, 0.02, 1.4*h])

    # Right colorbar axes
    l1, b1, w1, h1 = ax_diff1.get_position().bounds
    l2, b2, w2, h2 = ax_diff2.get_position().bounds
    cax_right1 = fg.add_axes([l1+w1+0.01, b2+0.5*h2, 0.02, (b1+0.5*h1)-(b2+0.5*h2)])

    # Right colorbar axes
    l3, b3, w3, h3 = ax_diff3.get_position().bounds
    cax_right2 = fg.add_axes([l3+w3+0.01, b3, 0.02, h3])

    # print('before: ', cax_left.get_position().bounds)
    cbar_left = fg.colorbar(hpcm_base, cax=cax_left)
    # print('after: ', cax_left.get_position().bounds)
    cbar_right1 = fg.colorbar(hpcm_diff1, cax=cax_right1)
    cbar_right2 = fg.colorbar(hpcm_diff3, cax=cax_right2)

    cax_left.set_ylabel(unit_label)
    cax_right1.set_ylabel('%')
    cax_right2.set_ylabel('%')

    # Save figure
    fg.savefig('{0}-level_{1:02d}-month_{2:02d}-reldiff.png'.format(gas, level, im))

    # Close the figure for better memory use
    plt.close(fg)


def plot_zonal_level(gas, unit_convert, cbar_label):
  """
  " Figure structure:
  "
  " raw      absdiff       reldiff
  "
  " BASE  |  E0C6-BASE  |  (E0C6-BASE)/BASE
  " ---------------------------------------
  " E0C6  |  E6C6-BASE  |  (E6C6-BASE)/BASE
  " ---------------------------------------
  " E6C6  |  E6C6-E0C6  |  (E6C6-E0C6)/E0C6
  "
  " Plot for each month
  "
  "   ^
  " l |
  " e |   zonal mean
  " v |
  " e |
  " l |
  "   |-------------->
  "       latitude
  """

  # ----- Set parameters
  data_crs = projection=ccrs.PlateCarree()
  map_proj = projection=ccrs.PlateCarree()

  for i in range(12):
    im = i + 1
    print(im)
  
    # ----- Calculate data
    gas_month_base = ds['BASE'][gas][24 + i, :, :, :].mean(dim='lon') * unit_convert
    gas_month_e0c6 = ds['E0C6'][gas][i, :, :, :].mean(dim='lon') * unit_convert
    gas_month_e6c6 = ds['E6C6'][gas][i, :, :, :].mean(dim='lon') * unit_convert
    gas_month_reldiff1 = (gas_month_e0c6 - gas_month_base)/gas_month_base  # [-]
    gas_month_reldiff2 = (gas_month_e6c6 - gas_month_base)/gas_month_base  # [-]
    gas_month_reldiff3 = (gas_month_e6c6 - gas_month_e0c6)/gas_month_e0c6  # [-]
    gas_month_absdiff1 = gas_month_e0c6 - gas_month_base
    gas_month_absdiff2 = gas_month_e6c6 - gas_month_base
    gas_month_absdiff3 = gas_month_e6c6 - gas_month_e0c6

    # ----- Read general data which are the same for all the cases
    lat = ds['BASE']['lat']
    lon = ds['BASE']['lon']
    lev = ds['BASE']['lev']
    lat_lev = np.tile(lat, (lev.size, 1))
    
    gph3D = ds_meteo['gph3D'][24 + i, :, :, :]
    gph3D_zonal_lev = gph3D.mean(dim=('lon'))
    pres = ds_meteo['pressure']
    pres_zonal = pres.mean(dim=('lon', 'lat'))

    # ---- Start ploting figures

    # Create a figure
    fg = plt.figure(figsize=(14, 8), constrained_layout=False, dpi=150)
  
    # Set axes structure
    nrow = 3
    ncol = 3
  
    ax_base = fg.add_subplot(nrow, ncol, 1)
    ax_e0c6 = fg.add_subplot(nrow, ncol, 4)
    ax_e6c6 = fg.add_subplot(nrow, ncol, 7)

    ax_absdiff1 = fg.add_subplot(nrow, ncol, 2)
    ax_absdiff2 = fg.add_subplot(nrow, ncol, 5)
    ax_absdiff3 = fg.add_subplot(nrow, ncol, 8)

    ax_reldiff1 = fg.add_subplot(nrow, ncol, 3)
    ax_reldiff2 = fg.add_subplot(nrow, ncol, 6)
    ax_reldiff3 = fg.add_subplot(nrow, ncol, 9)

    # Original dataset
    hpcm_base = ax_base.pcolormesh(lat_lev, gph3D_zonal_lev, gas_month_base)
    ax_base.set_title('BASE')

    hpcm_e0c6 = ax_e0c6.pcolormesh(lat_lev, gph3D_zonal_lev, gas_month_e0c6)
    ax_e0c6.set_title('E0C6')

    hpcm_e6c6 = ax_e6c6.pcolormesh(lat_lev, gph3D_zonal_lev, gas_month_e6c6)
    ax_e6c6.set_title('E6C6')


    # 3.1: DivergingNorm
    # 3.2: TwoSlopeNorm
    # divnorm = colors.DivergingNorm(vmin=-1, vcenter=0, vmax=1)
    # divnorm = colors.DivergingNorm(vcenter=0)


    # Absolute difference
    vabsmax = max( abs(gas_month_absdiff1.min().values), \
        abs(gas_month_absdiff1.max().values) )
    divnorm = colors.DivergingNorm(vmin=-vabsmax, vcenter=0, vmax=vabsmax)
    hpcm_absdiff1 = ax_absdiff1.pcolormesh( \
        lat_lev, gph3D_zonal_lev, gas_month_absdiff1, \
        norm=divnorm, cmap=plt.get_cmap('RdBu_r'))
    ax_absdiff1.set_title('E0C6-BASE')

    vabsmax = max( abs(gas_month_absdiff2.min().values), \
        abs(gas_month_absdiff2.max().values) )
    divnorm = colors.DivergingNorm(vmin=-vabsmax, vcenter=0, vmax=vabsmax)
    hpcm_absdiff2 = ax_absdiff2.pcolormesh( \
        lat_lev, gph3D_zonal_lev, gas_month_absdiff2, \
        norm=divnorm, cmap=plt.get_cmap('RdBu_r'))
    ax_absdiff2.set_title('E6C6-BASE')

    vabsmax = max( abs(gas_month_absdiff3.min().values), \
        abs(gas_month_absdiff3.max().values) )
    divnorm = colors.DivergingNorm(vmin=-vabsmax, vcenter=0, vmax=vabsmax)
    hpcm_absdiff3 = ax_absdiff3.pcolormesh( \
        lat_lev, gph3D_zonal_lev, gas_month_absdiff3, \
        norm=divnorm, cmap=plt.get_cmap('RdBu_r'))
    ax_absdiff3.set_title('E6C6-E0C6')


    # Relative difference
    vabsmax = max( abs(gas_month_reldiff1.min().values), \
        abs(gas_month_reldiff1.max().values) )
    divnorm = colors.DivergingNorm(vmin=-vabsmax, vcenter=0, vmax=vabsmax)
    hpcm_reldiff1 = ax_reldiff1.pcolormesh( \
        lat_lev, gph3D_zonal_lev, gas_month_reldiff1, \
        norm=divnorm, cmap=plt.get_cmap('RdBu_r'))
    ax_reldiff1.set_title('(E0C6-BASE)/BASE')

    vabsmax = max( abs(gas_month_reldiff2.min().values), \
        abs(gas_month_reldiff2.max().values) )
    divnorm = colors.DivergingNorm(vmin=-vabsmax, vcenter=0, vmax=vabsmax)
    hpcm_reldiff2 = ax_reldiff2.pcolormesh( \
        lat_lev, gph3D_zonal_lev, gas_month_reldiff2, \
        norm=divnorm, cmap=plt.get_cmap('RdBu_r'))
    ax_reldiff2.set_title('(E6C6-BASE)/BASE')

    vabsmax = max( abs(gas_month_reldiff3.min().values), \
        abs(gas_month_reldiff3.max().values) )
    divnorm = colors.DivergingNorm(vmin=-vabsmax, vcenter=0, vmax=vabsmax)
    hpcm_reldiff3 = ax_reldiff3.pcolormesh( \
        lat_lev, gph3D_zonal_lev, gas_month_reldiff3, \
        norm=divnorm, cmap=plt.get_cmap('RdBu_r'))
    ax_reldiff3.set_title('(E6C6-E0C6)/E0C6')

    for a in [ax_base, ax_e0c6, ax_e6c6]:
      a.set_ylabel('gph3D (m)')
  

    # Set figure properties
    fg.suptitle('{0}, Month: {1:02d}, Zonal mean vertically'.format(gas, im))

    # Adjust the figure structure and the axes positions
    fg.subplots_adjust(left=0.08, right=0.88, bottom=0.05, top=0.90, \
      wspace=0.70, hspace=0.3)

    # ----- Colorbars

    cbar_width = 0.01

    # Left colorbar axes
    ll, bl, wl, hl = ax_e0c6.get_position().bounds
    cax_left = fg.add_axes([ll+wl+0.01, bl-0.2*hl, cbar_width, 1.4*hl])
    cbar_left = fg.colorbar(hpcm_base, cax=cax_left)
    cax_left.set_ylabel(cbar_label)

    # Middle colorbar axes
    lm1, bm1, wm1, hm1 = ax_absdiff1.get_position().bounds
    lm2, bm2, wm2, hm2 = ax_absdiff2.get_position().bounds
    cax_middle1 = fg.add_axes([lm1+wm1+0.01, bm2+0.5*hm2, \
      cbar_width, (bm1+0.5*hm1)-(bm2+0.5*hm2)])
    cbar_middle1 = fg.colorbar(hpcm_absdiff1, cax=cax_middle1)
    cax_middle1.set_ylabel(cbar_label)

    lm3, bm3, wm3, hm3 = ax_absdiff3.get_position().bounds
    cax_middle2 = fg.add_axes([lm3+wm3+0.01, bm3, cbar_width, hm3])
    cbar_middle2 = fg.colorbar(hpcm_absdiff3, cax=cax_middle2)
    cax_middle2.set_ylabel(cbar_label)

    # Right colorbar axes
    lr1, br1, wr1, hr1 = ax_reldiff1.get_position().bounds
    lr2, br2, wr2, hr2 = ax_reldiff2.get_position().bounds
    cax_right1 = fg.add_axes([lr1+wr1+0.01, br2+0.5*hr2, \
      cbar_width, (br1+0.5*hr1)-(br2+0.5*hr2)])
    cbar_right1 = fg.colorbar(hpcm_reldiff1, cax=cax_right1)
    # cax_right1.set_ylabel('%')

    # Right colorbar axes
    lr3, br3, wr3, hr3 = ax_reldiff3.get_position().bounds
    cax_right2 = fg.add_axes([lr3+wr3+0.01, br3, cbar_width, hr3])
    cbar_right2 = fg.colorbar(hpcm_reldiff3, cax=cax_right2)
    # cax_right2.set_ylabel('%')

    # Save figure
    fg.savefig('zonal_mean_lat_lev/zonal_mean-{0}-month_{1:02d}-diff.png'.format( \
      gas, im))

    # Close the figure for better memory use
    plt.close(fg)


def plot_zonal_mean_at_levels(gas, unit_convert, ylabel):
  """
  " Figure structure:
  "
  " raw      absdiff       reldiff
  "
  " BASE  |  E0C6-BASE  |  (E0C6-BASE)/BASE
  " ---------------------------------------
  " E0C6  |  E6C6-BASE  |  (E6C6-BASE)/BASE
  " ---------------------------------------
  " E6C6  |  E6C6-E0C6  |  (E6C6-E0C6)/E0C6
  "
  " Plot for each month
  "
  "   ^
  "   |
  " c |  time series at
  " o |  different levels
  " n |
  " c |
  "   |-------------->
  "       latitude
  """

  # ----- Set parameters
  data_crs = projection=ccrs.PlateCarree()
  map_proj = projection=ccrs.PlateCarree()

  for i in range(12):
    im = i + 1
    print(im)
  
    # ----- Calculate data
    gas_month_base = ds['BASE'][gas][24 + i, :, :, :].mean(dim='lon') * unit_convert
    gas_month_e0c6 = ds['E0C6'][gas][i, :, :, :].mean(dim='lon') * unit_convert
    gas_month_e6c6 = ds['E6C6'][gas][i, :, :, :].mean(dim='lon') * unit_convert
    gas_month_reldiff1 = (gas_month_e0c6 - gas_month_base)/gas_month_base  # [%]
    gas_month_reldiff2 = (gas_month_e6c6 - gas_month_base)/gas_month_base  # [%]
    gas_month_reldiff3 = (gas_month_e6c6 - gas_month_e0c6)/gas_month_e0c6  # [%]
    gas_month_absdiff1 = gas_month_e0c6 - gas_month_base
    gas_month_absdiff2 = gas_month_e6c6 - gas_month_base
    gas_month_absdiff3 = gas_month_e6c6 - gas_month_e0c6

    # ----- Read general data which are the same for all the cases
    lat = ds['BASE']['lat']
    lon = ds['BASE']['lon']
    lev = ds['BASE']['lev']
    lat_lev = np.tile(lat, (lev.size, 1))
    
    gph3D = ds_meteo['gph3D'][24 + i, :, :, :]
    gph3D_zonal_lev = gph3D.mean(dim=('lon'))
    pres = ds_meteo['pressure']
    pres_zonal = pres.mean(dim=('lon', 'lat'))

    # ---- Start ploting figures

    # Create a figure
    fg = plt.figure(figsize=(14, 8), constrained_layout=False, dpi=150)
  
    # Set axes structure
    nrow = 3
    ncol = 3
  
    ax_base = fg.add_subplot(nrow, ncol, 1)
    ax_e0c6 = fg.add_subplot(nrow, ncol, 4)
    ax_e6c6 = fg.add_subplot(nrow, ncol, 7)

    ax_absdiff1 = fg.add_subplot(nrow, ncol, 2)
    ax_absdiff2 = fg.add_subplot(nrow, ncol, 5)
    ax_absdiff3 = fg.add_subplot(nrow, ncol, 8)

    ax_reldiff1 = fg.add_subplot(nrow, ncol, 3)
    ax_reldiff2 = fg.add_subplot(nrow, ncol, 6)
    ax_reldiff3 = fg.add_subplot(nrow, ncol, 9)

    plot_ilevs = [0, 5, 10, 20, 30]

    # Original dataset
    for il in plot_ilevs:
      ax_base.plot(lat, gas_month_base[il, :], \
          label='{0:4.1f} km'.format(gph3D_zonal_lev[il, :].mean().values/1.0e3))
      ax_e0c6.plot(lat, gas_month_e0c6[il, :])
      ax_e6c6.plot(lat, gas_month_e6c6[il, :])

    ax_base.set_title('BASE')
    ax_e0c6.set_title('E0C6')
    ax_e6c6.set_title('E6C6')

    for a in [ax_base, ax_e0c6, ax_e6c6]:
      a.set_ylabel(ylabel)

    ax_base.grid(True)
    ax_e0c6.grid(True)
    ax_e6c6.grid(True)

    ax_base.legend()  # only show legend once

    # Absolute difference
    for il in plot_ilevs:
      ax_absdiff1.plot(lat, gas_month_absdiff1[il, :])
      ax_absdiff2.plot(lat, gas_month_absdiff2[il, :])
      ax_absdiff3.plot(lat, gas_month_absdiff3[il, :])

    ax_absdiff1.set_title('E0C6-BASE')
    ax_absdiff2.set_title('E6C6-BASE')
    ax_absdiff3.set_title('E6C6-E0C6')

    ax_absdiff1.grid(True)
    ax_absdiff2.grid(True)
    ax_absdiff3.grid(True)


    # Relative difference
    for il in plot_ilevs:
      ax_reldiff1.plot(lat, gas_month_reldiff1[il, :])
      ax_reldiff2.plot(lat, gas_month_reldiff2[il, :])
      ax_reldiff3.plot(lat, gas_month_reldiff3[il, :])

    ax_reldiff1.set_title('(E0C6-BASE)/BASE')
    ax_reldiff2.set_title('(E6C6-BASE)/BASE')
    ax_reldiff3.set_title('(E6C6-E0C6)/E0C6')

    ax_reldiff1.grid(True)
    ax_reldiff2.grid(True)
    ax_reldiff3.grid(True)
  
    # Set figure properties
    fg.suptitle('{0}, Month: {1:02d}, Zonal mean at different levels'.format(gas, im))

    # Adjust the figure structure and the axes positions
    fg.subplots_adjust(left=0.08, right=0.92, bottom=0.05, top=0.90, \
      wspace=0.55, hspace=0.3)

    # Save figure
    fg.savefig('zonal_mean_lat_lev/zonal_mean_at_levels-{0}-month_{1:02d}-diff.png'.format( \
      gas, im))

    # Close the figure for better memory use
    plt.close(fg)


# Call the plot functions
# plot_time_series()
plot_global_gas('GAS_OH', 0, unit_label=r'[OH] (10$^6$ molec cm$^{-3}$)', \
  unit_convert=1.0/xmm_oh * Avog * 1.0e-6 * 1.0e-6)  # 10^6 molec cm-3
plot_global_gas('GAS_TERP', 0, unit_label=r'[TERP] (10$^{10}$ molec cm$^{-3}$)', \
  unit_convert=1.0/xmm_mt * Avog * 1.0e-6 * 1.0e-10)  # 10^10 molec cm-3
plot_global_gas('GAS_CH4', 0, unit_label=r'[CH4] (10$^{12}$ molec cm$^{-3}$)', \
  unit_convert=1.0/xmm_ch4 * Avog * 1.0e-6 * 1.0e-12)  # 10^12 molec cm-3

# 10^6 molec cm-3
# plot_zonal_level('GAS_OH', \
#   unit_convert=1.0/xmm_oh * Avog * 1.0e-6 * 1.0e-6, \
#   cbar_label=r'[OH] (10$^6$ molec cm$^{-3}$)')

# 10^12 molec cm-3
# plot_zonal_level('GAS_CH4', \
#   unit_convert=1.0/xmm_ch4 * Avog * 1.0e-6 * 1.0e-12, \
#   cbar_label=r'[CH4] (10$^{12}$ molec cm$^{-3}$)')

# 10^10 molec cm-3
# plot_zonal_level('GAS_TERP', \
#   unit_convert=1.0/xmm_mt * Avog * 1.0e-6 * 1.0e-10, \
#   cbar_label=r'[TERP] (10$^{10}$ molec cm$^{-3}$)')

# 10^6 molec cm-3
# plot_zonal_mean_at_levels('GAS_OH', \
#   unit_convert=1.0/xmm_oh * Avog * 1.0e-6 * 1.0e-6, \
#   ylabel=r'[OH] (10$^6$ molec cm$^{-3}$)')

# 10^12 molec cm-3
# plot_zonal_mean_at_levels('GAS_CH4', \
#   unit_convert=1.0/xmm_ch4 * Avog * 1.0e-6 * 1.0e-12, \
#   ylabel=r'[CH4] (10$^{12}$ molec cm$^{-3}$)')

# 10^10 molec cm-3
# plot_zonal_mean_at_levels('GAS_TERP', \
#   unit_convert=1.0/xmm_mt * Avog * 1.0e-6 * 1.0e-10, \
#   ylabel=r'[TERP] (10$^{10}$ molec cm$^{-3}$)')
