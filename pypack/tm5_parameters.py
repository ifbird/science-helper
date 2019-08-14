import numpy as np

#===== tm5 =====#
tm5 = {}

# Number of veg type
tm5['nvt'] = 20

# The grid in Lu2018 lpjg dataset is in N80 Gaussian grids with T159 resolution,
# the grid table can be checked below:
# * https://artefacts.ceda.ac.uk/badc_datadocs/ecmwf-op/grids.html#t159
# * https://rda.ucar.edu/datasets/common/ecmwf/ERA40/docs/std-transformations/dss_code_glwp.html

# Gaussian latitudes for N80 (T159, nlon=320 at equator) on nothern hemisphere
tm5['lat_N80'] = np.array([ \
  89.1416, 88.0294, 86.9108, 85.7906, 84.6699, \
  83.5489, 82.4278, 81.3066, 80.1853, 79.0640, \
  77.9426, 76.8212, 75.6998, 74.5784, 73.4570, \
  72.3356, 71.2141, 70.0927, 68.9712, 67.8498, \
  66.7283, 65.6069, 64.4854, 63.3639, 62.2425, \
  61.1210, 59.9995, 58.8780, 57.7566, 56.6351, \
  55.5136, 54.3921, 53.2707, 52.1492, 51.0277, \
  49.9062, 48.7847, 47.6632, 46.5418, 45.4203, \
  44.2988, 43.1773, 42.0558, 40.9343, 39.8129, \
  38.6914, 37.5699, 36.4484, 35.3269, 34.2054, \
  33.0839, 31.9624, 30.8410, 29.7195, 28.5980, \
  27.4765, 26.3550, 25.2335, 24.1120, 22.9905, \
  21.8690, 20.7476, 19.6261, 18.5046, 17.3831, \
  16.2616, 15.1401, 14.0186, 12.8971, 11.7756, \
  10.6542,  9.5327,  8.4112,  7.2897,  6.1682, \
   5.0467,  3.9252,  2.8037,  1.6822,  0.5607, \
  ])

# Longitude points at each latitude for reduced Gaussian grids
tm5['nlon_N80'] = np.array([ \
   18,  25,  36,  40,  45,  54,  60,  64,  72,  72, \
   80,  90,  96, 100, 108, 120, 120, 128, 135, 144, \
  144, 150, 160, 160, 180, 180, 180, 192, 192, 200, \
  200, 216, 216, 216, 225, 225, 240, 240, 240, 256, \
  256, 256, 256, 288, 288, 288, 288, 288, 288, 288, \
  288, 288, 300, 300, 300, 300, 320, 320, 320, 320, \
  320, 320, 320, 320, 320, 320, 320, 320, 320, 320, \
  320, 320, 320, 320, 320, 320, 320, 320, 320, 320, \
  ])

tm5['veg_type'] = { \
  'tv01': ('Crops, mixed farming'      , 'L'), \
  'tv02': ('Short grass'               , 'L'), \
  'tv03': ('Evergreen needleleaf trees', 'H'), \
  'tv04': ('Deciduous needleleaf trees', 'H'), \
  'tv05': ('Deciduous broadleaf trees' , 'H'), \
  'tv06': ('Evergreen broadleaf trees' , 'H'), \
  'tv07': ('Tall grass'                , 'L'), \
  'tv08': ('Desert'                    , '-'), \
  'tv09': ('Tundra'                    , 'L'), \
  'tv10': ('Irrigated crops'           , 'L'), \
  'tv11': ('Semidesert'                , 'L'), \
  'tv12': ('Ice caps and glaciers'     , '-'), \
  'tv13': ('Bogs and marshes'          , 'L'), \
  'tv14': ('Inland water'              , '-'), \
  'tv15': ('Ocean'                     , '-'), \
  'tv16': ('Evergreen shrubs'          , 'L'), \
  'tv17': ('Deciduous shrubs'          , 'L'), \
  'tv18': ('Mixed forest/woodland'     , 'H'), \
  'tv19': ('Interrupted forest'        , 'H'), \
  'tv20': ('Water and land mixtures'   , 'L'), \
  'cvh' : 'High vegetation cover', \
  'cvl' : 'Low vegetation cover' , \
  }

tm5['tvname'] = ['tv{:02d}'.format(int(i)) for i in range(1, tm5['nvt']+1)]

tm5['vtname'] = [ \
  'Crops, mixed farming'      , \
  'Short grass'               , \
  'Evergreen needleleaf trees', \
  'Deciduous needleleaf trees', \
  'Deciduous broadleaf trees' , \
  'Evergreen broadleaf trees' , \
  'Tall grass'                , \
  'Desert'                    , \
  'Tundra'                    , \
  'Irrigated crops'           , \
  'Semidesert'                , \
  'Ice caps and glaciers'     , \
  'Bogs and marshes'          , \
  'Inland water'              , \
  'Ocean'                     , \
  'Evergreen shrubs'          , \
  'Deciduous shrubs'          , \
  'Mixed forest/woodland'     , \
  'Interrupted forest'        , \
  'Water and land mixtures'   , \
  ]

tm5['veglh'] = [ \
  'L', 'L', 'H', 'H', 'H', \
  'H', 'L', '-', 'L', 'L', \
  'L', '-', 'L', '-', '-', \
  'L', 'L', 'H', 'H', 'L', \
  ]

# 999 means not available
tm5['cveg'] = np.array([ \
  0.9 , 0.85, 0.9, 0.9, 0.9, \
  0.99, 0.7 , 0.0, 0.5, 0.9, \
  0.1 , 999 , 0.6, 999, 999, \
  0.5 , 0.5 , 0.9, 0.9, 0.6, \
  ])

# Indices of low and high vegetation types, starting from 1
tm5['vegl_ind']  = np.array([1, 2, 7, 9, 10, 11, 13, 16, 17, 20])
tm5['vegh_ind'] = np.array([3, 4, 5, 6, 18, 19])

lu2018_veg_low = np.array([2, 7, 9, 13])
lu2018_veg_high = np.array([3, 4, 5, 6, 18])

# Region parameters
reg_glob360 = (-90, 90, 0, 360)  # global
reg_glob180 = (-90, 90, -180, 180)  # global
reg_wafr = ( -5, 40,  -20,  50)  # west Africa defined in Lu2018
reg_sahara = ( 10, 30,  -20,  40)  # Sahara region in Ergerer2018
