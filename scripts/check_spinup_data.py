# -*- coding: utf-8 -*-
"""
Description: Post-processing of CTSM spinup data

Authors: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    14.08.23 Evgenii Churiulin, MPI-BGC
           Initial release
"""

# =============================     Import modules     ================
# 1.1: Standard modules:
import os
import sys
import numpy as np
import pandas as pd
import xarray as xr
import cf_xarray # use cf-xarray so that we can use CF attributes

import warnings
warnings.filterwarnings("ignore")
# 1.2: Personal modules:
sys.path.append(os.path.join(os.getcwd(), '..'))
import lib4visualization as l4v
import lib4sys_support as l4s


sys_help = l4s.system_class()
# ----------------------------- Personal functions ----------------------------

class CTSM_control:
    def __init__(self, drive:str, mpath:str, sep:str):
        self.drive = drive  # drive
        self.mpath = mpath  # main path
        self.sep = sep      # separator for folders


    def create_input_path(self, subpath:str, ctsm_version:str, ssets:dict, tsets:dict):
        """Get actual paths for input data:
            1. subpath -> subfolder;
            2. ctsm_version -> version of CTSM simulation;
            3. ssets -> simulation settings;
            4. tsets -> time settings"""
        global sys_help
        # Local variables:
        tlim = 9
        ctsm_prefix = ssets.get(ctsm_version) # version of CTSM simulation
        ctsm_group  = ssets.get('group')      # data group (h0, h1 ... hn)
        # -- Create main input path for actual subfolder with data:
        pin = sys_help.os_path(
            self.drive,
            self.mpath,
            subpath,
            sep = self.sep,
        )
        # -- Create input paths according to CTSM simulation years:
        paths4years = [
            f'{pin}/spinup_BGI{ctsm_prefix}.clm2.{ctsm_group}.000{year}' if year <= tlim else
            f'{pin}/spinup_BGI{ctsm_prefix}.clm2.{ctsm_group}.00{year}'
            for year in np.arange(
                tsets.get('first_year'),
                tsets.get('last_year'),
                tsets.get('step_year'),
            )
        ]
        # -- Add to actual paths correct months:
        paths4months = [
            f'{paths4years[index]}-0{mon}.nc' if mon <= tlim else
            f'{paths4years[index]}-{mon}.nc'
            for index in range(len(paths4years))
            for mon in np.arange(
                tsets.get('first_mon'), 
                tsets.get('last_mon'),
                tsets.get('step_mon'),
            )
        ]
        return paths4months


    def merge_data(self, paths:list[str], param:str):
        '''
        paths -> input paths with monthly data
        param -> research parameter
        '''
        global sys_help
        # -- Local variables:
        var_area = 'area'
        # -- Get monthly data:
        lst4spinup = []
        for i,path in enumerate(paths):
            try:
                # -- Open dataset:
                ds = xr.open_dataset(path)
                # -- Correct time axis and area:
                ds_cor = sys_help.convert_ctsm_time(ds)
                # -- Select research variable:
                lst4spinup.append(ds_cor[[param, var_area]])
            except:
                print(f'no data: {path}')

        # -- Time merge:
        ds_param = xr.concat(lst4spinup, dim = 'time')
        #print(ds_param.time)
        return ds_param


class CTSM_converter:
    def __init__(self):
        # -- Convert units:
        self.sec_in_hour = 3600.0      # number of seconds in hour
        self.hour_in_day = 24.0        # number of hours in day
        self.g_in_kg = 1000.0          # gramms in 1 kg
        self.rec_coef = 1e-9           # m2 to 1000 km2
        self.kgc2pgc = 1e-12           # kgC --> PgC
        self.gc2pgc = 1e-15            #  gC --> PgC
        self.km22m2 = 1e6              # m2 in 1km2


    def gpp_converter(self, ds:xr.Dataset, param:str):
        """Convertation algorithm for GPP"""
        # Get area 
        area = ds['area'][0]
        # -- Convert GPP units for MAP from gC m-2 s-1 --> gC m-2 yr-1')
        map_param = (
            (ds[param] * self.sec_in_hour * self.hour_in_day * ds.time.dt.days_in_month)
            .resample(time = 'A').sum('time')
        )
        # -- Convert GPP units for TS from gC m-2 yr-1 --> PgC yr-1'
        ts_param = ((map_param * self.gc2pgc * area * self.km22m2)
               .sum(dim = {'lat', 'lon'})
               .groupby('time.year').sum()
        )
        return map_param, ts_param


    def lai_converter(self, ds:xr.Dataset, param:str):
        """Convertation algorithm for LAI"""
        # Get area 
        area = ds['area'][0]
        # LAI map -> 
        map_param = ds[param].resample(time = 'A').sum('time')
        # LAI ts
        # Get time series:
        tmp = map_param * area
        tmp = tmp / area.sum(dim = {'lat', 'lon'})
        ts_lai = tmp.sum(dim = {'lat', 'lon'}).groupby('time.year').mean()
        return map_param, ts_lai


