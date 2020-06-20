import os
import sys

from collections import OrderedDict

import numpy as np
import xarray as xr

import argparse


# ------------------------------------------------------------------------- #
#
# Helper functions
#
# ------------------------------------------------------------------------- #


# ------------------------------------------------------------------------- #
#
# Program
#
# ------------------------------------------------------------------------- #

# ----- Define the argument parser ----- #
parser = argparse.ArgumentParser(description= \
  'Save the annual data of TM5 output for a specific variable')

# Define arguments
parser.add_argument('rundir', \
    type=str, \
    help='Project rundir, usually output folders are inside it')
parser.add_argument('outdir', \
    type=str, \
    help='Output folder, usually inside rundir, multiple folders are separated by commas')
parser.add_argument('vars', \
    type=str, \
    help='Variable name, multiple names are separated by commas')
parser.add_argument('savedir', \
    type=str, \
    help='Where to save the data, the files names are determined by prefix and outdir')
parser.add_argument('-p', action='store', dest='prefix', default='tm5', \
    help='Prefix of save file names')
parser.add_argument('-j', action='store', dest='project', default='general', \
    help='Project name for different output, e.g., general, aerocom3')

# Get the arguments
args = parser.parse_args()

# Check if rundir exist or is a folder
if not os.path.isdir(args.rundir):
  print('[Error] {0} doest not exist or is not a folder.'.format(args.rundir))
  sys.exit()

# Get the outdir list
outdir_list = [s.strip() for s in args.outdir.split(',') if s != '']
outdir_list = list(OrderedDict.fromkeys(outdir_list))

# Find the variable list and remove the empty strings
vars_list = [s.strip() for s in args.vars.split(',') if s != '']
vars_list = list(OrderedDict.fromkeys(vars_list))
vars_str = '_'.join(vars_list)

# Iterate all the outdir
for od in outdir_list:
  print('===============================')

  # Abs path of outdir
  od_path = '{0}/{1}'.format(args.rundir, od)
  print('Processing {0}'.format(od_path))

  # Check if outdir exists
  if not os.path.isdir(od_path):
    print('[Warning] {0} doest not exist or is not a folder. Skipped.'.format(od_path))
    continue

  # Read the annual data into one xarray dataset
  # time unit should be: "days since 2001-01-01 00:00",
  # but in the simulations it is set to "days since 2009-01-01 00:00".
  if args.project == 'general':
    data_files = 'general_TM5_general_output_2009*_monthly.nc'
  elif args.project == 'aerocom3':
    data_files = 'aerocom3_TM5_aerocom_global_2009*_monthly.nc'

  print('-- Reading data files {0}'.format(data_files))
  data = xr.open_mfdataset('{0}/{1}'.format(od_path, data_files), combine='by_coords')

  # Set the save file path
  save_file = '{0}-{1}-{2}-{3}_output.nc'.format(args.prefix, od, vars_str, args.project)
  save_path = '{0}/{1}'.format(args.savedir, save_file)

  # Save the data with specified variables
  print('-- Saving to {0}'.format(save_path))
  merge_data = xr.merge( [data[v] for v in vars_list] )
  merge_data.to_netcdf(save_path)
