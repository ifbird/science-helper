import os
import sys
# sys.path.insert(0, 'your_package_path')

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.path as mpath

# Cartopy for the global map drawing
import cartopy.crs as ccrs
import cartopy.feature as cfeature


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
  # ax.add_feature(cfeature.LAKES, alpha=0.5)
  # ax.add_feature(cfeature.RIVERS)
  # ax.add_feature(cfeature.BORDERS)  # country borders
  ax.add_feature(cfeature.COASTLINE, linestyle=':')

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
  plt.close()


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
  center, radius = [0.5, 0.5], 1.5  # the unit is normalized for this subplot
  verts = np.vstack([np.sin(theta), np.cos(theta)]).T
  circle = mpath.Path(verts * radius + center)

  # Set the plot boudary to a circle
  ax2.set_boundary(circle, transform=ax2.transAxes)

  fg.savefig('cartopy_map_boundary.png')
  plt.close()


def plot_cartopy_web_map_service():
  fig = plt.figure(figsize=(10, 5))
  ax = fig.add_subplot(1, 1, 1, projection=ccrs.InterruptedGoodeHomolosine())
  ax.coastlines()

  ax.add_wms(wms='http://vmap0.tiles.osgeo.org/wms/vmap0',
  layers=['basic'])

  plt.show()


def plot_layout():
  fg = plt.figure(figsize=(10,10))
  ax1 = fg.add_axes([0, 0, 0.5, 1])
  ax2 = fg.add_axes([0.5, 0, 0.5, 1])
  print(dir(ax1.xaxis))
  print(ax1.xaxis.label_position)
  print(ax1.xaxis.get_label_position())
  print(ax1.xaxis.get_ticks_position())
  # plt.show()


def plot_colorbar_position():
  fig, axs = plt.subplots(3, 3, constrained_layout=True)
  for ax in axs.flat:
    pcm = ax.pcolormesh(np.random.random((20, 20)))

    fig.colorbar(pcm, ax=axs[0, :2], shrink=0.6, location='bottom')
    fig.colorbar(pcm, ax=[axs[0, 2]], location='bottom')
    fig.colorbar(pcm, ax=axs[1:, :], location='right', shrink=0.6)
    fig.colorbar(pcm, ax=[axs[2, 1]], location='left')

  plt.show()


if __name__ == '__main__':
  # plot_cartopy_basic_map(ccrs.Robinson())
  # plot_cartopy_map_boundary()
  # plot_cartopy_web_map_service()
  # plot_layout()
  plot_colorbar_position()
