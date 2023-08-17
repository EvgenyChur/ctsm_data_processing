# -*- coding: utf-8 -*-
"""
Description: The module is equipped with preliminary details pertaining to the
input forcing parameters. This foundational information serves as a basis for
further analysis and computations within the system.

Authors: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    16.08.2023 Evgenii Churiulin, MPI-BGC
           Initial release
"""

# =============================     Import modules     ================
# 1.1: Standard modules
import os
import sys
import pandas as pd
import xarray as xr
import cf_xarray # use cf-xarray so that we can use CF attributes
# =============================   Personal functions   ===============

class system_class:
    def __init__(self):
        self.act_user = 'evchur'


    def dep_clean(self, path:str):
        """ Remote previous results from folder"""
        for file in os.listdir(path):
            os.remove(path + file)


    def mkfolder(self, path:str):
        """ Create folder """
        try:
            os.makedirs(path)
        except FileExistsError:
            pass


    def os_path(self, disk, *args, sep = '//', **kwargs):
        """ Get path to the folder"""
        args = (disk, ) + args
        path = sep.join(args)
        return path

    # 3. Function --> get_info
    def get_info(self, df:pd.DataFrame, df_name:str):
        """ Get common information about datasets:"""
        print(f'Common information about - {df_name}')
        df.info()
        print(df.columns, '\n')
        print(f'Numbers of NaN values in the dataset - {df_name}', '\n')
        print(df.isnull().sum())
        print(f'Numbers of duplicates (explicit)in the dataset - {df_name}', '\n')


    def convert_ctsm_time(self, ds_prep:xr.Dataset):
        """Correct CTSM time axis based on CTSM time_bnds attributes:"""
        # -- Convert CESM monthly output data to correct time steps:
        attrs, encoding = ds_prep.time.attrs.copy(), ds_prep.time.encoding.copy()
        time_bounds = ds_prep.cf.get_bounds('time')
        time_bounds_dim_name = ds_prep.cf.get_bounds_dim_name('time')
        ds_prep = ds_prep.assign_coords(time=time_bounds.mean(time_bounds_dim_name))
        ds_prep.time.attrs, ds_prep.time.encoding = attrs, encoding
        return ds_prep

# =============================    End of module   =====================
