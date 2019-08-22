#==============================================================================#
#
# Plot for the poster used in EC-Earth meeting in Lisbon
#
#==============================================================================#

#
# Import header
#
import sys

from netCDF4 import Dataset

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
data1 = np.load('data1_reg11.npz')
cv_pi_lu2018 = data1['lu2018_pi'    ][()]['cv_dom_avg_reg11'][:, 1, ::-1, :]
cv_mh_lu2018 = data1['lu2018_mh'    ][()]['cv_dom_avg_reg11'][:, 1, ::-1, :]
cv_mhgsrd_lu2018 = data1['lu2018_mhgsrd'][()]['cv_dom_avg_reg11'][:, 1, ::-1, :]

cvh_pi_lu2018 = np.sum( cv_pi_lu2018[lf.tm5_veg_high-1, :, :], axis=0 )
cvh_mh_lu2018 = np.sum( cv_mh_lu2018[lf.tm5_veg_high-1, :, :], axis=0 )
cvh_mhgsrd_lu2018 = np.sum( cv_mhgsrd_lu2018[lf.tm5_veg_high-1, :, :], axis=0 )

ind_low = np.array([2, 7])
cvl_pi_lu2018 = np.sum( cv_pi_lu2018[ind_low-1, :, :], axis=0 )
cvl_mh_lu2018 = np.sum( cv_mh_lu2018[ind_low-1, :, :], axis=0 )
cvl_mhgsrd_lu2018 = np.sum( cv_mhgsrd_lu2018[ind_low-1, :, :], axis=0 )


# lon_lu2018 = data1['lu2018_pi'][()]['lon_reg11']
# lat_lu2018 = data1['lu2018_pi'][()]['lat_reg11'][::-1]


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

lon, lat = input_pi['lon'], input_pi['lat']
nlon, nlat = lon.size, lat.size

# Real coverage percent of each veg type
# cv_pi_input = np.copy(tv_pi_input)
# cv_pi_input[lf.tm5_veg_high-1, :, :] = tv_pi_input[lf.tm5_veg_high-1, :, :] * cvh_pi_input[np.newaxis, :, :]
# cv_pi_input[lf.tm5_veg_low -1, :, :] = tv_pi_input[lf.tm5_veg_low -1, :, :] * cvl_pi_input[np.newaxis, :, :]
# 
# cv_mh_input = np.copy(tv_mh_input)
# cv_mh_input[lf.tm5_veg_high-1, :, :] = tv_mh_input[lf.tm5_veg_high-1, :, :] * cvh_mh_input[np.newaxis, :, :]
# cv_mh_input[lf.tm5_veg_low -1, :, :] = tv_mh_input[lf.tm5_veg_low -1, :, :] * cvl_mh_input[np.newaxis, :, :]
# 
# cv_mhgsrd_input = np.copy(tv_mhgsrd_input)
# cv_mhgsrd_input[lf.tm5_veg_high-1, :, :] = tv_mhgsrd_input[lf.tm5_veg_high-1, :, :] * cvh_mhgsrd_input[np.newaxis, :, :]
# cv_mhgsrd_input[lf.tm5_veg_low -1, :, :] = tv_mhgsrd_input[lf.tm5_veg_low -1, :, :] * cvl_mhgsrd_input[np.newaxis, :, :]


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


##### dust load
# Files of three cases
fname_dl_pi     = '/wrk/putian/tm5-mp-1850/rundir/output/aerocom3_TM5_JPK_global_200902_monthly.nc'
fname_dl_mh     = '/wrk/putian/tm5-mp-mh/rundir/output/aerocom3_TM5_JPK_global_200902_monthly.nc'
fname_dl_mhgsrd = '/wrk/putian/tm5-mp-mhgsrd/rundir/output/aerocom3_TM5_JPK_global_200902_monthly.nc'

# Read data from files
fid_dl_pi = Dataset(fname_dl_pi, 'r')
fid_dl_mh = Dataset(fname_dl_mh, 'r')
fid_dl_mhgsrd = Dataset(fname_dl_mhgsrd, 'r')

