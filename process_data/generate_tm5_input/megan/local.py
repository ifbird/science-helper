#==============================================================================#
#
# Local functions
#
#==============================================================================#

def unit_conv(molmass, month_day):
  # molmass: molar mass, [kg mol-1]
  # [umol m-2 d-1] --> [kg m-2 s-1]
  # [mg m-2 mon-1] --> [kg m-2 s-1]: 1.0e-6/(30*86400)
  return 1.0e-6/month_day/86400.0

# Some setup
# c: pi, mh1, mh2
# s: iso, mon
# y: 1850, ..., 2009, or 1850_1859_mean


#
# Raw Lu2018 BVOC data file names
#

fdir_lu2018_bvoc = '/homeappl/home/putian/scripts/tm5-mp/data/lu2018_lpjg_monthly_bvoc/'


def get_fname_lu2018_lrg(c, s):
  return fdir_lu2018_bvoc + '/out_bvoc_{0}/m{1}_1850_1859.txt'.format(c, s)
  

def get_fname_lu2018_gxx(c, s):
  return fdir_lu2018_bvoc + '/out_bvoc_{0}/m{1}_1850_1859_gxx.nc'.format(c, s)


#
# Raw MEGAN emission data file name as a sample
#

fdir_megan_sample = '/proj/atm/TM5_EMISS/MEGAN'


def get_fname_megan_sample(s, y):
  if s == 'iso':
    return fdir_megan_sample + '/MEGAN-MACC_biogenic_{0}_isoprene.nc'.format(y)
  elif s == 'mon':
    return fdir_megan_sample + '/MEGAN-MACC_biogenic_{0}_monoterpenes.nc'.format(y)
  else:
    print('[ERROR] The species name should be iso or mon.')
    return None


#
# Generated MEGAN emission data file name
#

fdir_megan_new = '/homeappl/home/putian/scripts/tm5-mp/data/tm5_input_modified/megan'


def get_fname_megan_new(c, s, y):
  if s == 'iso':
    return fdir_megan_new + '/{0}-MEGAN-MACC_biogenic_{1}_isoprene.nc'.format(c, y)
    # return fdir_megan_new + '/MEGAN-MACC_biogenic_{0}_{1}_isoprene.nc'.format(c, y)
  elif s == 'mon':
    return fdir_megan_new + '/{0}-MEGAN-MACC_biogenic_{1}_monoterpenes.nc'.format(c, y)
    # return fdir_megan_new + '/MEGAN-MACC_biogenic_{0}_{1}_monoterpenes.nc'.format(c, y)
  else:
    print('[ERROR] The species name should be iso or mon.')
    return None

# Grid box area for 0.5x0.5
# lon, lat, gridbox_area [m-2]
fname_gridarea_0p5x0p5 = '/proj/atm/TM5_EMISS/MACCity/gridbox_area.nc'


# Case list
case_list = ['pi', 'mh1', 'mh2']

# Year count in Lu2018 BVOC data
nyear = 10
nmon  = 12
ndate = nmon
month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
