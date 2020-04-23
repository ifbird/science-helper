import os
import sys
# sys.path.insert(0, 'your_package_path')

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.ticker as mticker

# Cartopy for the global map drawing
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER



def plot_cartopy_basic_map(map_proj):
  fg = plt.figure(figsize=(10, 5))
  ax = fg.add_subplot(1, 1, 1, projection=map_proj)

  # Plot the global map
  ax.set_global()

  # Plot local map
  # ax.set_extent([west, east, south, north], transform)

  # Add a standard image to the map
  # Plot how the land and ocean looks like
  # ax.stock_img()

  # Add map features
  # ax.add_feature(cfeature.LAND)
  # ax.add_feature(cfeature.OCEAN)
  # ax.add_feature(cfeature.LAKES)
  # ax.add_feature(cfeature.RIVERS)
  # ax.add_feature(cfeature.BORDERS)  # country borders
  ax.add_feature(cfeature.COASTLINE)

  # Add grid lines
  ax.gridlines()

  # Plot the coastlines
  # ax.coastlines()  # same effect of add_feature for coastline

  # Plot the Tissot area points showing 
  ax.tissot(facecolor='orange', alpha=0.4)

  # Plot points and the line between p1 and p2
  # Transform: what coordinate system the data are using,
  # so the data in lat and lon are in PlateCarree coordinate system.
  # Projection: how the figure is plotted.
  p1 = [24.94, 60.17]  # Helsinki
  p2 = [116.41, 39.90]  # Beijing
  ax.plot(p1[0], p1[1], 'ob', markersize=20, alpha=0.7, transform=ccrs.PlateCarree())
  ax.plot(p2[0], p2[1], 'or', markersize=20, alpha=0.7, transform=ccrs.PlateCarree())
  ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r', transform=ccrs.PlateCarree())  # straight line on the map
  ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b', transform=ccrs.Geodetic())  # along the big circle

  fg.savefig('cartopy_basic_map.png')


def plot_cartopy_map_boundary():
  fg = plt.figure(figsize=[10, 5])
  ax1 = fg.add_subplot(1, 2, 1, projection=ccrs.SouthPolarStereo())
  ax2 = fg.add_subplot(1, 2, 2, projection=ccrs.SouthPolarStereo(), sharex=ax1, sharey=ax1)
  
  # Adjust the space and position of figure and subplots
  fg.subplots_adjust(bottom=0.05, top=0.95, left=0.04, right=0.95, wspace=0.02)
  
  # Limit the map to -60 degrees latitude and below.
  ax1.set_extent([-180, 180, -90, -60], ccrs.PlateCarree())
  
  ax1.add_feature(cfeature.LAND)
  ax1.add_feature(cfeature.OCEAN)
  
  ax1.gridlines()
  ax2.gridlines()
  
  ax2.add_feature(cfeature.LAND)
  ax2.add_feature(cfeature.OCEAN)

  # Compute a circle in axes coordinates, which we can use as a boundary
  # for the map. We can pan/zoom as much as we like - the boundary will be
  # permanently circular.

  theta = np.linspace(0, 2*np.pi, 100)
  center, radius = [0.5, 0.5], 0.5
  verts = np.vstack([np.sin(2*theta), np.cos(theta)]).T
  circle = mpath.Path(verts * radius + center)

  ax2.set_boundary(circle, transform=ax2.transAxes)

  fg.savefig('cartopy_map_boundary.png')


def plot_grid_lines():
  fg = plt.figure(figsize=[10, 10])

  ax = plt.axes(projection=ccrs.Mercator())
  ax.coastlines()

  gl = ax.gridlines(crs=ccrs.PlateCarree(), \
    draw_labels=True, linewidth=2, color='gray', alpha=0.5, linestyle='--')
  gl.xlabels_top = False
  gl.xlabels_bottom = True 
  gl.ylabels_left = False
  gl.ylabels_right = True
  gl.xlines = False  # longitude lines
  gl.ylines = True   # latitude lines
  gl.xlocator = mticker.FixedLocator([-180, -45, 0, 45, 180])
  gl.xformatter = LONGITUDE_FORMATTER
  gl.yformatter = LATITUDE_FORMATTER
  gl.xlabel_style = {'size': 15, 'color': 'gray'}
  gl.xlabel_style = {'color': 'red', 'weight': 'bold'}

  fg.savefig('cartopy_grid_lines.png')


if __name__ == '__main__':
  # plot_cartopy_basic_map(ccrs.Robinson())
  # plot_cartopy_map_boundary()
  plot_grid_lines()