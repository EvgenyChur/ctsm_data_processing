# -*- coding: utf-8 -*-
"""
Description: Module for visualization of ICON data

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    07.03.2023 Evgenii Churiulin, MPI-BGC
           Initial release
"""

# =============================     Import modules     =======================
import time
import numpy as np
import pandas            as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import colors
import xarray as xr
import warnings
warnings.filterwarnings("ignore")
from typing import Optional

import matplotlib.dates as mdates
days = mdates.DayLocator(5)

# =============================   Personal functions   ======================

# Function --> tick_rotation_size
def xticks_settings(ax:plt.Axes, rotation:float, fsize:int):
    """Additional settings for x ticks labels"""
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(rotation)
        label.set_fontsize(fsize)


def yticks_settings(ax:plt.Axes, rotation:float, fsize:int):
    """Additional settings for y ticks labels"""
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(fsize)


class Plot_settings:
    def __init__(self):
        # Set common parameters for all figures:
        self.title = 'title'    # Common plot title
        self.clr   = 'black'  # Color of labels
        self.fsize = 14       # Size of labels
        self.pad   = 20       # Space betveen axis and label
        self.l_pos = 'upper left'  # Legend location
        self.gtype = 'major'  # Which axis do you want to use for grid (major or)
        self.gclr  = 'grey'   # Grid color
        self.gstyle= 'dashed' # Grid line style
        self.galpha= 0.2      # Grid transparacy
        self.txaxis_format = '%Y'
        self.plt_format = 'png'
        self.plt_dpi = 300

    def plt_uniq_settings(self, ax, uset):
        """ User settings for plot"""
        # -- Set plot title:
        if 'ltitle' in uset and len(uset.get('ltitle')) > 0:
            ax.set_title(
                uset.get('ltitle'),
                color = self.clr,
                fontsize = self.fsize,
                pad = self.pad,
            )
        # -- Set x axis label:
        if 'xlabel' in uset:
            ax.set_xlabel(
                uset.get('xlabel'),
                color = self.clr,
                fontsize = self.fsize,
                labelpad = self.pad,
            )
        # -- Set y axis label:
        if 'ylabel' in uset:
            ax.set_ylabel(
                uset.get('ylabel'),
                color = self.clr,
                fontsize = self.fsize,
                labelpad = self.pad,
            )
        # -- Set X axis ticks paramters for numbers:
        if 'xlim_num' in uset and len(uset.get('xlim_num')) > 0:
            ax.set_xticks(
                np.arange(
                    uset.get('xlim_num')[0],
                    uset.get('xlim_num')[1],
                    uset.get('xlim_num')[2],
                )
            )
                # -- Set X axis ticks parameters for time axis:
        if 'xlim_time' in uset and len(uset.get('xlim_time')) > 0:
            ax.set_xlim(
                pd.to_datetime(uset.get('xlim_time')[0], format='%d.%m.%Y'),
                pd.to_datetime(uset.get('xlim_time')[1], format='%d.%m.%Y'),
            )
            xftm = mdates.DateFormatter(self.txaxis_format)
            ax.xaxis.set_major_formatter(xftm)
            ax.xaxis.set_minor_locator(days)
        #-- Extra parameters for ticks: (ax, rotation, size)
        if 'x_rotation' in uset:
            xticks_settings(ax, uset.get('x_rotation'), self.fsize)
        # -- Set Y axis ticks parameters:
        if 'ylim_num' in uset and len(uset.get('ylim_num')) > 0:
            ax.set_yticks(
                np.arange(
                    uset.get('ylim_num')[0],
                    uset.get('ylim_num')[1],
                    uset.get('ylim_num')[2],
                )
            )
        #-- Extra parameters for ticks: (ax, rotation, size)
        if 'y_rotation' in uset:
            yticks_settings(ax, uset.get('y_rotation'), self.fsize)
        # -- Add legend:
        if 'llegend' in uset and uset.get('llegend'):
            ax.legend(loc = self.l_pos)
        # -- Add grid settings:
        if 'lgrid' in uset and uset.get('lgrid'):
            ax.grid(
                uset.get('lgrid'),
                which = self.gtype,
                color = self.gclr,
                linestyle = self.gstyle,
                alpha = self.galpha,
            )
        # -- Set output parameters:
        if 'output' in uset and len(uset.get('output')) > 0:
            #-- Plot save
            plt.savefig(
                uset.get('output'),
                format = self.plt_format,
                dpi = self.plt_dpi,
            )
        else:
            plt.show()


# Function --> get_line_plot 
def get_line_plot(data, years, set4plot, set4ds):
    '''
    Task: Create line plot for research parameter

    Parameters
    ----------
    data : list, array
        Data for visualization
    years : Array
        Time axis
    set4plot : dict
        Plot settings
    set4ds : dict
        Dataset settings

    Returns
    -------
    Create and save output figure
    '''
    #-- Create plot    
    fig = plt.figure(figsize = (12,7))
    ax  = fig.add_subplot(111)

    for i in range(len(data)):
        ax.plot(
            years,
            data[i],
            label     = legends[i],
            color     = colors[i] ,
            linestyle = ln_style[i],
        )

    #-- Clean memory
    plt.close(fig)
    plt.gcf().clear()



def line_plot(data, set4plot, var):

    fig = plt.figure(figsize = (12,7))
    ax  = fig.add_subplot(111)
    for i in range(len(data)):
        ax.plot(data[i].index, data[i][var[i]]  ,
                label     = legends[i]  ,
                color     =  colors[i]  ,
                linestyle =  ln_style[i])
    #-- Clean memory
    plt.close(fig)
    plt.gcf().clear()

    return ax

# 2. netcdf_line_plots --> Visualization of the data from NetCDF files after xarray
#                          post-processing. In this function you can choose the
#                          actual number of lines for visualization.
#
#                          Data should be in one point (or for all grid accumulated
#                          to one point)
def netcdf_line_plots(
        # Input variables:
        lines_count:int,                       # Number of lines for visualization
        data:list[xr.DataArray],               # Data for visualization
        uset:dict,                             # user settings for plot
        mode: Optional[str] = 'Series',        # type of input data (xarray or series)
        # OUTPUT variables:
    ):                                         # Create new figure in output folder
    plt_parameters = Plot_settings()
    # -- Create figure:
    fig = plt.figure(figsize = (12,7))
    ax = fig.add_subplot(111)
    # -- Add data to figure:
    for i in range(lines_count):
        index = data[i].year if mode == 'xarray' else data[i].index

        ax.plot(
            index,
            data[i].values,
            label = uset['label'][i],
            color = uset['color'][i],
            linestyle = uset['linestyle'][i],
        )
    # Set plot parameters:
    plt_parameters.plt_uniq_settings(ax, uset)

    return ax

