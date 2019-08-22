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

fdir = '/homeappl/home/putian/scripts/tm5-mp/data/tm5_input_modified'
fname_raw = fdir + '/onlinedust_4.nc'

# Modify region is North Africa
reg_nafr = (-20.0, 40.0, 10.0, 30.0)  # W, E, S, N


#======================================#
# Modify for MH_gsrd
#======================================#
lu2018_mg = np.load('data1_mg.npz')

# Copy a new file from the raw data file to modify
fname_mhgsrd = fdir + '/onlinedust_4_mhgsrd.nc'
shutil.copyfile(fname_raw, fname_mhgsrd)

# Open the file with read and write permissions
fid = Dataset(fname_mhgsrd, 'r+')

# Read data from new netcdf file
lon, lat = fid.variables['lon'][:], fid.variables['lat'][:]
nlon, nlat = lon.size, lat.size  # 360, 180
potsrc = np.copy(fid.variables['potsrc'][:])  # [nlat, nlon]
cult   = np.copy(fid.variables['cult'][:])  # [nlat, nlon]
soilph = np.copy(fid.variables['soilph'][:])  # [nsoilph, nlat, nlon]
nsoilph = np.size(soilph, axis=0)

print(np.amax(cult))
print(cult[90, :])

# Region mask
regm_lon = (lon>=reg_nafr[0]) & (lon<=reg_nafr[1])
regm_lat = (lat>=reg_nafr[2]) & (lat<=reg_nafr[3])

#----- Modify potsrc -----#
# Set all the potsrc in the region 20W-40E, 10N-30N to 0,
# representing they are no longer potential dust sources but lakes in MH.
potsrc[np.ix_(regm_lat, regm_lon)] = 0.0  # select rows then columns

#----- Modify cult -----#
# Set to 0 in MH
cult = 0.0

#----- Modify soilph -----#

# Read cvh and cvl from data files, use annual average here as a first test
cvh = np.mean(lu2018_mg['cvh_dom_avg_11'], axis=0)
cvl = np.mean(lu2018_mg['cvl_dom_avg_11'], axis=0)

soilph = lf.modify_soilph(lon, lat, soilph, cvh, cvl, reg_nafr)

#----- Write back to file -----#
fid.variables['potsrc'][:] = potsrc  # [nlat, nlon]
fid.variables['cult'  ][:] = cult    # [nlat, nlon]
fid.variables['soilph'][:] = soilph  # [nsoilph, nlat, nlon]

fid.close()


#======================================#
# Modify for MH
#======================================#

# Read interpolated Lu2018 data
lu2018_mh = np.load('data1_mh.npz')

# Copy a new file from the raw data file to modify
fname_mh = fdir + '/onlinedust_4_mh.nc'
shutil.copyfile(fname_raw, fname_mh)

# Open the file with read and write permissions
fid = Dataset(fname_mh, 'r+')

# Read data
lon, lat = fid.variables['lon'][:], fid.variables['lat'][:]
nlon, nlat = lon.size, lat.size  # 360, 180
potsrc = np.copy(fid.variables['potsrc'][:])  # [nlat, nlon]
cult   = np.copy(fid.variables['cult'][:])  # [nlat, nlon]
soilph = np.copy(fid.variables['soilph'][:])  # [nsoilph, nlat, nlon]
nsoilph = np.size(soilph, axis=0)

#----- Modify potsrc -----#
# Set all the potsrc in the region 20W-40E, 10N-30N to 0,
# representing they are no longer potential dust sources but lakes in MH.
potsrc[np.ix_(regm_lat, regm_lon)] = 0.0  # select rows then columns

#----- Modify cult -----#
# Set to 0 in MH
cult = 0.0

#----- Modify soilph -----#

# Read cvh and cvl from data files
cvh = np.mean(lu2018_mh['cvh_dom_avg_11'], axis=0)
cvl = np.mean(lu2018_mh['cvl_dom_avg_11'], axis=0)

soilph = lf.modify_soilph(lon, lat, soilph, cvh, cvl, reg_nafr)

#----- Write back to file -----#
fid.variables['potsrc'][:] = potsrc  # [nlat, nlon]
fid.variables['cult'  ][:] = cult    # [nlat, nlon]
fid.variables['soilph'][:] = soilph  # [nsoilph, nlat, nlon]

fid.close()


##### Modify for PI

# Read interpolated Lu2018 data
lu2018_pi = np.load('data1_pi.npz')

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
