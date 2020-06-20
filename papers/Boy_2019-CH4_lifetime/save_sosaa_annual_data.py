import sys
sys.path.insert(0, '/users/putian/scripts/science-helper/')

import numpy as np
import xarray as xr

# pypack
import pypack.sosaa as ppsosaa
import pypack.tools as pptools
import pypack.functions as ppfunc


# ============================================================================ #
#
# Helper Functions
#
# ============================================================================ #

def read_whole_year_data(case_dir):
  print('Reading case data from {0} ...'.format(case_dir))

  # Read the first month data 
  case1 = ppsosaa.SosaaDat(case_dir + '/output-01')
  case1.get_dimensions()  # time, lev
  case1.get_variables_from_file('C5H8'    , ('time', 'lev'), 'Gas_C5H8.dat' )
  case1.get_variables_from_file('APINENE' , ('time', 'lev'), 'Gas_APINENE.dat' )
  case1.get_variables_from_file('BPINENE' , ('time', 'lev'), 'Gas_BPINENE.dat' )
  case1.get_variables_from_file('CARENE'  , ('time', 'lev'), 'Gas_CARENE.dat'  )
  case1.get_variables_from_file('LIMONENE', ('time', 'lev'), 'Gas_LIMONENE.dat')
  case1.get_variables_from_file('CINEOLE' , ('time', 'lev'), 'Gas_CINEOLE.dat' )
  case1.get_variables_from_file('OMT'     , ('time', 'lev'), 'Gas_OMT.dat')
  case1.get_variables_from_file('MYRCENE' , ('time', 'lev'), 'Gas_MYRCENE.dat' )
  case1.get_variables_from_file('SABINENE', ('time', 'lev'), 'Gas_SABINENE.dat')
  case1.get_variables_from_file('emi_CARENE', ('time', 'lev'), 'Emi_CARENE.dat' )
  case1.get_variables_from_file('emi_C5H8'  , ('time', 'lev'), 'Emi_C5H8.dat' )

  # Read the other month data and merge them to the first month data
  for im in range(2, 13):
    print('Merging the month {0:02d} ...'.format(im))
    case_tmp = ppsosaa.SosaaDat(case_dir + '/output-{0:02d}'.format(im))
    case_tmp.get_dimensions()  # time, lev
    case_tmp.get_variables_from_file('C5H8'    , ('time', 'lev'), 'Gas_C5H8.dat' )
    case_tmp.get_variables_from_file('APINENE' , ('time', 'lev'), 'Gas_APINENE.dat' )
    case_tmp.get_variables_from_file('BPINENE' , ('time', 'lev'), 'Gas_BPINENE.dat' )
    case_tmp.get_variables_from_file('CARENE'  , ('time', 'lev'), 'Gas_CARENE.dat'  )
    case_tmp.get_variables_from_file('LIMONENE', ('time', 'lev'), 'Gas_LIMONENE.dat')
    case_tmp.get_variables_from_file('CINEOLE' , ('time', 'lev'), 'Gas_CINEOLE.dat' )
    case_tmp.get_variables_from_file('OMT'     , ('time', 'lev'), 'Gas_OMT.dat')
    case_tmp.get_variables_from_file('MYRCENE' , ('time', 'lev'), 'Gas_MYRCENE.dat' )
    case_tmp.get_variables_from_file('SABINENE', ('time', 'lev'), 'Gas_SABINENE.dat')
    case_tmp.get_variables_from_file('emi_CARENE', ('time', 'lev'), 'Emi_CARENE.dat' )
    case_tmp.get_variables_from_file('emi_C5H8'  , ('time', 'lev'), 'Emi_C5H8.dat' )
  
    # Concatenate all the months
    case1.xrds = xr.concat([case1.xrds, case_tmp.xrds], dim='time')
  
  # Calculate monoterpenes
  case1.xrds['MT'] = \
      case1.xrds['APINENE'] + \
      case1.xrds['BPINENE' ] + \
      case1.xrds['CARENE'  ] + \
      case1.xrds['LIMONENE'] + \
      case1.xrds['CINEOLE' ] + \
      case1.xrds['OMT'     ] + \
      case1.xrds['MYRCENE' ] + \
      case1.xrds['SABINENE']

  case1.xrds['emi_MT'] = case1.xrds['emi_CARENE']/0.396

  return case1


# ============================================================================ #
#
# Read the original monthly data from SOSAA case output, merge into a yearly
# dataset, then save them.
#
# ============================================================================ #

case_folder = '/scratch/project_2001025/sosaa/cases'
data_folder = '/scratch/project_2001025/putian/Boy_2019-CH4_lifetime'

case = {}

case['BASE'] = read_whole_year_data(case_folder + '/boy2019-BASE')
case['E6C6'] = read_whole_year_data(case_folder + '/boy2019-E6C6')
case['E6C0'] = read_whole_year_data(case_folder + '/boy2019-E6C0')

case['BASE'].xrds.to_netcdf(data_folder + '/BASE.nc')
case['E6C6'].xrds.to_netcdf(data_folder + '/E6C6.nc')
case['E6C0'].xrds.to_netcdf(data_folder + '/E6C0.nc')
