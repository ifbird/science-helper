import os
import sys

from scipy import interpolate
import numpy as np

from pyhdf.SD import *

from constants import *


def calc_land_ind_in_grg_grid(lon_lrg, lat_lrg, lon_grg, lat_grg):
  """
  " Obtain the indices of lon and lat for each land grid in the global grid: land_ind
  "
  " Find lon and lat indices for land grids in global grids
  " For the i-th grid saved in the Lu2018 data,
  " the land lon and lat are: lon_land[i], lat_land[i]
  " the lon and lat in the global grid: lon_glob[land_ind[i, 1]][land_ind[i, 0]], lat_glob[land_ind[i, 1]]
  " In order to verify if the point in land and globe is close enough,
  " differences of lon and lat are calculated as diff_lg for each point at land grid and global grid.
  """

  ngrid_lrg = lon_lrg.size

  land_ind = np.zeros((ngrid_lrg, 4)).astype(int)  # save the lon and lat index in the global grid
  for i, (lon, lat) in enumerate(zip(lon_lrg, lat_lrg)):
    # lat
    ilat = (np.abs(lat - lat_grg)).argmin()
  
    # lon
    ilon = (np.abs(lon - lon_grg[ilat])).argmin()
  
    # Save the indices to the land_ind array, and the errors
    land_ind[i, :] = ilon, ilat, lon-lon_grg[ilat][ilon], lat-lat_grg[ilat]
    
  return land_ind


def data_lrg2grg(data_lrg, land_ind, lon_grg, lat_grg):
  """
  " Fill the data of one variable in grg grid with data in lrg grid
  " 
  " Input:
  "   data_lrg: (ngrid_lrg, ), the dataset at land grid
  "   land_ind: (ngrid_lrg, 4), indices of lon and lat of lrg in grg
  "   lon_grg: nlat_grg lists, lon of grg grid for each lat
  "   lat_grg: lat of grg grid
  " Output:
  "   data_grg: data at global reduced Gaussian grid
  "             data_grg[nlat][nlon]: 
  """

  ngrid_lrg = data_lrg.size
  nlat_grg = lat_grg.size

  # Put land data in lrg to grg
  data_grg = []  # data at grg grid
  for j in range(nlat_grg):
    data_grg.append( np.zeros((lon_grg[j].size,)) )

  for ig in range(ngrid_lrg):
    ilon, ilat = land_ind[ig, 0:2]
    data_grg[ilat][ilon] = data_lrg[ig]

  return data_grg


def data_grg2gxx(data_grg, lon_grg, lat_grg, lon_gxx, lat_gxx, kind='linear'):
  """
  " Interpolate data from grg grid to gxx grid
  "
  " data_grg: the dataset at grg grid
  " data_gxx: [nlon_gxx, nlat_gxx]
  """

  # Set parameters
  nlat_grg = lat_grg.size
  nlon_gxx, nlat_gxx = lon_gxx.size, lat_gxx.size

  # Data at gg grid as the intermediate data
  data_gg  = np.zeros((nlon_gxx, nlat_grg))
  data_gxx = np.zeros((nlon_gxx, nlat_gxx))

  # grg to gg: Interpolate for each lat at grg grid to gg grid
  for ilat in range(nlat_grg):
    # Construct data set representing the period data
    x = np.concatenate([ [lon_grg[ilat][-1]-360.0], lon_grg[ilat][:], [lon_grg[ilat][0]+360.0] ])
    y = np.concatenate([ [data_grg[ilat][-1]], data_grg[ilat][:], [data_grg[ilat][0]] ])

    # Interpolate with method kind
    f = interpolate.interp1d(x, y, kind=kind)
    data_gg[:, ilat] = f(lon_gxx)

  # gg to gxx: Interpolate for each lon_gxx from grg lat to gxx lat: gg --> gxx
  # 0 for external points, and remember to keep xp increment
  for ilon in range(nlon_gxx):
    # New interpolation method, make sure x is in the increment order
    f = interpolate.interp1d(lat_grg, data_gg[ilon, :], kind=kind, fill_value=0.0, bounds_error=False)
    data_gxx[ilon, :] = f(lat_gxx)
  
  return data_gxx


