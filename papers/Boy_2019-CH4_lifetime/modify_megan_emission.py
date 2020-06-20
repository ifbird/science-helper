import sys
sys.path.insert(0, '/users/putian/scripts/science-helper/pypack')

import xarray as xr
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import BoundaryNorm
import matplotlib.patches as mpatches

# pypack
from tm5_parameters import tm5
import constants

# Put the data in data_folder
data_folder = '/scratch/project_2001025/putian/Boy_2019-CH4_lifetime'

# Read MEGAN input file for monoterpenes in 2009
# From the calculation in sosaa_case_comparison.py, we found the emission rate
# of monoterpenes increased by 71.6% in E6C0 and E6C6 than the BASE case,
# it is the same in every month.
megan_folder = '/scratch/project_2001025/tm5mp/TM5_EMISS/MEGAN'
megan_mt_file = 'MEGAN-MACC_biogenic_2009_monoterpenes.nc'
megan_mt_xrds = xr.open_dataset(megan_folder + '/' + megan_mt_file)
megan_mt_xrds_new = megan_mt_xrds.copy(deep=True)
emirate_ratio = 1.716

# tm5 vegetation data: needle leaf tree cover sum
tmp_xrda = xr.open_dataset(data_folder + '/tm5_needleleaf_tree_cover_annual_sum.nc') \
    ['needleleaf_tree_cover_annual_sum']

# Boreal forest in TM5 in this case: needleleaf trees exist anytime in 2009,
# and lat>=50 N
tm5_boreal_forest = xr.where(tmp_xrda > 0.0, 1, 0)
tm5_boreal_forest = xr.where(tm5_boreal_forest.lat >= 50.0, tm5_boreal_forest, 0)

# Extend tm5_boreal_forest to include the periodic boundary condition in the
# west-east direction, and north and south poles, this is convenient for the
# interpolation.
lon_tm5 = tm5_boreal_forest.lon
lat_tm5 = tm5_boreal_forest.lat
lon_ext = np.append( np.append([-180.5,], tm5_boreal_forest.lon.values), [180.5,] )
lat_ext = np.append( np.append([-90,], tm5_boreal_forest.lat.values), [90,] )
data_ext = np.zeros( (lat_tm5.size + 2, lon_tm5.size + 2) )
data_ext[1:-1, 0] = tm5_boreal_forest.values[:, -1]  # data at lon -180.5
data_ext[1:-1, -1] = tm5_boreal_forest.values[:, 0]  # data at lon 180.5
data_ext[0, :] = 0.0  # south pole
data_ext[-1, :] = 0.0  # north pole
data_ext[1:-1, 1:-1] = tm5_boreal_forest.values
tm5_boreal_forest_extend = xr.DataArray(data_ext, \
    coords=[lat_ext, lon_ext], dims=['lat', 'lon'])

# Interpolate tm5_boreal_forest_extend (1x1) to megan emission data grid (0.5x0.5)
megan_boreal_forest = tm5_boreal_forest_extend.interp( \
    lat=megan_mt_xrds.lat, lon=megan_mt_xrds.lon, \
    method='nearest')

# Modify emission rate data according to boreal forest region

for i in range(12):  # loop for 12 months
  megan_mt_xrds_new['MEGAN_MACC'][i, :, :] = xr.where( \
      megan_boreal_forest>0, \
      megan_mt_xrds_new['MEGAN_MACC'][i, :, :] * emirate_ratio, \
      megan_mt_xrds_new['MEGAN_MACC'][i, :, :])

# Save new megan emission rate data
data_folder = '/scratch/project_2001025/putian/Boy_2019-CH4_lifetime'
megan_mt_xrds_new.to_netcdf(data_folder + '/E6C6-MEGAN-MACC_biogenic_2009_monoterpenes.nc')


# ================================================================ #
#
# Plot figures
#
# ================================================================ #

# ------- Plot all ----------------------------


fg = plt.figure(figsize=(12, 6), constrained_layout=False, dpi=150)
gs = fg.add_gridspec(1, 2, left=0.05, right=0.9, bottom=0.05, top=0.95, \
    wspace=0.15, hspace=0.0)

gs0 = gs[0].subgridspec(2, 1, hspace=0.0)
gs1 = gs[1].subgridspec(12, 1, wspace=0.0, hspace=0.0)


