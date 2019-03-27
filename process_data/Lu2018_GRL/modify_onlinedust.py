import sys

import shutil

# import netCDF4 as netcdf
from netCDF4 import Dataset

import numpy as np
import numpy.ma as ma

from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import putian_functions as pf
import local_functions as lf


#
# Path of onlinedust_4.nc (now it is netCDF file)
# Original path: /proj/atm/EC-Earth/input-trunk-r5801/tm5/TM5_INPUT/aerosols/Dust/ONLINE/
# Here the file ../data/tm5_input_modified/onlinedust_4.nc will be modified.
#
# NETCDF4 data model, file format HDF5
# institution: KNMI (Royal Netherlands Meteorological Institute, De Bilt, The Netherlands)
# title: Online dust emission input fields
# contact: Achim Strunk (KNMI); strunk@knmi.nl
# institude_id: KNMI
# comment: produced from single hdf/txt files provided by E. Vignati
# history: Fri Jul  6 10:56:50 2012: ncks -4 onlinedust.nc onlinedust_4.nc
# created Mon Dec 12 19:22:17 2011 by IDL ncdf_write
# NCO: 4.0.8
# dimensions(sizes): lat(180), lon(360), nfpar(12), nsoilph(5), nz0(13)
# variables(dimensions): float32 area(lat,lon), float32 cult(lat,lon), float32 fpar(nfpar,lat,lon), float32 lat(lat), float32 lon(lon),
#                        float32 potsrc(lat,lon), float32 soilph(nsoilph,lat,lon), float32 soiltype(lat,lon), float64 z0(nz0,lat,lon)
#

fdir = '../data/tm5_input_modified'
fname_raw = fdir + '/onlinedust_4.nc'

# Load data3
data3 = np.load('data3_input.npz')

##### Modify for MH_gsrd

# Copy a new file from the raw data file to modify
fname_mhgsrd = fdir + '/onlinedust_4_mhgsrd.nc'
shutil.copyfile(fname_raw, fname_mhgsrd)

# Open the file with read and write permissions
fid = Dataset(fname_mhgsrd, 'r+')

# Read data
lon, lat = fid.variables['lon'][:], fid.variables['lat'][:]
nlon, nlat = lon.size, lat.size  # 360, 180
potsrc = np.copy(fid.variables['potsrc'][:])  # [nlat, nlon]
cult   = np.copy(fid.variables['cult'][:])  # [nlat, nlon]
soilph = np.copy(fid.variables['soilph'][:])  # [nsoilph, nlat, nlon]
nsoilph = np.size(soilph, axis=0)

# Region mask
regm_lat = (lat>=10) & (lat<=30)
regm_lon = (lon>=-20) & (lon<=40)

#----- Modify potsrc -----#
# Set all the potsrc in the region 20W-40E, 10N-30N to 0,
# representing they are no longer potential dust sources but lakes in MH.
potsrc[np.ix_(regm_lat, regm_lon)] = 0.0  # select rows then columns

#----- Modify cult -----#
# Set to 0 in MH
cult = 0.0

#----- Modify soilph -----#
# In emission_dust.F90: the area with soilph(3) + soilph(4) > 0 is considered as desert
# Lu2018: bare soil is set where vegetation cover < 20%.
# So here we set both the soilph(3) and soilph(4) to 0 (not desert) when cvh + cvl >= 0.2 in the northern African region (20W-40E, 10N-30N).
# Notice the index of 3 and 4 are 2 and 3.

# Read cvh and cvl from data files
cvh = np.copy(data3['input_mhgsrd'][()]['cvh'])
cvl = np.copy(data3['input_mhgsrd'][()]['cvl'])
cvh_reg = cvh[np.ix_(regm_lat, regm_lon)]
cvl_reg = cvl[np.ix_(regm_lat, regm_lon)]

# Extract the region, set regional soilph wrt cvh and cvl, then set back the values
sp3_reg = np.squeeze( np.copy( soilph[np.ix_([2], regm_lat, regm_lon)] ) )
sp3_reg[cvh_reg+cvl_reg >= 0.2] = 0.0
soilph[np.ix_([2], regm_lat, regm_lon)] = sp3_reg

sp4_reg = np.squeeze( np.copy( soilph[np.ix_([3], regm_lat, regm_lon)] ) )
sp4_reg[cvh_reg+cvl_reg >= 0.2] = 0.0
soilph[np.ix_([3], regm_lat, regm_lon)] = sp4_reg

#----- Write back to file -----#
fid.variables['potsrc'][:] = potsrc  # [nlat, nlon]
fid.variables['cult'  ][:] = cult    # [nlat, nlon]
fid.variables['soilph'][:] = soilph  # [nsoilph, nlat, nlon]

fid.close()


##### Modify for MH

# Copy a new file from the raw data file to modify
fname_mh = fdir + '/onlinedust_4_mh.nc'
shutil.copyfile(fname_raw, fname_mh)

# Open the file with read and write permissions
# fid, fattr, fdim, fvar = pf.ncdump(fname_mhgsrd, verb=False)
fid = Dataset(fname_mh, 'r+')

