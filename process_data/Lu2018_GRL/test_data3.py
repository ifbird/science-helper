#==============================================================================#
#
# Header
#
#==============================================================================#
import os
import sys
import shutil

import numpy as np
import numpy.ma as ma
from pyhdf.SD import *

import putian_functions as pf
import local_functions as lf

data3 = np.load('data3_input.npz')

data_mhgsrd = data3['input_mhgsrd'][()]
data_mh     = data3['input_mh'    ][()]
data_pi     = data3['input_pi'    ][()]

#==============================================================================#
#
# Check by the plot
#
#==============================================================================#
pm = 'cyl'
reg = lf.reg_glob


# mhgsrd
lat = data_mhgsrd['lat']
lon = data_mhgsrd['lon']

z = data_mhgsrd['cvh']
zm = ma.array(z, mask = z<0.2)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/tm5veg_mhgsrd_cvh.png')

z = data_mhgsrd['cvl']
zm = ma.array(z, mask = z<0.2)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/tm5veg_mhgsrd_cvl.png')


# mh
lat = data_mh['lat']
lon = data_mh['lon']

z = data_mh['cvh']
zm = ma.array(z, mask = z<0.2)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/tm5veg_mh_cvh.png')

z = data_mh['cvl']
zm = ma.array(z, mask = z<0.2)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/tm5veg_mh_cvl.png')


# pi
lat = data_pi['lat']
lon = data_pi['lon']

z = data_pi['cvh']
zm = ma.array(z, mask = z<0.2)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/tm5veg_pi_cvh.png')

z = data_pi['cvl']
zm = ma.array(z, mask = z<0.2)
lf.plot_simple_pcolor_map(lon, lat, zm, pm, reg, './figures/tm5veg_pi_cvl.png')

sys.exit()


"""
if os.path.exists(fname_tm5_input_veg_6kbp02_mhgsrd):
  os.remove(fname_tm5_input_veg_6kbp02_mhgsrd)

# Read input data modified from Lu2018
tv = data3['input_mhgsrd'][()]['tv']
cvh = data3['input_mhgsrd'][()]['cvh']
cvl = data3['input_mhgsrd'][()]['cvl']
lon = data3['input_mhgsrd'][()]['lon']
lat = data3['input_mhgsrd'][()]['lat']
nlon, nlat = lon.size, lat.size

#=================================================================#
fid = SD(fname_tm5_input_veg_6kbp02_mhgsrd, SDC.WRITE|SDC.CREATE)

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
d.endaccess()

d = fid.create('LON', SDC.FLOAT64, nlon)
dim0 = d.dim(0)
dim0.setname('LON')
d.endaccess()

# Create datasets for tv
for i in range(lf.nvt):
  tvstr = lf.tm5_tvname[i]
  # print(tvstr)
  d = fid.create(tvstr, SDC.FLOAT64, (nlat, nlon))
  # d.set(0)
  # dim0 = d.dim(0)
  # d.dim(1) = lon
  dim0 = d.dim(0)
  dim1 = d.dim(1)
  dim0.setname('LAT')
  dim1.setname('LON')
  # dim0 = lat
  # dim1 = lon

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
# Close dataset
d.endaccess()

d = fid.create('cvl', SDC.FLOAT64, (nlat, nlon))
dim0 = d.dim(0)
dim1 = d.dim(1)
dim0.setname('LAT')
dim1.setname('LON')
d[:] = cvl
# Close dataset
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
fid_raw.end()

# Check file info
fid, fattr, fdset = pf.h4dump(fname_tm5_input_veg_6kbp02_mhgsrd, True, 'output_tm5_input_veg_6kbp02_mhgsrd.txt')

sys.exit()

#=================================================================#

# Copy raw file to new file
shutil.copyfile(fname_tm5_input_veg_200902_raw, fname_tm5_input_veg_6kbp02_mhgsrd)



fid, fattr, fdset = pf.h4dump(fname_tm5_input_veg_6kbp02_mhgsrd, False, 'output_tm5_input_veg_6kbp02_mhgsrd.txt')

# Open the newly copied veg file to append data
# fid_sd = SD(fname_tm5_input_veg_6kbp02_mhgsrd, SDC.READ|SDC.WRITE|SDC.CREATE)
fid_sd = SD(fname_tm5_input_veg_6kbp02_mhgsrd, SDC.WRITE)

#----- Set new values to tv, cvh, and cvl -----#
for i in range(lf.nvt):
  tvstr = lf.tm5_tvname[i]
  print(tvstr)
  d = fid_sd.select(tvstr)
  print(d.unit)
  print(d.time1)
  print(d)
  print(d.get())
  d = np.float32(tv[i, :, :])
  d.endaccess()

d = fid_sd.select('cvh')
d = np.float32(cvh)
d.endaccess()

d = fid_sd.select('cvl')
d = np.float32(cvl)
d.endaccess()

fid.end()


fname_tm5_input_veg_6kbp02_mh  = '../data/tm5_input_modified/ec-ei-an0tr6-sfc-glb100x100-veg_6kbp02_mh.hdf'
fname_tm5_input_veg_185002_pi  = '../data/tm5_input_modified/ec-ei-an0tr6-sfc-glb100x100-veg_185002_pi.hdf'
"""