# ===== tm5 boreal forest ===== #
ax_tm5 = fg.add_subplot(gs0[0, 0], projection=ccrs.PlateCarree())
tm5_boreal_forest.plot.pcolormesh(ax=ax_tm5, \
    levels=[0, 0.5, 1.5], colors=['#ffffff00', '#228b22'], \
    add_colorbar=False)
ax_tm5.set_title('Boreal forest in TM5 grid (1x1)', fontsize=10)


# ===== megan boreal forest ===== #
ax_meg = fg.add_subplot(gs0[1, 0], projection=ccrs.PlateCarree())
megan_boreal_forest.plot.pcolormesh(ax=ax_meg, \
  levels=[0, 0.5, 1.5], colors=['#ffffff00', '#228b22'], \
  add_colorbar=False)
ax_meg.set_title('Boreal forest in MEGAN grid (0.5x0.5)', fontsize=10)


# ===== Adjust axes properties for ax_tm5 and ax_meg ===== #
for a in [ax_tm5, ax_meg]:
  a.set_global()
  a.add_feature(cfeature.COASTLINE, linewidth=0.3)
  gl = a.gridlines()
  gl.xlabels_bottom = True
  gl.ylabels_left = True
  gl.xlocator = mticker.FixedLocator([-180, -120, -60, 0, 60, 120, 180])
  gl.ylocator = mticker.FixedLocator([-90, -50, 0, 50, 90])
  gl.xlabel_style = {'size': 8}
  gl.ylabel_style = {'size': 8}

  # Check axes boundaries
  # rect = mpatches.Rectangle((0, 0), width=1, height=1, \
  #                        transform=a.transAxes, color='yellow', \
  #                        alpha=0.5, zorder=5)
  # a.add_patch(rect)


# ===== Emission rate difference in each month =====#
ax_emidiff = [None]*12  # for 12 months
cmap = plt.get_cmap('YlGn')
# norm = BoundaryNorm([0, 2, 4, 6, 8, 10, 12, 14, 16], ncolors=cmap.N, clip=True)
norm = BoundaryNorm([0, 1, 2, 3, 4, 5, 8, 11, 15, 20], ncolors=cmap.N, clip=True)
for row in range(12):
  ax_emidiff[row] = fg.add_subplot(gs1[row, 0], projection=ccrs.PlateCarree())
  
  # Calculate megan mt emission rate difference
  megan_mt_diff_tmp = (megan_mt_xrds_new['MEGAN_MACC'][row, :, :] - \
    megan_mt_xrds['MEGAN_MACC'][row, :, :]) \
    * 86400.0 * 1.0e6 * constants.monthday[row]
  # megan_mt_diff_tmp.plot.pcolormesh(ax=ax_emidiff[row], \
  #   levels=10, \
  #   add_colorbar=False)
  hpcm = ax_emidiff[row].pcolormesh( \
      megan_mt_diff_tmp.lon, megan_mt_diff_tmp.lat, \
      megan_mt_diff_tmp, \
      norm=norm, \
      cmap=plt.get_cmap('YlGn'))

  # Set the axes properties
  ax_emidiff[row].set_xticks([])
  ax_emidiff[row].set_yticks([])
  ax_emidiff[row].set_xlabel('')
  ax_emidiff[row].set_ylabel('{0}'.format(row+1))
  ax_emidiff[row].set_extent([-180, 180, 50, 90])
  ax_emidiff[row].add_feature(cfeature.COASTLINE, linewidth=0.3)

  # Add a rectangle patch to show the axes boundary
  # rect = mpatches.Rectangle((0, 0), width=1, height=1, \
  #                        transform=ax_emidiff[row].transAxes, color='yellow', \
  #                        alpha=0.5, zorder=5)
  # ax_emidiff[row].add_patch(rect)

ax_emidiff[0].set_title('MT emission rate: E6C6-BASE', fontsize=9)

# Add colorbar to megan emission rate difference
cax = fg.add_axes([0.92, 0.25, 0.02, 0.5])
cbar = fg.colorbar(hpcm, cmap=cmap, cax=cax, orientation='vertical')
cbar.ax.get_yaxis().labelpad = 15  # prevent ylabel overlapped with yticklabels
cbar.ax.set_ylabel(r'Monoterpene emission rate difference (mg m$^{-2}$ mon$^{-1}$)', \
    rotation=270)

# Save the figure
fg.savefig('all.png')
