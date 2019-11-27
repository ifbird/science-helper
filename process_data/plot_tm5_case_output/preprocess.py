import numpy as np
from netCDF4 import Dataset

from local import *

def calculate_sample_veg_monthly_avg(fprefix, y, m):
  """
  " Calculate monthly average of vegetation cover from original tm5 input veg data
  " File name sample:
  "   tm5_input_sample/meteo-veg/ec-ei-an0tr6-sfc-glb100x100-2009-veg_20090101_00p06.nc
  " fprefix: /.../tm5_input_sample/meteo-veg/ec-ei-an0tr6-sfc-glb100x100
  " y: '2009'
  " m: '01'
  "
  " cvl_monavg, cvh_monavg: [nlat, nlon]
  """

  iy = int(y)
  im = int(m)
  md = month_day[im-1]

  for d_1 in range(md):
    # Current day
    d = d_1 + 1

    # File name
    fname = '{prefix}-{year}-veg_{year}{month}{day:02d}_00p06.nc'.format( \
      prefix=fprefix, year=y, month=m, day=d)
    # print('Reading veg file {0}'.format(fname))

    # Get the daily mean data
    fid = Dataset(fname, 'r')
    cvl_dayavg = np.mean(fid.variables['cvl'][:, :, :], axis=0)
    cvh_dayavg = np.mean(fid.variables['cvh'][:, :, :], axis=0)

    # Add up to the monthly data
    if d == 1:  # initiate on the first day
      lon = fid.variables['lon'][:]
      lat = fid.variables['lat'][:]
      nlon = len(lon)
      nlat = len(lat)

      cvl_monavg = np.zeros( (nlat, nlon) )
      cvh_monavg = np.zeros( (nlat, nlon) )

    cvl_monavg += cvl_dayavg
    cvh_monavg += cvh_dayavg

    # print(m, np.mean(cvl_dayavg), np.mean(cvh_dayavg))

    # Close the file
    fid.close

  # Divided by the month day
  cvl_monavg /= md
  cvh_monavg /= md

  # print(m, np.mean(cvl_monavg), np.mean(cvh_monavg))

  return (cvl_monavg, cvh_monavg, lon, lat)


def save_sample_veg_monthly_avg(month_range):
  months = range(month_range[0], month_range[1] + 1)
  nmonth = month_range[1] - month_range[0] + 1

  # Save monthly data in one file
  fname = './data/tm5_input_sample-veg-2009-monthly.nc'
  fid = Dataset(fname, 'w')

  # File prefix
  fprefix = '/media/pzzhou/Seagate Expansion Drive' + \
    '/data/ecearth3/tm5mp/tm5_input_sample/meteo-veg/ec-ei-an0tr6-sfc-glb100x100'

  # Save the monthly data in one file
  first_loop = True
  for i in range(nmonth):
    # Month number
    month = months[i]
    print('Saving {0} ...'.format(month))

    # Month string
    m_str = '{:02d}'.format(month)

    # Get monthly avg data
    cvl_monavg, cvh_monavg, lon, lat = calculate_sample_veg_monthly_avg(fprefix, '2009', m_str)
    nlon, nlat = lon.size, lat.size

    # Create dimensions and variables in the first loop
    if first_loop:
      # Create dimensions
      fid.createDimension('lon', nlon)
      fid.createDimension('lat', nlat)
      fid.createDimension('time', nmonth)

      # Create dimension variables
      lon_new = fid.createVariable('lon', np.dtype('float32'), ('lon', ))
      lat_new = fid.createVariable('lat', np.dtype('float32'), ('lat', ))
      time_new = fid.createVariable('time', np.dtype('float32'), ('time', ))

      # Set dimension values
      lon_new[:] = lon[:]
      lat_new[:] = lat[:]
      time_new[:] = np.array(months)

      # Create other variables
      cvl_new = fid.createVariable('cvl', np.dtype('float32'), ('time', 'lat', 'lon'))
      cvh_new = fid.createVariable('cvh', np.dtype('float32'), ('time', 'lat', 'lon'))
      
      first_loop = False
    
    # Set the values for cvl and cvh
    cvl_new[i, :, :] = cvl_monavg[:, :]
    cvh_new[i, :, :] = cvh_monavg[:, :]

  fid.close()


if __name__ == '__main__':
  # Save the monthly averaged vegetation cover (cvl, cvh) data in one nc file
  save_sample_veg_monthly_avg((1, 12))
