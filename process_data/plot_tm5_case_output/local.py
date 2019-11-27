case_list = ['pio', 'pic', 'piz', 'mh1', 'mh2']
case_full_name = {'pio': 'pi_01_orig', 'pic': 'pi_01_ctrl', 'piz': 'pi_01_zeroanthro', 'mh1': 'mh1_01', 'mh2': 'mh2_01'}

month_day = [31, 28, 31, 30, 31,   30, 31, 31, 30, 31,   30, 31]

# c: case
#    pi_01_orig, pi_01_ctrl, pi_01_zeroanthro, mh1_01, mh2_01
# i: item
#    spinup_6m, spinup_1y, 1y
# p: proj
#    aerocom3, general
# y: year
# m: month
# d: day

def get_fname_output(c, i, p, y, m):
  fdir = '/media/pzzhou/Seagate Expansion Drive/data/ecearth3/tm5mp/case_output'
  if p == 'aerocom3':
    fname = '{d}/{c}-{i}/output-{i}/aerocom3_TM5_aerocom_global_{y}{m}_monthly.nc'.format(d=fdir, c=case_full_name[c], i=i, y=y, m=m)
  elif p == 'general':
    fname = '{d}/{c}-{i}/output-{i}/general_TM5_general_output_{y}{m}_monthly.nc'.format(d=fdir, c=case_full_name[c], i=i, y=y, m=m)
  else:
    print('Wrong project name.')
    fname = ''

  return fname


def get_fname_lu2018_veg_raw(c):
  fdir = '/media/pzzhou/Seagate Expansion Drive/data/ecearth3/tm5mp/lu2018_lpjg_monthly_veg'

  if c in ['pi', 'pio', 'pic', 'piz']:
    fname = fdir + '/LPJ-GUESS_monthlyoutput_PI.txt'
  elif c == 'mh1':
    fname = fdir + '/LPJ-GUESS_monthlyoutput_MH.txt'
  elif c == 'mh2':
    fname = fdir + '/LPJ-GUESS_monthlyoutput_MHgsrd.txt'
  else:
    print('Wrong case name.')
    fname = ''

  return fname


def get_fname_lu2018_veg_gxx(c):
  fdir = '/media/pzzhou/Seagate Expansion Drive/data/ecearth3/tm5mp/lu2018_lpjg_monthly_veg'

  if c in ['pi', 'pio', 'pic', 'piz']:
    fname = fdir + '/pi-lpjg_monthly_gxx.nc'
  elif c == 'mh1':
    fname = fdir + '/mh1-lpjg_monthly_gxx.nc'
  elif c == 'mh2':
    fname = fdir + '/mh2-lpjg_monthly_gxx.nc'
  else:
    print('Wrong case name.')
    fname = ''

  return fname
    

def get_fname_input_veg_sample(y):
  fdir = '/media/pzzhou/Seagate Expansion Drive/data/ecearth3/tm5mp/tm5_input_sample/meteo-veg'
  fname = fdir + '/tm5_input_sample-veg-{y}-monthly.nc'.format(y=y)

  return fname



def get_fname_input_veg(c, y, m):
  fdir = '/media/pzzhou/Seagate Expansion Drive/data/ecearth3/tm5mp/tm5_input_modified/meteo-veg'
  if c in ['pio',]:
    # fname = '{fdir}/pi/pi-ec-ei-an0tr6-sfc-glb100x100-{year}-veg_{year}{month}.nc'.format( \
    #   fdir=fdir, year=y, month=m)
    fname = get_fname_input_veg_sample(y)
  elif c == 'pic':
    fname = '{fdir}/pi/pi-ec-ei-an0tr6-sfc-glb100x100-{year}-veg_{year}{month}.nc'.format( \
      fdir=fdir, year=y, month=m)
  elif c == 'piz':
    fname = '{fdir}/pi/pi-ec-ei-an0tr6-sfc-glb100x100-{year}-veg_{year}{month}.nc'.format( \
      fdir=fdir, year=y, month=m)
  elif c == 'mh1':
    fname = '{fdir}/mh1/mh1-ec-ei-an0tr6-sfc-glb100x100-{year}-veg_{year}{month}.nc'.format( \
      fdir=fdir, year=y, month=m)
  elif c == 'mh2':
    fname = '{fdir}/mh2/mh2-ec-ei-an0tr6-sfc-glb100x100-{year}-veg_{year}{month}.nc'.format( \
      fdir=fdir, year=y, month=m)
  else:
    print('Wrong case name.')
    fname = ''

  return fname