def data_lrg2gxx(data_lrg, lon_lrg, lat_lrg, land_ind, lon_grg, lat_grg, lon_gxx, lat_gxx, kind='linear'):
  """
  " Interpolate data from lrg grid to gxx grid
  """
  data_grg = data_lrg2grg(data_lrg, land_ind, lon_grg, lat_grg)
  data_gxx = data_grg2gxx(data_grg, lon_grg, lat_grg, lon_gxx, lat_gxx, kind)

  return data_gxx


def calc_grg_grid(nlon_nhrg, lat_nhrg):
  """
  " Calculate the global reduced Gaussian grid from nlon and lat of northern hemisphere reduced Gaussian grid
  "
  " Input:
  "   nlon_nhrg: number of lon along every lat in lat_nhrg
  "   lat_nhrg: lat in Gaussian grid in northern hemisphere
  "
  " Output:
  "   lat_grg: lat from -90 to 90, poles are usually not included
  "   lon_grg: lon_grg[i] is the lon along the i-th lat_grg
  """

  ##### Global lat from south to north
  if lat_nhrg[1] - lat_nhrg[0] > 0:  # lat_nhrg is from south to north
    lat_grg = np.concatenate( [-lat_nhrg[::-1], lat_nhrg] )
    is_input_s2n = True
  else:  # lat_nhrg is from north to south
    lat_grg = np.concatenate( [-lat_nhrg, lat_nhrg[::-1]] )
    is_input_s2n = False

  ##### Global lon from west to east, 0 is about in the middle
  ##### lon: a list of arrays
  # Combine the NH and SH
  if is_input_s2n:
    nlon_grg = np.concatenate( [nlon_nhrg[::-1], nlon_nhrg] )
  else:
    nlon_grg = np.concatenate( [nlon_nhrg, nlon_nhrg[::-1]] )

  # Initiate
  lon_grg = []

  # Loop for each lat
  for i, n in enumerate(nlon_grg):
    dl = 360.0/n  # lon interval for each lat
    if n % 2 == 1:  # n is odd
      l0 = -180.0 + dl/2.0
      l1 = 180.0 - dl/2.0
      n0 = int((n-1)/2)
    else:  # n is even
      l0 = -180.0 + dl
      l1 = 180.0
      n0 = int((n-2)/2)
    n1 = n - n0
  
    # 0 degree must be included in the reduced Gaussian grid
    lon_temp = np.concatenate([np.linspace(l0, 0, n0, endpoint=False), np.linspace(0, l1, n1)])

    # Add the lon array to the lon_grg list
    lon_grg.append(lon_temp)

  return lon_grg, lat_grg


def calc_gxx_grid(xbeg, xend, dlon, ybeg, yend, dlat, mode='c'):
  """
  " Calculate gxx grid in grid centers
  "
  " xbeg, xend, ybeg, yend: beginning and ending boundaries of grid
  " dlon, dlat: grid dimensions
  " mode: 'c': generated points are in centers
  "       'b': generated points are in boundaries
  """
  if mode == 'c':
    nlon = int(round( (xend - xbeg)/dlon ))
    nlat = int(round( (yend - ybeg)/dlat ))

    lon_gxx = np.linspace(xbeg+dlon/2, xend-dlon/2, nlon)
    lat_gxx = np.linspace(ybeg+dlat/2, yend-dlat/2, nlat)
  elif mode = 'b':
    nlon = int(round( (xend - xbeg)/dlon )) + 1
    nlat = int(round( (yend - ybeg)/dlat )) + 1

    lon_gxx = np.linspace(xbeg, xend, nlon)
    lat_gxx = np.linspace(ybeg, yend, nlat)

  return lon_gxx, lat_gxx