# -------------------- USER SETTINGS ------------------------------------------
# Local variables
disk = 'C:'
main  = 'Users/evchur/Desktop/DATA/CTSM'
pout  = 'C:/Users/evchur/Python/scripts/github/ctsm_data_processing/RESULTS/SPINUP'
separator = '/'

# -- Select input simulations:
#ctsm_exp = ['SPINUP_020', 'SPINUP_200', 'SPINUP_900', 'spinup_BGI_GSWP3_002' ]
#ctsm_pref = ['sim1', 'sim2', 'sim3', 'sim4']

ctsm_exp = ['spinup_BGI_005', 'spinup_BGI_GSWP3_002' ]
ctsm_pref = ['sim3', 'sim4']

#ctsm_exp = ['spinup_BGI_005']
#ctsm_pref = ['sim3']

# -- Time settings:
tsets = {
    'first_year' : 1,
    'last_year'  : 27,#12,
    'step_year'  : 1,
    'first_mon'  : 1,
    'last_mon'   : 13,
    'step_mon'   : 1,
}

# -- Simulation settings:
ssets = {
    'sim1'  : '_020',
    'sim2'  : '_200',
    'sim3'  : '_005', 
    'sim4'  : '_GSWP3_002',
    'group' : 'h0',
}

# -- Define parameters for plots (legend, line color and line style):
#leg = ['s20', 's200', 's900', 'gswp'], 
#col = ['r'  , 'b'  , 'g'   , 'black'],
#ln  = ['-', '-.','-', '-'],

leg = ['myForcing' ,'gswp']
col = ['g'   , 'black']
ln =  ['-', '-']

# -- User settings for GPP plot:
set4gpp_plot = {
    'label' : leg,
    'color' : col, 
    'linestyle': ln,
    'ltitle'   : 'GPP SPINUP',
    'xlabel': 'SPINUP years',
    'ylabel': 'GPP, PgC yr -1',
    'xlim_num': [0, 30, 1],
    'x_rotation': 0,
    'ylim_num': [0, 150, 10],
    'llegend' : True,
    'lgrid'   : True,
    'output': f'{pout}/GPP_30yr.png',
}
# -- User settings for LAI plot:
set4lai_plot = {
    'label'    : leg, 
    'color'    : col,
    'linestyle': ln,
    'ltitle' : 'LAI SPINUP',
    'xlabel': 'SPINUP years',
    'ylabel': 'LAI, m2 m-2',
    'xlim_num': [0, 30, 1],
    'x_rotation': 0,
    'ylim_num': [0, 20, 2],
    'llegend' : True,
    'lgrid'   : True,
    'output': f'{pout}/LAI_30yr.png',
}
# -- Research parameters
lst4params = ['GPP', 'TLAI']
#act_param = 'GPP'
# ----------------------------- Start program ---------------------------------
if __name__ == '__main__':
    sys_help.mkfolder(pout)
    ctsm = CTSM_control(disk, main, separator)
    units_converter = CTSM_converter()
    for act_param in lst4params:
        # Main data computations:
        lst4maps = []
        lst4ts = []
        for i,ver in enumerate(ctsm_exp):
            # Get data for different simulations:
            sp = ctsm.create_input_path(f'{ver}/lnd/hist', ctsm_pref[i], ssets, tsets)
            # Get data for parameter:
            ds4param = ctsm.merge_data(sp, act_param)
            # Convert units and get 2d map and timeseries:
            if act_param == 'GPP':
                m_param, ts_param = units_converter.gpp_converter(ds4param, act_param)
            elif act_param == 'TLAI':
                m_param, ts_param = units_converter.lai_converter(ds4param, act_param)
            else:
                print('Use original units')
            # Create lists with data:
            lst4maps.append(m_param)
            #lst4ts.append(pd.Series(ts_param.values))
            ts_test = ts_param.values
            ts_test = np.insert(ts_test, 0, 0., axis=0)
            lst4ts.append(pd.Series(ts_test))
        # Main visualization:
        if act_param == 'GPP':
            user_settings = set4gpp_plot
        elif act_param == 'TLAI':
            user_settings = set4lai_plot
        plots = l4v.netcdf_line_plots(
            len(lst4ts),
            lst4ts,
            user_settings,
        )
        # -- Reserv option for xarray plots:
        #plots = l4v.netcdf_line_plots(
        #    len(lst4ts),
        #    lst4ts,
        #    user_settings,
        #    mode = 'xarray',
        #)
