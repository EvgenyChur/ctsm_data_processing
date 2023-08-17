# -*- coding: utf-8 -*-
"""
Description: Comparing input forcing data (GSWP3 and B1850)

data for GSWP3 simulation were prepared by script:
    /work/mj0143/b381275/inputdata/atm/datm7/atm_forcing.datm7.GSWP3.0.5d.v1.c170516/prep_forcing_gswp3.bash
  
dato for MODEL simulation were prepared by script:
    /work/mj0143/b381275/inputdata/atm/datm7/atm_forcing.datm7.MODEL/prep_forcing4comparison.bash


Authors: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    17.08.2023 Evgenii Churiulin, MPI-BGC
           Initial release
"""

# =============================     Import modules     =================
# 1.1: Standard modules
import os
import sys
import pandas as pd
import xarray as xr
import warnings
warnings.filterwarnings("ignore")

# 1.2 Personal module
sys.path.append(os.path.join(os.getcwd(), '..'))
import lib4visualization as l4v
import lib4sys_support as l4s
import config as cnf

sys_help = l4s.system_class()
# =============================   Personal functions   ================

def get_forcing_data(dvars:dict, **kwards):
    """ Get data for processing """
    global sys_help
    # -- Check input dataset list:
    if 'lst4ds' in kwards and len(kwards.get('lst4ds')) != 0:
        datasets_list = kwards.get('lst4ds') 
    else:
        sys.exit("Error: Either no research datasets are available, or an incorrect keyword has been used.")
    # -- Check input path:
    if 'pin_path' in kwards and len(kwards.get('pin_path')) != 0:
        pin = kwards.get('pin_path')
    else:
        sys.exit("Error: Either the input path is missing or an incorrect keyword has been used.")
    # -- Check input time limits:
    if 'tstart' in kwards and 'tstop' in kwards:
        t1 = kwards.get('tstart')
        t2 = kwards.get('tstop')
    else:
        sys.exit("Error: Either the tstart or tstop is missing or an incorrect keyword has been used.")
    # -- Check mask for GSWP3 forcing:
    if 'mask' in kwards and 'lgswp3_forc' in kwards and kwards.get('lgswp3_forc'):
        mask = kwards.get('mask')

    # -- Main part:
    datasets = []
    for ds_name in datasets_list:
        # -- Select special parameters for input data
        if 'lmodel_forc' in kwards and kwards.get('lmodel_forc'):
            path = f'{pin}/{ds_name}.{t1}_{t2}_fldmean.nc'
            freq_ts = '1D'

        if 'lgswp3_forc' in kwards and kwards.get('lgswp3_forc'):
            path = f'{pin}/{mask}.{ds_name}.{t1}_{t2}_fldmean.nc'
            freq_ts = '3H'

        # -- Create new time index without leap days:
        ts_index = pd.date_range(f'01-01-{t1}', f'01-01-{t2+1}', freq = freq_ts)[0:-1]
        leap = ts_index[(ts_index.day != 29) | (ts_index.month != 2)]
        # -- Open dataset:
        ds = xr.open_dataset(path)
        # -- Select data by parameters:
        lst4params = []
        for var in dvars.get(ds_name):
            if kwards.get('lmodel_forc'):
                ds_new = sys_help.convert_ctsm_time(ds)
            if kwards.get('lgswp3_forc'):
                ds_new = ds
            # Add data to list:
            lst4params.append(
                pd.Series(ds_new[var].data, index = leap, name = var))
        datasets.append(lst4params)
    return pd.concat([pd.concat(datasets[0], axis = 1),
                      pd.concat(datasets[1], axis = 1),
                      pd.concat(datasets[2], axis = 1)],axis = 1)