def get_fname_input_iso(c, y):
  fdir_sample = '/media/pzzhou/Seagate Expansion Drive/data/ecearth3/tm5mp/tm5_input_sample/megan'
  fdir = '/media/pzzhou/Seagate Expansion Drive/data/ecearth3/tm5mp/tm5_input_modified/megan'
  if c == 'pio':
    fname = '{fdir}/MEGAN-MACC_biogenic_{year}_isoprene.nc'.format( \
      fdir=fdir_sample, year='2009')
  elif c == 'pic':
    fname = '{fdir}/pi/pi-MEGAN-MACC_biogenic_{year}_isoprene.nc'.format( \
      fdir=fdir, year=y)
  elif c == 'piz':
    fname = '{fdir}/pi/pi-MEGAN-MACC_biogenic_{year}_isoprene.nc'.format( \
      fdir=fdir, year=y)
  elif c == 'mh1':
    fname = '{fdir}/mh1/mh1-MEGAN-MACC_biogenic_{year}_isoprene.nc'.format( \
      fdir=fdir, year=y)
  elif c == 'mh2':
    fname = '{fdir}/mh2/mh2-MEGAN-MACC_biogenic_{year}_isoprene.nc'.format( \
      fdir=fdir, year=y)
  else:
    print('Wrong case name.')
    fname = ''

  return fname


def get_fname_input_mon(c, y):
  fdir_sample = '/media/pzzhou/Seagate Expansion Drive/data/ecearth3/tm5mp/tm5_input_sample/megan'
  fdir = '/media/pzzhou/Seagate Expansion Drive/data/ecearth3/tm5mp/tm5_input_modified/megan'
  if c == 'pio':
    fname = '{fdir}/MEGAN-MACC_biogenic_{year}_monoterpenes.nc'.format( \
      fdir=fdir_sample, year='2009')
  elif c == 'pic':
    fname = '{fdir}/pi/pi-MEGAN-MACC_biogenic_{year}_monoterpenes.nc'.format( \
      fdir=fdir, year=y)
  elif c == 'piz':
    fname = '{fdir}/pi/pi-MEGAN-MACC_biogenic_{year}_monoterpenes.nc'.format( \
      fdir=fdir, year=y)
  elif c == 'mh1':
    fname = '{fdir}/mh1/mh1-MEGAN-MACC_biogenic_{year}_monoterpenes.nc'.format( \
      fdir=fdir, year=y)
  elif c == 'mh2':
    fname = '{fdir}/mh2/mh2-MEGAN-MACC_biogenic_{year}_monoterpenes.nc'.format( \
      fdir=fdir, year=y)
  else:
    print('Wrong case name.')
    fname = ''

  return fname


def get_fname_tm5_grid_area():
  fdir = '/media/pzzhou/Seagate Expansion Drive/data/ecearth3/tm5mp/tm5_grids'
  fname = fdir + '/tm5_grid_area.nc'

  return fname


def get_fname_onlinedust(c, y):
  fdir_sample = '/media/pzzhou/Seagate Expansion Drive/data/ecearth3/tm5mp/tm5_input_sample/aerosol-dust'
  fdir = '/media/pzzhou/Seagate Expansion Drive/data/ecearth3/tm5mp/tm5_input_modified/aerosol-dust'
  if c == 'pio':
    fname = fdir_sample + '/onlinedust_4.nc'
  elif c in ['pic', 'piz']:
    fname = fdir + '/pi-{y}-onlinedust_4.nc'.format(y=y)
  elif c in ['mh1',]:
    fname = fdir + '/mh1-{y}-onlinedust_4.nc'.format(y=y)
  elif c in ['mh2',]:
    fname = fdir + '/mh2-{y}-onlinedust_4.nc'.format(y=y)
  else:
    print('Wrong case name.')
    fname = ''

  return fname