# Read data
lon, lat = fid.variables['lon'][:], fid.variables['lat'][:]
nlon, nlat = lon.size, lat.size  # 360, 180
potsrc = np.copy(fid.variables['potsrc'][:])  # [nlat, nlon]
cult   = np.copy(fid.variables['cult'][:])  # [nlat, nlon]
soilph = np.copy(fid.variables['soilph'][:])  # [nsoilph, nlat, nlon]
nsoilph = np.size(soilph, axis=0)

# Region mask
regm_lat = (lat>=10) & (lat<=30)
regm_lon = (lon>=-20) & (lon<=40)

#----- Modify potsrc -----#
# Set all the potsrc in the region 20W-40E, 10N-30N to 0,
# representing they are no longer potential dust sources but lakes in MH.
potsrc[np.ix_(regm_lat, regm_lon)] = 0.0  # select rows then columns

#----- Modify cult -----#
# Set to 0 in MH
cult = 0.0

#----- Modify soilph -----#
# In emission_dust.F90: the area with soilph(3) + soilph(4) > 0 is considered as desert
# Lu2018: bare soil is set where vegetation cover < 20%.
# So here we set both the soilph(3) and soilph(4) to 0 when cvh + cvl >= 0.2 in the northern African region (20W-40E, 10N-30N).
# Notice the index of 3 and 4 are 2 and 3.

# Read cvh and cvl from data files
cvh = np.copy(data3['input_mh'][()]['cvh'])
cvl = np.copy(data3['input_mh'][()]['cvl'])
cvh_reg = cvh[np.ix_(regm_lat, regm_lon)]
cvl_reg = cvl[np.ix_(regm_lat, regm_lon)]

# Extract the region, set regional soilph wrt cvh and cvl, then set back the values
sp3_reg = np.squeeze( np.copy( soilph[np.ix_([2], regm_lat, regm_lon)] ) )
sp3_reg[cvh_reg+cvl_reg >= 0.2] = 0.0
soilph[np.ix_([2], regm_lat, regm_lon)] = sp3_reg

sp4_reg = np.squeeze( np.copy( soilph[np.ix_([3], regm_lat, regm_lon)] ) )
sp4_reg[cvh_reg+cvl_reg >= 0.2] = 0.0
soilph[np.ix_([3], regm_lat, regm_lon)] = sp4_reg

#----- Write back to file -----#
fid.variables['potsrc'][:] = potsrc  # [nlat, nlon]
fid.variables['cult'  ][:] = cult    # [nlat, nlon]
fid.variables['soilph'][:] = soilph  # [nsoilph, nlat, nlon]

fid.close()


##### Modify for PI

# Copy a new file from the raw data file to modify
fname_pi = fdir + '/onlinedust_4_pi.nc'
shutil.copyfile(fname_raw, fname_pi)

# Open the file with read and write permissions
fid = Dataset(fname_pi, 'r+')

# Read data
lon, lat = fid.variables['lon'][:], fid.variables['lat'][:]
nlon, nlat = lon.size, lat.size  # 360, 180
potsrc = np.copy(fid.variables['potsrc'][:])  # [nlat, nlon]
cult   = np.copy(fid.variables['cult'][:])  # [nlat, nlon]
soilph = np.copy(fid.variables['soilph'][:])  # [nsoilph, nlat, nlon]
nsoilph = np.size(soilph, axis=0)

# Region mask
regm_lat = (lat>=10) & (lat<=30)
regm_lon = (lon>=-20) & (lon<=40)

#----- Modify potsrc -----#
# potsrc does not change

#----- Modify cult -----#
# Set to 0 in PI
cult = 0.0

#----- Modify soilph -----#
# soilph does not change.

#----- Write back to file -----#
fid.variables['potsrc'][:] = potsrc  # [nlat, nlon]
fid.variables['cult'  ][:] = cult    # [nlat, nlon]
fid.variables['soilph'][:] = soilph  # [nsoilph, nlat, nlon]

fid.close()


sys.exit()


#
# Plot the check
#
pm = 'cyl'
reg = lf.reg_glob

# soilph 3
z1 = np.copy( fid.variables['soilph'][:][2, :, :] )
zm1 = ma.array(z1, mask = z1==0)
lf.plot_simple_pcolor_map(lon, lat, zm1, pm, reg, './figures/onlinedust_soilph3_present.png')

z2 = np.copy( soilph[2, :, :] )
zm2 = ma.array(z2, mask = z2==0)
lf.plot_simple_pcolor_map(lon, lat, zm2, pm, reg, './figures/onlinedust_soilph3_mhgsrd.png')

# soilph 4
z = np.copy( fid.variables['soilph'][:][3, :, :] )
zm = ma.array(z, mask = z==0)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/onlinedust_soilph4_present.png')

z = np.copy( soilph[3, :, :] )
zm = ma.array(z, mask = z==0)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/onlinedust_soilph4_mhgsrd.png')

# potsrc
z = fid.variables['potsrc'][:]
zm = ma.array(z, mask = z==0)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/onlinedust_potsrc_present.png')

z = potsrc
zm = ma.array(z, mask = z==0)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/onlinedust_potsrc_mhgsrd.png')

# cvh + cvl
z = cvh + cvl
zm = ma.array(z, mask = z<0.2)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/onlinedust_masked_cv.png')
