import numpy as np

import calendar

import putian_functions as pf
import local_functions as lf

#
# Set parameters
#

# Variable id in tm5 veg files
varidx_in_tm5_veg = {
  'tv01': ( 0, 19, 36, 53),
  'tv02': ( 3, 20, 37, 54),
  'tv03': ( 4, 21, 38, 55),
  'tv04': ( 5, 22, 39, 56),
  'tv05': ( 6, 23, 40, 57),
  'tv06': ( 7, 24, 41, 58),
  'tv07': ( 8, 25, 42, 59),
  'tv08': None,
  'tv09': ( 9, 26, 43, 60),
  'tv10': (10, 27, 44, 61),
  'tv11': (11, 28, 45, 62),
  'tv12': None,
  'tv13': (12, 29, 46, 63),
  'tv14': None,
  'tv15': None,
  'tv16': (13, 30, 47, 64),
  'tv17': (14, 31, 48, 65),
  'tv18': (15, 32, 49, 66),
  'tv19': (16, 33, 50, 67),
  'tv20': None,
  'cvl' : (17, 34, 51, 68),
  'cvh' : (18, 35, 52, 69),
  }

# Used tv variables in tm5
used_tvind  = ['01', '02', '03', '04', '05', '06', '07', '09', '10', '11', '13', '16', '17', '18', '19']
used_tvname = ['tv' + i for i in used_tvind]

# Number of veg types
nvt = 20


def calculate_monthly_mean_for_tm5_veg(meteo_dir, year, month):
  # tm5 veg data dir
  fdir = '{0:s}/{1:4d}'.format(meteo_dir, year)

  # Check for leap year
  md = list(pf.monthday)  # get a copy of pf.monthday
  if calendar.isleap(year):
    md[1] = md[1] + 1  # add one day to Feb

  # Day count of current month
  nday = md[month-1]

  # Loop for every day in the month, starting from day 1
  first_loop = True
  for day in range(1, nday+1):
    fname = fdir + '/ec-ei-an0tr6-sfc-glb100x100-veg_{0:4d}{1:02d}{2:02d}_00p06.hdf'.format(year, month, day)

    # Read the file and get file id, attribute list and dataset list
    fid, fattr, fdset = pf.h4dump(fname, False)

    #
    # Only do once
    #
    if first_loop:
      # Get the dimension data
      lat = fid.select('LAT')[:]  # -89.5 to 89.5, 180
      lon = fid.select('LON')[:]  # -179.5 to 179.5, 360
      nlat, nlon = lat.size, lon.size

      # Intiate tv, cvh, cvl
      tv = np.zeros((nvt, nlat, nlon))
      cvh = np.zeros((nlat, nlon))
      cvl = np.zeros((nlat, nlon))

      first_loop = False

    #
    # Add up the input values
    #

    # Loop for each veg type
    for ivt in range(nvt):
      tvname = 'tv{:02d}'.format(int(ivt+1))
      if varidx_in_tm5_veg[tvname] is not None:
        # Loop for each 6-hourly data
        for idx in varidx_in_tm5_veg[tvname]:
          tv[int(ivt), :, :] += fid.select(idx)[:]

    # Loop for each 6-hourly data
    for idx in varidx_in_tm5_veg['cvh']:
      cvh[:] += fid.select(idx)[:]

    # Loop for each 6-hourly data
    for idx in varidx_in_tm5_veg['cvl']:
      cvl[:] += fid.select(idx)[:]

  # Calculat the mean from sum for 6-hourly data in a month, 4 data point per day
  tv  /= 4.0*nday
  cvh /= 4.0*nday
  cvl /= 4.0*nday

  return tv, cvh, cvl, lat, lon


#
# Read tm5 veg 6-hourly data
#

# Date
year = 2009
month = 2
# day = 1  # from 1 to 28 for Feb

# tm5 meteo folder
meteo_dir = '/proj/atm/TM5_METEO'

# Get the monthly mean value of tv (0-100), cvh (0-1), cvl(0-1)
tv, cvh, cvl, lat, lon = calculate_monthly_mean_for_tm5_veg(meteo_dir, year, month)

# Save monthly mean tm5 veg data
np.savez('data2_tm5veg_{:4d}{:02d}.npz'.format(year, month), tv=tv, cvh=cvh, cvl=cvl, lat=lat, lon=lon)

#
# Debug
#

# ind_low = lf.tm5_veg_low
# ind_high = lf.tm5_veg_high
# tv_low = np.sum(tv[lf.tm5_veg_low-1, :, :], axis=0)
# tv_high = np.sum(tv[lf.tm5_veg_high-1, :, :], axis=0)
# tv_all = tv_low + tv_high
# tv_low = np.sum(tv[lf.lu2018_veg_low-1, :, :], axis=0)
# tv_high = np.sum(tv[lf.lu2018_veg_high-1, :, :], axis=0)
# print(tv_low[90, :]/100.0)
# print(cvl[90, :])
# print(tv_high[90, :]/100.0)
# print(cvh[90, :])
# 
# eps = 1.0e-30
# lon_slice = np.arange(100,120).astype(int)
# print(tv_low[90, :]/(tv_all[90,:]+eps) - cvl[90, :])
# print(tv_high[90, :]/(tv_all[90,:]+eps) - cvh[90, :])
# print(cvh[90, lon_slice] + cvl[90, lon_slice])
# print(tv_all[90, lon_slice])
# print(tv_low[90, lon_slice]/(tv_all[90, lon_slice] + eps))
# print(tv_high[90, lon_slice]/(tv_all[90, lon_slice] + eps))

# print(np.max(tv[0], axis=0))
# print(np.max(cvh, axis=0))
# print(np.max(cvl, axis=0))

# tm5_meteo_dir = '/proj/atm/TM5_METEO/{:4d}'.format(year)
# tm5_veg_fname = tm5_meteo_dir + '/ec-ei-an0tr6-sfc-glb100x100-veg_{0:4d}{1:02d}{2:02d}_00p06.hdf'.format(year, month, day)
# 
# print(tm5_veg_fname)
# fid, fattr, fdset = pf.h4dump(tm5_veg_fname, False, 'output_tm5_veg.txt')
# 
# print(fattr)
# print(fdset)


# Calculate monthly mean


# Combine the Lu2018 data and tm5 veg 6-hourly data


# Save in the tm5 input data format
