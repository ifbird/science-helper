import sys

import numpy as np
import xarray as xr

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from mpl_toolkits.mplot3d import proj3d

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


# ----- Plot orography ----- #

# Read oro data, oro is saved as geopotential [m2 s-1]
oro_file_path = '/scratch/project_2001025/tm5mp/TM5_METEO/2009/ec-ei-an0tr6-sfc-glb100x100-0000-oro.nc'
oro_xrds = xr.open_dataset(oro_file_path)

out_dir = '/scratch/project_2001025/tm5mp/runs/boy2019-E0C6/rundir/output-2009-03'
out_gen_file_path = out_dir + '/general_TM5_general_output_200901_monthly.nc'
gen_xrds = xr.open_dataset(out_gen_file_path)

X_gen, Y_gen = np.meshgrid(gen_xrds['lat'], gen_xrds['lon'])
# print(gen_xrds['gph3D'][0, 0, :, :].max())

# print(oro_xrds['lat'])
# print(oro_xrds['lon'])
# print(oro_xrds['oro'])
# print(oro_xrds.attrs)


fg = plt.figure()
ax = fg.add_subplot(1, 1, 1, projection = '3d')

X, Y = np.meshgrid(oro_xrds['lat'].values, oro_xrds['lon'].values)
Z = oro_xrds['oro'].values.transpose() / oro_xrds.attrs['grav'] / 100.0

surf = ax.plot_surface(X, Y, Z, \
  cmap=cm.coolwarm, \
  linewidth=0, \
  antialiased=True)

Z_gen = gen_xrds['gph3D'][0, 10, :, :].values.transpose() / 100.0
surf = ax.plot_surface(X_gen, Y_gen, Z_gen, \
  cmap=cm.coolwarm, \
  linewidth=0, \
  antialiased=True)

Z_gen = gen_xrds['gph3D'][0, 20, :, :].values.transpose() / 100.0
surf = ax.plot_surface(X_gen, Y_gen, Z_gen, \
  cmap=cm.coolwarm, \
  linewidth=0, \
  antialiased=True)

plt.show()

# fig = plt.figure()
# ax = fig.gca(projection='3d')
# 
# # Make data.
# X = np.arange(-5, 5, 0.25)
# Y = np.arange(-5, 5, 0.25)
# X, Y = np.meshgrid(X, Y)
# R = np.sqrt(X**2 + Y**2)
# Z = np.sin(R)
# 
# # Plot the surface.
# surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
#                        linewidth=0, antialiased=False)
# 
# # Customize the z axis.
# ax.set_zlim(-1.01, 1.01)
# ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
# 
# # Add a color bar which maps values to colors.
# fig.colorbar(surf, shrink=0.5, aspect=5)
# 
# plt.show()


# fig = plt.figure()
# ax = fig.add_subplot(111, projection = '3d')
# x = [1, 2, 3]
# y = [4, 5, 6]
# z = [7, 8, 9]
# sc = ax.scatter(x,y,z)
# 
# #####################    
# x2, y2, _ = proj3d.proj_transform(1, 4, 5, ax.get_proj())
# print(x2, y2)   # project 3d data space to 2d data space
# print(ax.transData.transform((x2, y2)))  # convert 2d space to screen space
# #####################
# def on_motion(e):
#     # move your mouse to (1,1,1), and e.xdata, e.ydata will be the same as x2, y2
#     print(e.x, e.y, e.xdata, e.ydata)
# 
# def on_click(e):
#     # move your mouse to (1,1,1), and e.xdata, e.ydata will be the same as x2, y2
#     print(e.x, e.y, e.xdata, e.ydata)
# 
# # fig.canvas.mpl_connect('motion_notify_event', on_motion)
# fig.canvas.mpl_connect('button_press_event', on_click)
# plt.show()

# fig, ax = plt.subplots()
# ax.plot(np.random.rand(10))
# 
# def onclick(event):
#     print('%s click: button=%d, x=%f, y=%f, xdata=, ydata=' %
#           ('double' if event.dblclick else 'single', event.button,
#            event.x, event.y))
#     # print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
#     #       ('double' if event.dblclick else 'single', event.button,
#     #        event.x, event.y, event.xdata, event.ydata))
# 
# cid = fig.canvas.mpl_connect('button_press_event', onclick)
# 
# plt.show()
