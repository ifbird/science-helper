import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
# mpl.use('Agg')


# Recommended colormaps
# BVOC emissions:
#   Greens: white to green


def create_cmap_norm_from_bounds(cm_name, bounds):
  # Set colormap
  ncolors = len(bounds) - 1
  cmap_tmp = mpl.cm.get_cmap(cm_name, ncolors)
  colors = cmap_tmp(np.arange(ncolors))
  cmap = mpl.colors.ListedColormap(colors)  # create colormap object
  norm = mpl.colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)  # create norm index for pcolormesh

  return cmap, norm


def ll2xy_for_map_pcolor(lon, lat, m):
  """
  Calculate x, y from lon and lat, and extend lon and lat to the corners for pcolor or pcolormesh
  lon, lat should be monotonic
  """

  # Grid interval
  dlon = lon[1] - lon[0]
  dlat = lat[1] - lat[0]

  # Extend lon and lat
  lonp = np.concatenate( (lon-dlon*0.5, [lon[-1]+dlon*0.5]) )
  latp = np.concatenate( (lat-dlat*0.5, [lat[-1]+dlat*0.5]) )

  # Generate 2D mesh grid
  xp, yp = np.meshgrid(lonp, latp)
  xpm, ypm = m(xp, yp)
  # print(lonp.size, latp.size)
  # print(lonp, latp)
  # xpm, ypm = m(lonp, latp)

  return xpm, ypm


def plot_basemap(ax, pm, reg=[-90, 90, -180, 180], parallels=np.arange(-90, 91, 15.0), meridians=np.arange(-180.0, 181.0, 30.0)):
  """  
  llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
  are the lat/lon values of the lower left and upper right corners of the map.
  reg: [south, north, west, east]

  resolution = 'c' means use crude resolution coastlines.
  """

  color = 'lightgray'

  # Create basemap
  m = Basemap(projection=pm, lon_0=0, lat_0=0, llcrnrlat=reg[0], urcrnrlat=reg[1], llcrnrlon=reg[2], urcrnrlon=reg[3], \
    resolution='c', ax=ax)

  # Draw coastlines and fill the continent
  # If you do not want to show boundaries of inland lakes and rivers:
  # one way is: do not draw coast lines, set the same color for continent, lakes and rivers
  # the other way: also set the color of coast lines the same as others
  m.drawcoastlines(linewidth=0.5)
  # m.fillcontinents(color=color, lake_color=color)
  # m.drawrivers(color=color)

  # Draw country boundaries
  # m.drawcountries(linewidth=0.25)

  # Draw parallels and meridians.
  # labels = [left,right,top,bottom]
  m.drawparallels(parallels, labels=[True, False, False, False], fontsize=18)  # draw latitude lines every 30 degrees
  m.drawmeridians(meridians, labels=[False, False, False, True], fontsize=18)  # draw longitude lines every 60 degrees
  # m.drawmapboundary(fill_color='aqua')  # draw the edge of map projection region  

  # land-sea mask
  # m.drawlsmask(land_color='coral', ocean_color='aqua', lakes=False)
  
  return m


def plot_mon_emis(data_dict):
  #
  # Plot the original land data
  #

  # Coordinates
  lon_land, lat_land = data_dict['pi']['lon_land'], data_dict['pi']['lat_land']
  nland = lon_land.size
  
  # Set colormap
  bounds = np.array([0.0, 1, 2, 4, 6, 8, 10])  # colormap boundaries
  # cmap_tmp = mpl.cm.autumn_r( np.linspace(0.0, 1.0, bounds.size-1) )  # start point of colormap 'Greens'
  cmap_tmp = mpl.cm.rainbow( np.linspace(0.0, 1.0, bounds.size-1) )  # start point of colormap 'Greens'
  # cmap_tmp1 = np.concatenate( ([[237.0/255.0, 201.0/255.0, 175.0/255.0, 1.0]], cmap_tmp), axis=0 )  # add some other colors to the colormap
  cmap = colors.ListedColormap(cmap_tmp)  # create colormap object
  norm = colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)  # create norm index for pcolormesh

  # cm = plt.get_cmap('Wistia')
  # cm = plt.get_cmap('autumn_r')
  # cm = plt.get_cmap('YlOrBr')
  # cm = plt.get_cmap('default')
  # cm_diff = plt.get_cmap('BrBG_r')
  # vmin, vmax = 0.1, 1.6
  # vmin_diff, vmax_diff = -0.04, 0.04
  # ticks_diff = [-0.04, -0.03, -0.02, -0.01, 0, 0.01, 0.02, 0.03, 0.04]
  # eps = vmin
  # eps_diff = 5.0e-4
  # alpha = 0.7
  pm = 'moll'
  plot_reg_glob = lf.reg_glob

  # Initiate figure
  fg, ax = plt.subplots(3, 1, figsize=(16, 24), dpi=DPI)
  
  # Plot dataset in subplots
  titles = ['PI', 'MH', 'MH_gsrd']
  for a, c, t in zip(ax.flatten(), lf.clist, titles):
    print('Plotting {0} ...'.format(c))
    z = np.nanmean(data_dict[c]['emis_avg']*unit_conv, axis=0)  # annual mean
    zm = ma.array(z, mask=z<bounds[0])

    # Set up the map
    m = lf.plot_map(pm='moll', reg=plot_reg_glob, ax=a)
    x, y = m(lon_land, lat_land)

    # Plot the scatter points

    h = m.scatter(x, y, s=4, c=zm, norm=norm, cmap=cmap, zorder=3)
    
    # Set subtitles
    a.set_title(t, fontsize=30)

  # Add one colorbar for all
  fg.subplots_adjust(left=0.05, right=0.85, bottom=0.05, top=0.95)
  cax = fg.add_axes([0.9, 0.25, 0.02, 0.5])
  cb = fg.colorbar(h, cax=cax, ticks=bounds, extend='both')
  cb.ax.tick_params(labelsize=20)
  cb.set_label(label=r'monoterpene emission [mgC m$^{-2}$ d$^{-1}$]', size=20)

  # Save the figure
  fg.savefig('{0:s}{1:s}.png'.format('./figures/', 'monoterpene_emission'), dpi=DPI)
