"""
" File IO
"""
import os
import sys

import numpy as np
import pandas as pd


def set_sysstdout(verb=True, log_file=None):
  """
  " Set the output location to printf
  " verb: 
  "   log_file is None: screen
  "   log_file is not None: file (log_file)
  " not verb:
  "   do not output
  """
  # Set output location
  if verb:
    # To file
    if log_file is not None:
      sys.stdout = open(log_file, 'w')
    # To screen
    else:
      sys.stdout = sys.__stdout__
  else:
    # To nothing (do not output anything)
    sys.stdout = open(os.devnull, 'w')

  return sys.stdout.write


def eol(n=1):
  """
  " Change n new lines.
  " Calling set_sysstdout before eol is recommended.
  " Use eol directly, do not use print(eol).
  """
  # printf("%s" % chr(10) * n)
  sys.stdout.write("%s" % chr(10) * n)


def read_avaasmear_csv(file_name, var_name_list=None):
  #
  # Read csv
  #
  # The format of the data file
  #
  # Year,Month,Day,Hour,Minute,Second,<variable_names>
  #

  # Date column names in header
  header_date = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']
  
  # Read data to pandas dataframe
  df = pd.read_csv(file_name)

  # Read raw data
  print(df[header_date].shape)
  date = pd.to_datetime(df[header_date])

  # Delete 6 date columns and add one date column
  df.drop(header_date, axis=1, inplace=True)
  df.insert(0, 'date', date)

  # Rename the columns
  if var_name_list is not None:
    nvar = len(var_name_list)
    ncol = len(df.columns[1:])  # count starting from variables
    if nvar == ncol:
      for i, var_name in enumerate(var_name_list):
        df.rename(columns={ df.columns[i+1]: var_name }, inplace = True) 
    else:
      print('[ERROR] The number of input variables names is not the same as that in the input data.')
      print('[ERROR] The column names are not changed.')

  return df


def read_avaasmear(file_name, file_format, var_name_list=None):
  if file_format == 'csv':
    df = read_avaasmear_csv(file_name, var_name_list)
  elif file_format == 'txt':
    pass
  else:
    pass
  
  # Return a pandas dataframe
  return df


if __name__== '__main__':
  # Test read_avaasmear_csv
  file_name = '20160601_0630-taum_ustar-30min.csv'
  df = read_avaasmear_csv(file_name, ['taum', 'ustar'])

  print(df)

  print(df.columns)
  print(df.columns[1:])
  print(len(df.columns[1:]))
