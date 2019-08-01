from .fileio import *

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


if __name__ == '__main__':
  # Get first command line argument as the input hdf4 file name
  ncFile = sys.argv[1]

  # Print the hdf4 file info on the screen
  ncdump(ncFile, verb=True)