def create_tm5_input_monthly_veg_file(fname, year, month, lon, lat, cvl, cvh, tv, \
    fsample, verb=False, output='output_veg.txt'):
  """
  " Create the vegetation input file in the hdf4 format for tm5
  "
  " fname: name of tm5 input veg hdf4 file which will be generated
  " input data: lon, lat, cvl, cvh, tv
  " fsample: name of sample tm5 input veg file, we need to copy global attributes from it
  """

  # fid_sample, fattr_sample, fdset_sample = pf.h4dump(fname_sample, True, 'output_tm5_input_veg_sample.txt')

  # Delete file if exists, so create a totally new file
  if os.path.exists(fname):
    os.remove(fname)
  
  # Number of lon and lat
  nlon, nlat = lon.size, lat.size
  
  # Open a file to write
  fid        = SD(fname, SDC.WRITE|SDC.CREATE)
  fid_sample = SD(fsample, SDC.READ)
  
  # Set global attributes according to fid_sample
  fid.ae       = fid_sample.ae
  fid.area_m2  = fid_sample.area_m2
  fid.fname    = fname  # better to use absolute path here
  fid.format   = fid_sample.format
  fid.grav     = fid_sample.grav
  fid.gridtype = fid_sample.gridtype
  fid.latmax   = fid_sample.latmax
  fid.latmin   = fid_sample.latmin
  fid.lonmax   = fid_sample.lonmax
  fid.lonmin   = fid_sample.lonmin

  # Create datasets for lon and lat
  d = fid.create('LAT', SDC.FLOAT64, nlat)
  dim0 = d.dim(0)
  dim0.setname('LAT')
  d[:] = lat
  d.endaccess()
  
  d = fid.create('LON', SDC.FLOAT64, nlon)
  dim1 = d.dim(0)
  dim1.setname('LON')
  d[:] = lon
  d.endaccess()
  
  # Create datasets for tv
  for i in range(nvt):
    tvstr = tm5['tvname'][i]
    d = fid.create(tvstr, SDC.FLOAT64, (nlat, nlon))
    dim0 = d.dim(0)
    dim1 = d.dim(1)
    dim0.setname('LAT')
    dim1.setname('LON')
  
    d[:] = tv[i, :, :]

    # Close dataset
    d.endaccess()

  # Create datasets for cvh and cvl
  d = fid.create('cvh', SDC.FLOAT64, (nlat, nlon))
  dim0 = d.dim(0)
  dim1 = d.dim(1)
  dim0.setname('LAT')
  dim1.setname('LON')
  d[:] = cvh
  d.endaccess()
  
  d = fid.create('cvl', SDC.FLOAT64, (nlat, nlon))
  dim0 = d.dim(0)
  dim1 = d.dim(1)
  dim0.setname('LAT')
  dim1.setname('LON')
  d[:] = cvl
  d.endaccess()
  
  #
  # Add variable attributes
  #

  # Set the common attibutes with tm5 veg sample file except time parts
  ds_names = fid.datasets()
  ds_sample = fid_sample.select('tv01')
  for dn in ds_names:
    ds = fid.select(dn)
    if not ds.iscoordvar():
      for attr_name, attr_value in ds_sample.attributes().items():
        setattr(ds, attr_name, attr_value)

      ds.idate = [year, month, 1, 0, 0, 0]
      ds.time1 = [year, month, 1, 0, 0, 0]
      if int(month) == 12:
        ds.time2 = [year+1, 1, 1, 0, 0, 0]
      else:
        ds.time2 = [year, month+1, 1, 0, 0, 0]
      ds.tref  = [year, month, 1, 0, 0, 0]

  # Set units for tv
  for i in range(nvt):
    tvstr = tm5['tvname'][i]
    ds = fid.select(tvstr)
    ds.unit = '%'

  # Set units for cvl and cvh
  ds = fid.select('cvl')
  ds.unit = '0-1'
  ds = fid.select('cvh')
  ds.unit = '0-1'

  # Close file
  fid.end()
  fid_sample.end()
  
  # Check file info
  fid, fattr, fdset = pf.h4dump(fname, verb, output)

  return fid, fattr, fdset