lon_dl, lat_dl = fid_dl_pi.variables['lon'][:], fid_dl_pi.variables['lat'][:]
dl_pi = np.squeeze( fid_dl_pi.variables['loaddust'][:] )*1.0e3  # [g m-2]
dl_mh = np.squeeze( fid_dl_mh.variables['loaddust'][:] )*1.0e3  # [g m-2]
dl_mhgsrd = np.squeeze( fid_dl_mhgsrd.variables['loaddust'][:] )*1.0e3  # [g m-2]

cm_dl = plt.get_cmap('autumn_r')


#
# Plot the data
#
DPI = lf.DPI
pm = 'cyl'

##### Plot vegetation cover
reg = lf.reg_wafr
xpm, ypm = lf.ll_to_xy_for_map_pcolor(lon, lat, pm, reg)

fg, ax = plt.subplots(3, 2, figsize=(12, 12), dpi=DPI)


#----- mhgsrd -----#
m = lf.plot_map(ax[0,0], pm, reg)
z = cvh_mhgsrd_lu2018
zm = ma.array(z, mask= z<0.2)
h = m.pcolormesh(xpm, ypm, zm, zorder=3)

m = lf.plot_map(ax[0,1], pm, reg)
z = cvl_mhgsrd_lu2018
zm = ma.array(z, mask= z==0)
h = m.pcolormesh(xpm, ypm, zm, zorder=3)


#----- mh -----#
m = lf.plot_map(ax[1,0], pm, reg)
z = cvh_mh_lu2018
zm = ma.array(z, mask= z<0.2)
h = m.pcolormesh(xpm, ypm, zm, zorder=3)

m = lf.plot_map(ax[1,1], pm, reg)
z = cvl_mh_lu2018
zm = ma.array(z, mask= z==0)
h = m.pcolormesh(xpm, ypm, zm, zorder=3)


#----- pi -----#
m = lf.plot_map(ax[2,0], pm, reg)
z = cvh_pi_lu2018
zm = ma.array(z, mask= z<0.2)
h = m.pcolormesh(xpm, ypm, zm, zorder=3)

m = lf.plot_map(ax[2,1], pm, reg)
z = cvl_pi_lu2018
zm = ma.array(z, mask= z==0)
h = m.pcolormesh(xpm, ypm, zm, zorder=3)


# save the figure
# fg.tight_layout()
fg.subplots_adjust(hspace=0.2, wspace=0.2)
fg.tight_layout()
fg.savefig('./figures/poster_cvh_cvl.png', dpi=DPI)

sys.exit()


##### Plot dust load
pm = 'cyl'
reg = lf.reg_glob
vmin, vmax = 0.0, 1.5
vm = 0.05
cm = plt.get_cmap('autumn_r')

xpm, ypm = lf.ll_to_xy_for_map_pcolor(lon_dl, lat_dl, pm, reg)

fg, ax = plt.subplots(3, 1, figsize=(10, 12), dpi=DPI)


#----- mhgsrd -----#
m = lf.plot_map(ax[0], pm, reg)
z = dl_mhgsrd
zm = ma.array(z, mask=z<vm)
h1 = m.pcolormesh(xpm, ypm, zm, vmin=vmin, vmax=vmax, cmap=cm, zorder=3)
cb1 = m.colorbar(h1, 'right')


#----- mh -----#
m = lf.plot_map(ax[1], pm, reg)
z = dl_mh
zm = ma.array(z, mask=z<vm)
h2 = m.pcolormesh(xpm, ypm, zm, vmin=vmin, vmax=vmax, cmap=cm, zorder=3)
cb2 = m.colorbar(h2, 'right')


#----- pi -----#
m = lf.plot_map(ax[2], pm, reg)
z = dl_pi
zm = ma.array(z, mask=z<vm)
h3 = m.pcolormesh(xpm, ypm, zm, vmin=vmin, vmax=vmax, cmap=cm, zorder=3)
cb3 = m.colorbar(h3, 'right')

# save the figure
fg.tight_layout()
fg.savefig('./figures/poster_dustload.png', dpi=DPI)
