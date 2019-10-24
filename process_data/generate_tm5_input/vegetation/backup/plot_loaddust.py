import sys

from pyhdf.SD import *
from netCDF4 import Dataset

import numpy as np
import numpy.ma as ma

from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
# mpl.use('Agg')
import matplotlib.pyplot as plt

import putian_functions as pf
import local_functions as lf

# inspired by http://nipunbatra.github.io/2014/08/latexify/
# params = {
#     'text.latex.preamble': ['\\usepackage{gensymb}'],
#     'image.origin': 'lower',
#     'image.interpolation': 'nearest',
#     'image.cmap': 'gray',
#     'axes.grid': False,
#     'savefig.dpi': 150,  # to adjust notebook inline plot size
#     'axes.labelsize': 8, # fontsize for x and y labels (was 10)
#     'axes.titlesize': 8,
#     'font.size': 8, # was 10
#     'legend.fontsize': 6, # was 10
#     'xtick.labelsize': 8,
#     'ytick.labelsize': 8,
#     'text.usetex': True,
#     'figure.figsize': [3.39, 2.10],
#     'font.family': 'serif',
# }

# mpl.rcParams.update(params)

# Files of three cases
case_list = ['pi', 'mh', 'mhgsrd']

fdir = {}
fdir['pi'] = '/wrk/putian/tm5-mp-1850/rundir/output'
fdir['mh'] = '/wrk/putian/tm5-mp-mh/rundir/output'
fdir['mhgsrd'] = '/wrk/putian/tm5-mp-mhgsrd/rundir/output'

fname = {}
for i in case_list:
  fname[i] = fdir[i] + '/aerocom3_TM5_JPK_global_200902_monthly.nc'

# Read data from files
fid = {}
for i in case_list:
  fid[i] = Dataset(fname[i], 'r')

# Dimensions, the same for different cases
print('Reading data ...')
lon120 = fid['pi'].variables['lon'][:]
lat90  = fid['pi'].variables['lat'][:]

nlon120 = lon120.size
nlat90  = lat90.size

# Dust load
loaddust = {}
for i in case_list:
  loaddust[i] = np.squeeze(fid[i].variables['loaddust'][:])*1.0e3  # [g m-2], [90, 120] after squeeze
  # print(i)
  # lf.show_statistics(loaddust[i])
  
# lf.show_statistics(loaddust['mh'] - loaddust['mhgsrd'])
# sys.exit()

# Area
# area = fid['pi'].variables['area'][:]
# print(area.shape)
# sys.exit()

# Region mask for west Africa
# my_reg_wafr = [5, 30, -20, 30]
my_reg_wafr = lf.reg_wafr
regm_lat = (lat90>=my_reg_wafr[0]) & (lat90<=my_reg_wafr[1])
regm_lon = (lon120>=my_reg_wafr[2]) & (lon120<=my_reg_wafr[3])

# Total dustload in [g m-2] within the region reg_wafr
total_loaddust_wafr_pi     = np.sum(loaddust['pi'][np.ix_(regm_lat, regm_lon)])
total_loaddust_wafr_mhgsrd = np.sum(loaddust['mhgsrd'][np.ix_(regm_lat, regm_lon)])
rel_total_loaddust_wafr = (total_loaddust_wafr_mhgsrd - total_loaddust_wafr_pi) / total_loaddust_wafr_pi
# diff_mhgsrd_pi = loaddust['mhgsrd'] - loaddust['pi']
# abs_diff_wafr = np.sum(diff_mhgsrd_pi[np.ix_(regm_lat, regm_lon)])
# rel_diff_wafr = np.sum(loaddust['mhgsrd'][np.ix_(regm_lat, regm_lon)]) - np.sum(loaddust['pi'][np.ix_(regm_lat, regm_lon)])
print('Relative total dust load change: ', rel_total_loaddust_wafr)  # -0.3498154 ~ -35%
# sys.exit()

#
# Plot loaddust
#
print('Plotting loaddust ...')

DPI = 200


# cm = plt.get_cmap('Wistia')
cm = plt.get_cmap('autumn_r')
# cm = plt.get_cmap('YlOrBr')
# cm = plt.get_cmap('default')
# cm_diff = plt.get_cmap('BrBG_r')
vmin, vmax = 0.1, 1.6
vmin_diff, vmax_diff = -0.04, 0.04
ticks_diff = [-0.04, -0.03, -0.02, -0.01, 0, 0.01, 0.02, 0.03, 0.04]
eps = vmin
eps_diff = 5.0e-4
alpha = 0.9
pm = 'cyl'

# Initiate figure
fg, ax = plt.subplots(3, 1, figsize=(16, 24), dpi=DPI)

# Plot dataset in subplots
for a, c in zip(ax.flatten(), case_list):
  z = loaddust[c]
  zm = ma.array(z, mask=z<vmin)
  m, h = lf.plotax_pcolormesh(a, lon120, lat90, zm, vmin=vmin, vmax=vmax, pm=pm, reg=lf.reg_glob, cmap=plt.get_cmap('Wistia'), alpha=0.6)
  
  # Set subtitles
  a.set_title(c, fontsize=20)
  a.tick_params(labelsize=18)
  
# z = loaddust['mhgsrd'] - loaddust['mh']
# zm = ma.array(z, mask=z==0)
# m, h = lf.plotax_pcolormesh(ax[1,1], lon120, lat90, zm, vmin=None, vmax=None, pm=pm, reg=lf.reg_glob)
  
# Add one colorbar for all
# fg.subplots_adjust(left=0.05, right=0.85, bottom=0.1, top=0.9, wspace=0.1, hspace=0.01)
fg.subplots_adjust(left=0.05, right=0.85, wspace=0.1, hspace=0.10)
cax = fg.add_axes([0.9, 0.25, 0.02, 0.5])
cb = fg.colorbar(h, cax=cax)
cb.ax.tick_params(labelsize=20)

# Set figure title
fg.suptitle('{0:s}'.format('loaddust [g m-2]'), fontsize=20)
  
# Save the figure
fg.savefig('{0:s}{1:s}.png'.format('./figures/', 'loaddust_pi_mh_mhgsrd'), dpi=DPI)
plt.show()

# Close the figure
# plt.clf()