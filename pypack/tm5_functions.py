import numpy as np
from scipy import interpolate

from netCDF4 import Dataset

import netcdf


def interp_to_lonlat_3d(fname1, fname2, lon2, lat2, vname):
  """
  " Interpolate the variable in fname1 and save the data to fname2
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