def show_statistics(data):
  """
  " Show main information of a dataset in a numpy array:
  "   min, 25% quantile, median, 75% quantile, max
  "   mean, std
  "
  " np.quantile is added in 1.15.0
  """
  _min    = np.nanmin(data.flatten())
  _max    = np.nanmax(data.flatten())
  _q1     = np.percentile(data.flatten(), 25)
  _q3     = np.percentile(data.flatten(), 75)
  _median = np.nanmedian(data.flatten())
  _mean   = np.nanmean(data.flatten())
  _std    = np.nanstd(data.flatten())
  
  print('{0:>12s}{1:>12s}{2:>12s}{3:>12s}{4:>12s}{5:>12s}{6:>12s}'.format('min', 'q1', 'median', 'q3', 'max', 'mean', 'std'))
  print('{0:12.3e}{1:12.3e}{2:12.3e}{3:12.3e}{4:12.3e}{5:12.3e}{6:12.3e}'.format(_min, _q1, _median, _q3, _max, _mean, _std))
  
  return (_min, _q1, _median, _q3, _max, _mean, _std)


def set_dir(d):
  """
  " Create a dir d if not existed
  """
  try:
    os.makedirs(d)
    return d
  except OSError as e:
    if e.errno != errno.EEXIST:  # if the error is not 'already existed'
      raise
    else:
      return d


def interp_to_lonlat_3d(fname1, fname2, lon2, lat2, vname):
  """
  " Interpolate the variable in fname1 (netcdf) and save the data to fname2 (netcdf)
  "
  " fname1:
  "   Dimensions: time, lev, lat, lon, others 
  "   Variables : time(time), lev(lev), lat(lat), lon(lon), vname(time, lev, lat, lon), others
  "
  " fname2:
  "   Dimensions: copied time, copied lev, new lat, new lon, copied others
  "   Variables : copied time(time), copied lev(lev), new lat(lat), new lon(lon),
  "               new vname(time, lev, new lat, new lon), copied others
  """

  # Read data from the raw data file
  fid1, attr_list1, dim_list1, var_list1 = netcdf.ncdump(fname1, verb=False, log_file=None)

  time1 = fid1.variables['time']; ntime1 = len(time1)
  lev1  = fid1.variables['lev' ]; nlev1  = len(lev1 )
  lon1  = fid1.variables['lon' ]; nlon1  = len(lon1 )
  lat1  = fid1.variables['lat' ]; nlat1  = len(lat1 )

  var1 = fid1.variables[vname]

  # Create a new netcdf file to save the interpolated data
  fid2 = Dataset(fname2, 'w')

  # Copy global attributes from fname1
  netcdf.copy_global_attributes(fid1, fid2)

  # Copy dimensions except lat and lon
  for dname in dim_list1:
    if not (dname in ['lon', 'lat']):
      netcdf.copy_dimension(fid1, fid2, dname)

  # Create new lon and lat dimensions
  nlon2, nlat2 = len(lon2), len(lat2)
  fid2.createDimension('lon', nlon2)
  fid2.createDimension('lat', nlat2)

  # Copy variables except vname
  for vn in var_list1:
    if not (vn in ['lon', 'lat', vname]):
      netcdf.copy_variable(fid1, fid2, vn)

  # Create new variables lon, lat, and vname
  lon2_ref = fid2.createVariable('lon', lon1.dtype, ('lon',))
  lat2_ref = fid2.createVariable('lat', lat1.dtype, ('lat',))
  var2_ref = fid2.createVariable(vname, var1.dtype, ('time', 'lev', 'lat', 'lon'))

  # Interpolate the data to new lonlat grid
  ntime2 = ntime1
  nlev2 = nlev1
  var2 = np.zeros((ntime2, nlev2, nlat2, nlon2))

  for it, t in enumerate(time1):
    print(it, t)
    for il, l in enumerate(lev1):
      f = interpolate.interp2d(lon1, lat1, var1[it, il][:, :], kind='linear')
      var2[it, il][:, :] = f(lon2, lat2)

  # Get the values
  lon2_ref[:] = lon2
  lat2_ref[:] = lat2
  var2_ref[:] = var2[:]

  fid2.close()