def plot_settings(var:str, path_exit:str,**kwards):
    # Get metainformation about parameters:
    cfg = cnf.Builder_config_class()
    param_settings = cfg.buildClass(
        lone_year = False, 
        xaxis_limits =  ['01.01.1850', '01.01.1931']
    )
    # -- local variables:
    sname = param_settings.get(var).get('short_name')
    lname = param_settings.get(var).get('long_name')
    units = param_settings.get(var).get('units')
    title =  f'Comparison input {sname} forcing data (GSWP3 and B1850)'
    xlabel = 'Years'
    ylable = f'{lname}, {units}'
    xlim  = param_settings.get(var).get('xlimits')
    ylim  = param_settings.get(var).get('ylimits')
    rotation = 0
    pout  = f'{path_exit}/{var}_forcing.png'
    # -- Create output dictionary:
    set4plot = {
        'ltitle' : title,
        'xlabel' : xlabel,
        'ylabel' : ylable,
        'xlim_time' : xlim,
        'x_rotation': rotation,
        'ylim_num' : ylim,
        'llegend' : True,
        'lgrid' : True,
        'output' : pout,
    }
    # -- Add extra settings:
    if 'labels' in kwards:
        set4plot['label'] = kwards['labels']
    if 'colors' in kwards:
        set4plot['color'] = kwards['colors']
    if 'linestyles' in kwards:
        set4plot['linestyle'] = kwards['linestyles']
    return set4plot

#================   User settings (have to be adapted)  =======================
# -- Local variables:
drive = 'C:'
main  = 'Users/evchur/Desktop/DATA/CLM_FORCING'
pout  = f'{drive}/Users/evchur/Python/scripts/github/ctsm_data_processing/RESULTS/CMP_FORCING_PLOTS' 
separator = '/'

# Parameters for GSWP3 forcing data:
sforcing1='GSWP3'
gt1 = 1901
gt2 = 1920
gds = ['Solr', 'Prec', 'TPQWL']
gvar = {
    'Solr' : ['FSDS'],
    'Prec' : ['PRECTmms'],
    'TPQWL' : ['FLDS', 'PSRF', 'QBOT', 'TBOT', 'WIND'],
}
fmask = f'clmforc.{sforcing1}.c2011.0.5x0.5'

# Parameters for B1850 forcing data:
sforcing2='MODEL'
mt1 = 1850
mt2 = 1880
mds  = ['FSDS', 'Prec', 'TPHW']
mvar = {
    'FSDS' : ['FSDS'],
    'Prec' : ['TOTPREC'],
    'TPHW' : ['FLDS','PSL','QREFHT','TREFHT','WIND'],
}

# -- Parameters for plot:
labels = [sforcing1, sforcing2] # legend
colors = ['black','red']        # Line colors
linestyles = ['-' , '-']        # Line styles

gvars = ['FSDS', 'PRECTmms', 'FLDS', 'PSRF', 'QBOT'  , 'TBOT'  , 'WIND']
mvars = ['FSDS', 'TOTPREC' , 'FLDS', 'PSL' , 'QREFHT', 'TREFHT', 'WIND']
#=============================    Main program   ============================== 
if __name__ == '__main__':
    # Create output folder:
    sys_help.mkfolder(pout)
    # Get input paths:
    pin_gswp3 = sys_help.os_path(drive, f'{main}/FORCING_{sforcing1}', sep = separator)
    pin_model = sys_help.os_path(drive, f'{main}/FORCING_{sforcing2}', 'FORCING', sep = separator)
    # Get GSWP3 forcing data:
    ds_gswp3 = get_forcing_data(
        gvar,
        lgswp3_forc = True,
        pin_path = pin_gswp3,
        lst4ds = gds,
        tstart = gt1,
        tstop = gt2,
        mask = fmask,
    )
    # Get MODEL data:
    ds_models = get_forcing_data(
        mvar,
        lmodel_forc = True,
        pin_path = pin_model,
        lst4ds = mds,
        tstart = mt1,
        tstop = mt2,
    )
    # -- Create comparison plots:
    for i, gparam in enumerate(gvars):
        # -- Get user settings for plot:
        uset_flds = plot_settings(
            mvars[i],
            pout,
            labels = labels,
            colors = colors,
            linestyles = linestyles,
        )
        # -- Prep data for plot:
        data = [ds_gswp3[gparam], ds_models[mvars[i]]]
        l4v.netcdf_line_plots(
            len(data), 
            data,
            uset_flds,
        )
#=============================    End of program   ============================ 
