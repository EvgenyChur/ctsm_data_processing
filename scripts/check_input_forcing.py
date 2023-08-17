# -*- coding: utf-8 -*-
"""
Description: A script has been created to oversee the management of input
forcing data, which is computed using information obtained from the
B1850 model run.

    1. FLDS    --> Downwelling longwave flux at surface --> W/m2
    2. FSDS    --> Downwelling solar flux at surface    --> W/m2
    3. PSL     --> Sea level pressure                   --> Pa
    4. QREFHT  --> Reference height humidity            --> kg/kg
    5. TOTPREC --> Total precipitations                 --> mm
    6. TREFHT  --> Reference height temperature         --> K
    7. U       --> Zonal wind                           --> m/s
    8. V       --> Meridional wind                      --> m/s

Authors: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    14.08.2023 Evgenii Churiulin, MPI-BGC
           Initial release
"""

# =============================     Import modules     ===================
# 1.1: Standard modules
import os
import sys
import numpy as np
import pandas as pd
import xarray as xr
import warnings
warnings.filterwarnings("ignore")
# 1.2 Personal modules:
sys.path.append(os.path.join(os.getcwd(), '..'))
import lib4visualization as l4p
import lib4sys_support as l4s
import config as cnf

# --------------------------- Personal functions --------------------------

def get_data4param(paths:list[str], var:str):
    """Get intup data from datasets"""
    global tsets

    #-- local variables:
    pa2hpa = 1    # convert Pa to hPa --> use this values pa2hpa = 1e-2
    ms2mms = 1e3  # convert m/s to mm/s
    
    lst4data = []
    lst4years = []
    # - Get actual data for years -> main data for visualization:
    for path in paths:
        ds = xr.open_dataset(path)[var]
        # -- Select algorithm for data processing:
        if var in ('FLDS', 'FSDS', 'QREFHT', 'TREFHT'):
            ts_params = ds.mean(dim = {'lat', 'lon'})
        elif var in ('PSL'):
            ts_params = (ds*pa2hpa).mean(dim = {'lat', 'lon'})
        elif var in ('TOTPREC'):
            #ts_params = (ds*ms2mms).sum(dim = {'lat', 'lon'})
            ts_params = (ds*ms2mms).mean(dim = {'lat', 'lon'})
        lst4data.append(pd.Series(ts_params.values))
    # -- Get actual legend labels:
    for year in np.arange(
            tsets.get('frs_yr'), tsets.get('lst_yr'), tsets.get('step')):
        lst4years.append(f'{year}')
    return lst4data, lst4years


def plot_settings(var:str, path_exit:str,**kwards):
    """ Create dictionary with user settings for plots"""
    global tsets
    # Get metainformation about parameters:
    cfg = cnf.Builder_config_class()
    param_settings = cfg.buildClass()
    # -- local variables:
    t1 = tsets.get('frs_yr')
    t2 = tsets.get('lst_yr')
    sname = param_settings.get(var).get('short_name')
    lname = param_settings.get(var).get('long_name')
    units = param_settings.get(var).get('units')
    title =  f'Raw forcing data - {sname} from {t1} to {t2-1} yr'
    xlabel = 'Calendar day'
    ylable = f'{lname}, {units}'
    xlim  = param_settings.get(var).get('xlimits')
    ylim  = param_settings.get(var).get('ylimits')
    rotation = 0
    pout = f'{path_exit}/{var}_{t1}_{t2}.png'
    # -- Create output dictionary:
    set4plot = {
        'ltitle' : title,
        'xlabel' : xlabel,
        'ylabel' : ylable,
        'xlim_num' : xlim,
        'x_rotation': rotation,
        'ylim_num' : ylim,
        'llegend' : True,
        'lgrid' : True,
        'output' : pout,
        }
    # -- Add new elements to output dictionary:
    if 'labels' in kwards:
        set4plot['label'] = kwards['labels']
    if 'colors' in kwards:
        set4plot['color'] = kwards['colors']
    if 'linestyles' in kwards:
        set4plot['linestyle'] = kwards['linestyles']
    return set4plot


def fast_test(ds_list:list[pd.Series], var:str):
    """Fast quality test"""
    for i in range(len(ds_list)):
        if ds_list[i].isnull().sum() != 0:
            print(f'These is a gap in timeseries with index {i} for {var} parmater')
            sys.exit('Error in fast_test function')


# ---------------------------- User settings ----------------------------------
# -- Local variables:
drive = 'C:'
main = 'Users/evchur/Desktop/DATA/CLM_FORCING/RAW_DATA'
pout = f'{drive}/Users/evchur/Python/scripts/github/ctsm_data_processing/RESULTS/CHECK_INT_FORS'
separator = '/'


# -- Time intervals:
timesteps = [1850, 1860]#, 1870, 1880]
# Line colors:
colors = ['black'    , 'grey'  , 'silver', 'brown', 'red'   ,
          'chocolate', 'orange', 'green' , 'blue' , 'purple']
# Line styles:
linestyles = ['-' , '-' , '-' , ':' , ':' ,
              ':' , '-.', '-.', '-.', '--']
# -- List of research parameters from B1850 dataset:
lst4params = ['FLDS', 'FSDS', 'PSL', 'QREFHT', 'TOTPREC', 'TREFHT']
#lst4params = ['TOTPREC']

# --------------------------- Main program ------------------------------------
if __name__ == '__main__':
    sys_help = l4s.system_class()
    # Create output folder:
    sys_help.mkfolder(pout)    
    # -- Cycle over parameter:
    for param in lst4params:
        # -- Cycle over time steps:
        for i,tstep in enumerate(timesteps):
            # -- Set correct time intervals:
            if i+1 < len(timesteps):
                tsets = {'frs_yr':timesteps[i], 'lst_yr':timesteps[i+1], 'step': 1}
            # -- Get input common path:
            path = sys_help.os_path(drive, main, sep = separator)
            # -- Get uniq data paths for each year:
            paths4years = [
                f'{path}/{year}.nc' for year in np.arange(
                    tsets.get('frs_yr'), tsets.get('lst_yr'), tsets.get('step')
                )
            ]
            # -- Get daily data:
            ds_param, legends = get_data4param(paths4years, param)
            # -- Run fast quality test for daily data:
            fast_test(ds_param, param)
            # -- Get dictionary with user settings for plot:
            uset_plot = plot_settings(
                param,
                pout,
                labels = legends,
                colors = colors,
                linestyles = linestyles)
            # -- Create plot:
            plot = l4p.netcdf_line_plots(
                len(ds_param),
                ds_param,
                uset_plot,
            )
