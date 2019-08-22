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
# print('Reading Lu2018 data for MH ...')
# lu2018_mh     = lfunc.read_Lu2018_lpjg_data(dir_lu2018_data + '/LPJ-GUESS_monthlyoutput_MH.txt'    )
# print('Reading Lu2018 data for MHgsrd ...')
# lu2018_mhgsrd = lfunc.read_Lu2018_lpjg_data(dir_lu2018_data + '/LPJ-GUESS_monthlyoutput_MHgsrd.txt')


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
# lon and lat for each grid
#

# Land RG grid
lon_land = lu2018_pi['lon'][-1, :]
lat_land = lu2018_pi['lat'][-1, :]

# Global RG grid
lon_glob, lat_glob = lfunc.generate_global_reduced_gaussian_grid(lfunc.nlon_N80, lfunc.lat_N80)

# Global regular 1x1 grid
lon_reg11 = np.linspace(-179.5, 179.5, 360)
lat_reg11 = np.linspace(89.5, -89.5, 180)
nlon_reg11 = lon_reg11.size
nlat_reg11 = lat_reg11.size
lu2018_pi['lon_reg11'] = lon_reg11
lu2018_pi['lat_reg11'] = lat_reg11

# Global regular lon with reduced Gaussian lat
lon_regrg = np.copy(lon_reg11)
lat_regrg = np.copy(lat_glob)
nlon_regrg = lon_regrg.size
nlat_regrg = lat_regrg.size
lu2018_pi['lon_regrg'] = lon_regrg
lu2018_pi['lat_regrg'] = lat_regrg

# Land ind in global grid for RG grid
land_ind = lfunc.get_land_ind_in_glob_reduced_gaussian_grid(lon_land, lat_land, lon_glob, lat_glob)

#
# Start interpolation
#

# Initiate data array
lu2018_pi['cv_dom_avg_regrg'] = np.zeros((nvt, nmon, nlat_regrg, nlon_regrg))
lu2018_pi['cv_dom_avg_reg11'] = np.zeros((nvt, nmon, nlat_reg11, nlon_reg11))

# Loop for each veg type and month
for iv in range(nvt):
  for im in range(nmon):
    print('veg: {0}, month: {1}'.format(iv, im))
    lu2018_pi['cv_dom_avg_regrg'][int(iv), int(im), :, :], lu2018_pi['cv_dom_avg_reg11'][int(iv), int(im), :, :] = \
      lfunc.interp_part_reduced_gaussian_regular_grid(lon_land, lat_land, land_ind, lu2018_pi['cv_dom_avg'][int(iv), int(im), :], \
      lon_glob, lat_glob, lon_regrg, lat_regrg, lon_reg11, lat_reg11)

#
# Plot figures to show the data
#
# ------------------------------------------------
# |  global high veg    |  global low veg        |
# ------------------------------------------------
# |  west African high  |  west African low veg  |
# ------------------------------------------------
#
# west Africa: 20W-50E, 5S-40N
#

# Color list for different vegetation types
veg_color = [ \
  'goldenrod', # L, Crops, mixed farming
  'limegreen', # L, Short grass
  'olivedrab', # H, Evergreen needleleaf trees
  'yellowgreen', # H, Deciduous needleleaf trees
  'seagreen', # H, Deciduous broadleaf trees
  'green', # H, Evergreen broadleaf trees
  'green', # L, Tall grass
  'gold', # -, Desert
  'silver', # L, Tundra
  'goldenrod', # L, Irrigated crops
  'darkgoldenrod', # L, Semidesert
  'snow', # -, Ice caps and glaciers
  'darkturquoise', # L, Bogs and marshes
  'blue', # -, Inland water
  'royalblue', # -, Ocean
  'firebrick', # L, Evergreen shrubs
  'tomato', # L, Deciduous shrubs
  'green', # H, Mixed forest/woodland
  'green', # H, Interrupted forest
  'teal', # L, Water and land mixtures
  ]

# Region parameters
reg_glob = (-90, 90, -180, 180)  # global
reg_wafr = ( -5, 40,  -20,  50)  # west Africa

#===== PI =====#
print('Plotting Lu2018 data for PI ...')

# Plot cv_dom_avg
# lfunc.plot_cv_dom_avg(lu2018_pi, './figures/pi')

# Plot cv_dom_avg_reg11
lfunc.plot_cv_dom_avg_reg(lu2018_pi, './figures/pi_reg11')

sys.exit()


##### cf from data['cvl'], data['cvh'] and data['cf']
iyear = 9
imon = 5

## Low vegetation
for v in lu2018_pi['vtl_set']:
  print(v)

  # Initiate figure
  fg, ax = plt.subplots(2, 1, figsize=(12, 12), dpi=150)

  # cvl
  # Initiate map
  m = plot_map(ax[0], reg_glob)

  # Convert lon lat to x y coordinates
  x, y = m(lu2018_pi['lon'][iyear, :], lu2018_pi['lat'][iyear, :])
  z = lu2018_pi['cvl'][iyear, imon, :]
  mask = lu2018_pi['vtl'][iyear, :] == v

  im1 = m.scatter(x[mask], y[mask], c=z[mask], zorder=3)

  # cv
  # Initiate map
  m = plot_map(ax[1], reg_glob)

  # Convert lon lat to x y coordinates
  z = lu2018_pi['cv'][iyear, imon, int(v-1), :]

  im1 = m.scatter(x, y, c=z, zorder=3)


  fg.savefig('{0}{1:02d}.png'.format('pi_cv', int(v)), dpi=150)

# cmap = colors.ListedColormap(veg_color)
# im1 = m.scatter(x, y, c=mask_z, s=2, cmap=cmap, zorder=3)
# im1 = m.scatter(x, y, c=mask_z, cmap=cmap, zorder=3)
# im1 = m.scatter(x, y, c=lu2018_pi['vth'][-1, :], cmap=cmap, zorder=3)
# cb1 = m.colorbar(im1, "right", size="5%", pad='2%')
# m.pcolormesh(lon, lat, vtl_regular_nearest, zorder=3, alpha=0.6)

