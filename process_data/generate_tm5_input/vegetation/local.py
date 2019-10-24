#==============================================================================#
#
# Local functions
#
#==============================================================================#

# Some setup
# c: pi, mh1, mh2
# s: iso, mon
# y: 1850, ..., 2009, or 1850_1859_mean
# m: month, 01 - 12
# d: day, 1 - 31


#
# Raw Lu2018 veg data file names
#

fdir_lu2018_veg = '/homeappl/home/putian/scripts/tm5-mp/data/lu2018_lpjg_monthly_veg'


def get_fname_lu2018_veg_lrg(c):
  newc = {'pi': 'PI', 'mh1': 'MH', 'mh2': 'MHgsrd'}
  return fdir_lu2018_veg+ '/LPJ-GUESS_monthlyoutput_{0}.txt'.format(newc[c])


def get_fname_lu2018_veg_gxx(c):
  return fdir_lu2018_veg+ '/{0}-lpjg_monthly_gxx.nc'.format(c)


#
# Raw meteo data file name as a sample
#

fdir_sample_veg = '/proj/atm/TM5_METEO/2009'
fdir_sample_srols = '/proj/atm/TM5_METEO/2009'


def get_fname_sample_veg(y, m, d):
  return fdir_sample_veg + '/ec-ei-an0tr6-sfc-glb100x100-{0}-veg_{1}_00p06.nc'.format(y, y+m+d)


def get_fname_sample_srols(y, m):
  return fdir_sample_srols + '/ec-ei-an0tr6-sfc-glb100x100-{0}-srols_{1}.nc'.format(y, y+m)


#
# New monthly veg data files
#

fdir_new_veg = '/homeappl/home/putian/scripts/tm5-mp/data/tm5_input_modified/meteo-veg'


def get_fname_new_veg(c, y, m):
  return fdir_new_veg + '/{0}/{0}-ec-ei-an0tr6-sfc-glb100x100-{1}-veg_{2}.nc'.format(c, y, y+m)


# Grid box area for 0.5x0.5
# lon, lat, gridbox_area [m-2]
# fname_gridarea_0p5x0p5 = '/proj/atm/TM5_EMISS/MACCity/gridbox_area.nc'


# Case list
case_list = ['pi', 'mh1', 'mh2']

# Year count in Lu2018 veg data
nyear = 10
nmon  = 12
ndate = nmon
month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
