import numpy as np

from fileio import *

from netCDF4 import Dataset


def ncdump(ncfile, verb=True, log_file=None):
  '''
  SOURCE
    Copied from: http://schubert.atmos.colostate.edu/~cslocum/netcdf_example.html
  REVISION HISTORY
    20180726 -- Zhou Putian -- Also print out the variables which are dimensions.
    20180831 -- Zhou Putian -- Can choose to output to file, screen or nothing
  USAGE
  ncdump outputs dimensions, variables and their attribute information.
  The information is similar to that of NCAR's ncdump utility.
  ncdump requires a valid instance of Dataset.
  
  Parameters
  ----------
  ncfile : netCDF4 file
  verb : Boolean
    whether or not nc_attrs, nc_dims, and nc_vars are printed
  log_file: String
    choose where to output the information
  
  Returns
  -------
  nc_fid : netCDF4.Dataset
    A netCDF4 dateset object
  nc_attrs : list
    A Python list of the NetCDF file global attributes
  nc_dims : list
    A Python list of the NetCDF file dimensions
  nc_vars : list
    A Python list of the NetCDF file variables
  '''

  def print_ncattr(key):
    """
    Prints the NetCDF file attributes for a given key
  
    Parameters
    ----------
    key : unicode
        a valid netCDF4.Dataset.variables key
    """
    try:
      printf("\t\ttype:" + repr(nc_fid.variables[key].dtype)); eol()
      for ncattr in nc_fid.variables[key].ncattrs():
        printf('\t\t%s:' % ncattr + \
          repr(nc_fid.variables[key].getncattr(ncattr))); eol()
    except KeyError:
      printf("\t\tWARNING: %s does not contain variable attributes" % key); eol()
  
  # Set output location
  printf = set_sysstdout(verb=verb, log_file=log_file)

  nc_fid = Dataset(ncfile, 'r')

  # NetCDF global attributes
  nc_attrs = nc_fid.ncattrs()
  if verb:
    printf("NetCDF Global Attributes:"); eol()
    for nc_attr in nc_attrs:
      printf( '\t%s:' % nc_attr + repr(nc_fid.getncattr(nc_attr)) ); eol()

  # Dimension shape information.
  nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions
  if verb:
    printf("NetCDF dimension information:"); eol()
    for dim in nc_dims:
      printf( "\tName:{0}".format(dim) ); eol()
      printf( "\t\tsize:{0}".format(len(nc_fid.dimensions[dim])) ); eol()
      print_ncattr(dim)

  # Variable information.
  nc_vars = [var for var in nc_fid.variables]  # list of nc variables
  if verb:
    printf("NetCDF variable information:"); eol()
    for var in nc_vars:
      printf( '\tName:{0}'.format(var) ); eol()
      printf( "\t\tdimensions:{0}".format(nc_fid.variables[var].dimensions) ); eol()
      printf( "\t\tsize:{0}".format(nc_fid.variables[var].size) ); eol()
      print_ncattr(var)

  # Reset output location to screen
  set_sysstdout(verb=True)

  return nc_fid, nc_attrs, nc_dims, nc_vars


def copy_global_attributes(nc_fid1, nc_fid2):
  """
  " Copy the global attributes in nc_fid1 to nc_fid2
  """
  
  for attr_name in nc_fid1.ncattrs():
    setattr(nc_fid2, attr_name, getattr(nc_fid1, attr_name)) 

  return nc_fid2


def copy_dimension(nc_fid1, nc_fid2, dim_name):
  """
  " Create a new dimension the same as that in nc_fid1
  """

  # If the dim is already in nc_fid2, print a message and do nothing
  if dim_name in nc_fid2.dimensions:
    print('{0} is already in the targeted netcdf file.'.format(dim_name))
    return nc_fid2

  # Get the dimension from nc_fid1
  dim1 = nc_fid1.dimensions[dim_name]
  if dim1.isunlimited():
    dim2 = nc_fid2.createDimension(dim_name, None)
  else:
    ndim = len(dim1)  # dimension length
    dim2 = nc_fid2.createDimension(dim_name, ndim)

  return nc_fid2


def copy_variable(nc_fid1, nc_fid2, var_name):
  """
  " Create a new variable, copy the attributes and the values
  """

  # If the var is already in nc_fid2, print a message and do nothing
  if var_name in nc_fid2.variables:
    print('{0} is already in the targeted netcdf file.'.format(var_name))
    return nc_fid2 

  # Get the variable and its dims from nc_fid1
  var1 = nc_fid1.variables[var_name]
  dims = var1.dimensions
  dtype = var1.dtype

  # Create a new variable in nc_fid2
  print(var_name, dtype, dims)
  var2 = nc_fid2.createVariable(var_name, dtype, dims)

  # Copy the attributes
  copy_variable_attributes(nc_fid1, var_name, nc_fid2, var_name)

  # Copy the data
  var2[:] = var1[:]

  return nc_fid2


