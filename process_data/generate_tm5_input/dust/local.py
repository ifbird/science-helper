import shutil
import numpy as np
from netCDF4 import Dataset

#==============================================================================#
#
# Local functions
#
#==============================================================================#

# Some setup
# c: pi, mh1, mh2
# s: iso, mon
# y: 1850, ..., 2009, or 1850_1859_mean
# m: month, 01 - 12
# d: day, 1 - 31


#
# Raw Lu2018 veg data file names
#

fdir_lu2018_veg = '/homeappl/home/putian/scripts/tm5-mp/data/lu2018_lpjg_monthly_veg'


def get_fname_lu2018_veg_lrg(c):
  newc = {'pi': 'PI', 'mh1': 'MH', 'mh2': 'MHgsrd'}
  return fdir_lu2018_veg+ '/LPJ-GUESS_monthlyoutput_{0}.txt'.format(newc[c])


def get_fname_lu2018_veg_gxx(c):
  return fdir_lu2018_veg+ '/{0}-lpjg_monthly_gxx.nc'.format(c)


#
# Raw onlinedust_4.nc as a sample
#

fdir_sample_dust = '/proj/atm/TM5_INPUT/aerosols/Dust/ONLINE'

def get_fname_sample_dust():
  return fdir_sample_dust + '/onlinedust_4.nc'


#
# New onlinedust_4.nc files
#

fdir_new_dust = '/homeappl/home/putian/scripts/tm5-mp/data/tm5_input_modified/aerosol-dust'


def get_fname_new_dust(c, y):
  return fdir_new_dust + '/{0}-{1}-onlinedust_4.nc'.format(c, y)


# Grid box area for 0.5x0.5
# lon, lat, gridbox_area [m-2]
# fname_gridarea_0p5x0p5 = '/proj/atm/TM5_EMISS/MACCity/gridbox_area.nc'


# Case list
case_list = ['pi', 'mh1', 'mh2']

# Year count in Lu2018 veg data
nyear = 10
nmon  = 12
ndate = nmon
month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def modify_onlinedust_from_veg(fname_raw, fname_new, cvl, cvh, potsrc_region, cult_new, soilph_threshold):
  """
  " Modify onlinedust file wrt to meteo veg data
  " potsrc_region: [south, north, west, east]
  """
  # Copy raw file to a new one for further modifying
  shutil.copyfile(fname_raw, fname_new)
  
  # Open the file with read and write permissions
  # fid, fattr, fdim, fvar = pf.ncdump(fname_mhgsrd, verb=False)
  fid = Dataset(fname_new, 'r+')
  
  # Read data
  lon, lat = fid.variables['lon'][:], fid.variables['lat'][:]
  nlon, nlat = lon.size, lat.size  # 360, 180
  potsrc = np.copy(fid.variables['potsrc'][:])  # [nlat, nlon]
  cult   = np.copy(fid.variables['cult'][:])  # [nlat, nlon]
  soilph = np.copy(fid.variables['soilph'][:])  # [nsoilph, nlat, nlon]
  nsoilph = np.size(soilph, axis=0)
  
  # Region mask
  regm_lat = (lat>=potsrc_region[0]) & (lat<=potsrc_region[1])
  regm_lon = (lon>=potsrc_region[2]) & (lon<=potsrc_region[3])
  
  #----- Modify potsrc -----#
  # Set all the potsrc in the region 20W-40E, 10N-30N to 0,
  # representing they are no longer potential dust sources but lakes in MH.
  potsrc[np.ix_(regm_lat, regm_lon)] = 0.0  # select rows then columns
  
  #----- Modify cult -----#
  # Set to 0 in MH
  cult = cult_new
  
  #----- Modify soilph -----#
  # In emission_dust.F90: the area with soilph(3) + soilph(4) > 0 is considered as desert
  # Lu2018: bare soil is set where vegetation cover < 20%.
  # So here we set both the soilph(3) and soilph(4) to 0 (not desert) when cvh + cvl >= 0.2
  # in the northern African region (20W-40E, 10N-30N) the same as potsrc_region.
  # Notice the index of 3 and 4 are 2 and 3.
  
  # Read cvh and cvl from data files
  cvh_reg = cvh[np.ix_(regm_lat, regm_lon)]
  cvl_reg = cvl[np.ix_(regm_lat, regm_lon)]
  
  # Extract the region, set regional soilph wrt cvh and cvl, then set back the values
  sp3_reg = np.squeeze( np.copy( soilph[np.ix_([2], regm_lat, regm_lon)] ) )
  sp3_reg[cvh_reg+cvl_reg >= soilph_threshold] = 0.0
  soilph[np.ix_([2], regm_lat, regm_lon)] = sp3_reg
  
  sp4_reg = np.squeeze( np.copy( soilph[np.ix_([3], regm_lat, regm_lon)] ) )
  sp4_reg[cvh_reg+cvl_reg >= soilph_threshold] = 0.0
  soilph[np.ix_([3], regm_lat, regm_lon)] = sp4_reg
  
  #----- Write back to file -----#
  fid.variables['potsrc'][:] = potsrc  # [nlat, nlon]
  fid.variables['cult'  ][:] = cult    # [nlat, nlon]
  fid.variables['soilph'][:] = soilph  # [nsoilph, nlat, nlon]
  
  fid.close()
