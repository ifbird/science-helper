# Header
import os
import sys
import shutil

import numpy as np
import numpy.ma as ma
from pyhdf.SD import *

import putian_functions as pf
import local_functions as lf


def create_tm5_input_veg_file(fname, input_data, fid_raw, verb=False, output='output_veg.txt'):
  """
  " fname: name of tm5 input veg hdf4 file
  " input_data: including tv, cvh, cvl, lon, lat
  " fid_raw: 
  """

  # Delete file if exists, so create a totally new file
  if os.path.exists(fname):
    os.remove(fname)
  
  # Read input data modified from Lu2018
  tv  = input_data['tv']
  cvh = input_data['cvh']
  cvl = input_data['cvl']
  lon = input_data['lon']
  lat = input_data['lat']
  nlon, nlat = lon.size, lat.size
  
  # Open a file to write
  fid = SD(fname, SDC.WRITE|SDC.CREATE)
  
  # Set global attributes according to fid_raw
  fid.ae       = fid_raw.ae
  fid.area_m2  = fid_raw.area_m2
  fid.fname    = fname_tm5_input_veg_6kbp02_mhgsrd
  fid.format   = fid_raw.format
  fid.grav     = fid_raw.grav
  fid.gridtype = fid_raw.gridtype
  fid.latmax   = fid_raw.latmax
  fid.latmin   = fid_raw.latmin
  fid.lonmax   = fid_raw.lonmax
  fid.lonmin   = fid_raw.lonmin
  
  # Create datasets for lon and lat
  d = fid.create('LAT', SDC.FLOAT64, nlat)
  dim0 = d.dim(0)
  dim0.setname('LAT')
  d[:] = lat
  d.endaccess()
  
  d = fid.create('LON', SDC.FLOAT64, nlon)
  dim0 = d.dim(0)
  dim0.setname('LON')
  d[:] = lon
  d.endaccess()
  
  # Create datasets for tv
  for i in range(lf.nvt):
    tvstr = lf.tm5_tvname[i]
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
  
  # Add variable attributes the same as in tm5 veg 2009 raw file
  ds_names = fid.datasets()
  ds_raw = fid_raw.select('tv01')
  for dn in ds_names:
    ds = fid.select(dn)
    if not ds.iscoordvar():
      for attr_name, attr_value in ds_raw.attributes().items():
        setattr(ds, attr_name, attr_value)
  
  # Close file
  fid.end()
  # fid_raw.end()
  
  # Check file info
  fid, fattr, fdset = pf.h4dump(fname, verb, output)

  return fid, fattr, fdset


fname_tm5_input_veg_200902_raw = '../data/tm5_input_modified/ec-ei-an0tr6-sfc-glb100x100-veg_200902.hdf'
fid_raw, fattr_raw, fdset_raw = pf.h4dump(fname_tm5_input_veg_200902_raw, True, 'output_tm5_input_veg_200902_raw.txt')


data3 = np.load('data3_input.npz')
#
# MH_gsrd
#
fname_tm5_input_veg_6kbp02_mhgsrd = '../data/tm5_input_modified/ec-ei-an0tr6-sfc-glb100x100-veg_6kbp02_mhgsrd.hdf'
print(data3['input_mhgsrd'][()]['cvh'].shape)
fid_mhgsrd, fattr_mhgsrd, fdset_mhgsrd = create_tm5_input_veg_file(fname_tm5_input_veg_6kbp02_mhgsrd, data3['input_mhgsrd'][()], fid_raw, \
  verb=True, output='output_tm5_input_veg_6kbp02_mhgsrd.txt')


#
# MH
#
fname_tm5_input_veg_6kbp02_mh = '../data/tm5_input_modified/ec-ei-an0tr6-sfc-glb100x100-veg_6kbp02_mh.hdf'
fid_mh, fattr_mh, fdset_mh= create_tm5_input_veg_file(fname_tm5_input_veg_6kbp02_mh, data3['input_mh'][()], fid_raw, \
  verb=True, output='output_tm5_input_veg_6kbp02_mh.txt')


#
# PI
#
fname_tm5_input_veg_185002_pi = '../data/tm5_input_modified/ec-ei-an0tr6-sfc-glb100x100-veg_185002_pi.hdf'
fid_pi, fattr_pi, fdset_pi = create_tm5_input_veg_file(fname_tm5_input_veg_185002_pi, data3['input_pi'][()], fid_raw, \
  verb=True, output='output_tm5_input_veg_185002_pi.txt')


# Close fid_raw
fid_raw.end()


#==============================================================================#
# Check by the plot
#==============================================================================#
pm = 'cyl'
reg = lf.reg_glob


# mhgsrd
lat = fid_mhgsrd.select('LAT')[:]
lon = fid_mhgsrd.select('LON')[:]

z = fid_mhgsrd.select('cvh')[:, :]
zm = ma.array(z, mask = z==0)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/tm5veg_mhgsrd_cvh.png')

z = fid_mhgsrd.select('cvl')[:, :]
zm = ma.array(z, mask = z==0)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/tm5veg_mhgsrd_cvl.png')


# mh
lat = fid_mh.select('LAT')[:]
lon = fid_mh.select('LON')[:]

z = fid_mh.select('cvh')[:, :]
zm = ma.array(z, mask = z==0)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/tm5veg_mh_cvh.png')

z = fid_mh.select('cvl')[:, :]
zm = ma.array(z, mask = z==0)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/tm5veg_mh_cvl.png')


# pi
lat = fid_pi.select('LAT')[:]
lon = fid_pi.select('LON')[:]

z = fid_pi.select('cvh')[:, :]
zm = ma.array(z, mask = z==0)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/tm5veg_pi_cvh.png')

z = fid_pi.select('cvl')[:, :]
zm = ma.array(z, mask = z==0)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/tm5veg_pi_cvl.png')