def copy_variable_attributes(nc_fid1, var_name1, nc_fid2, var_name2):
  """
  " Copy the attributes of var_name1 in nc_fid1 to var_name2 in nc_fid2
  """

  # If dim names are not in nc files, do nothing
  if not (var_name1 in nc_fid1.variables and var_name2 in nc_fid2.variables):
    print('Variable names do not exist in the netcdf files.')
    return nc_fid2

  # Copy variable attributes
  var1 = nc_fid1.variables[var_name1]
  var2 = nc_fid2.variables[var_name2]
  for attr_name in var1.ncattrs():
    setattr(var2, attr_name, getattr(var1, attr_name))

  return nc_fid2


def save_single_data_to_netcdf(fname, dname_list, dim_list, vname, var):
  """
  " Simply save a variable to a nc file
  "
  " fname: file name
  "
  " The order of dimensions should be consistent, e.g.,
  "   dname_list: ['time', 'lat', 'lon']
  "   dim_list  : [time, lat, lon]
  "   vname     : ['data']
  "   var       : [data(time, lat, lon)]
  """

  # Open a file to write
  fid = Dataset(fname, 'w')

  # Create dimensions
  for dname, dim in zip(dname_list, dim_list):
    ndim = len(dim)
    fid.createDimension(dname, ndim)
    dim_ref = fid.createVariable(dname, np.dtype('float32'), (dname,))
    dim_ref[:] = dim[:]

  # Create new variables
  var_ref = fid.createVariable(vname, np.dtype('float32'), tuple(dname_list))
  var_ref[:] = var[:]

  # Close the file
  fid.close()


def save_multiple_data_to_netcdf(fname, dname_list, dim_list, vname_list, vdim_list, var_list):
  """
  " Simply save some variables to a nc file
  "
  " fname: file name
  "
  " The order of dimensions should be consistent, e.g.,
  "   dname_list: ['time', 'lat', 'lon']
  "   dim_list  : [time, lat, lon]
  "   vname_list: ['data1', 'data2', ...]
  "   vdim_list: [ ['time', 'lat', 'lon'], ['lon', 'lat'] ]
  "   var_list  : [data1(time, lat, lon), data2(lat, lon), ...]
  """

  # Open a file to write
  fid = Dataset(fname, 'w')

  # Create dimensions
  for dname, dim in zip(dname_list, dim_list):
    ndim = len(dim)
    fid.createDimension(dname, ndim)
    dim_ref = fid.createVariable(dname, np.dtype('float32'), (dname,))
    dim_ref[:] = dim[:]

  # Create new variables
  for vname, vdim, var in zip(vname_list, vdim_list, var_list):
    var_ref = fid.createVariable(vname, np.dtype('float32'), tuple(vdim))
    print('[Putian Debug] var_ref shape: ', var_ref.shape)
    print('[Putian Debug] var shape: ', var.shape)
    var_ref[:] = var[:]

  # Close the file
  fid.close()


def save_multiple_data_to_netcdf(fname, dname_list, dim_list, vname_list, vdim_list, var_list):
  """
  " Simply save some variables to a nc file
  "
  " fname: file name
  "
  " The order of dimensions should be consistent, e.g.,
  "   dname_list: ['time', 'lat', 'lon']
  "   dim_list  : [time, lat, lon]
  "   vname_list: ['data1', 'data2', ...]
  "   vdim_list: [ ['time', 'lat', 'lon'], ['lon', 'lat'] ]
  "   var_list  : [data1(time, lat, lon), data2(lat, lon), ...]
  """

  # Open a file to write
  fid = Dataset(fname, 'w')

  # Create dimensions
  for dname, dim in zip(dname_list, dim_list):
    ndim = len(dim)
    fid.createDimension(dname, ndim)
    dim_ref = fid.createVariable(dname, np.dtype('float32'), (dname,))
    dim_ref[:] = dim[:]

  # Create new variables
  for vname, vdim, var in zip(vname_list, vdim_list, var_list):
    var_ref = fid.createVariable(vname, np.dtype('float32'), tuple(vdim))
    print('[Putian Debug] var_ref shape: ', var_ref.shape)
    print('[Putian Debug] var shape: ', var.shape)
    var_ref[:] = var[:]

  # Close the file
  fid.close()


if __name__ == '__main__':
  # Get first command line argument as the input hdf4 file name
  ncFile = sys.argv[1]

  # Print the hdf4 file info on the screen
  ncdump(ncFile, verb=True)
