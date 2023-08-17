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

# =============================   Personal functions   ===============

class config_class:
    def __init__(self):
        """        """
        self.values = {}

    def add(self, key, values):
        """        """
        self.values[key] = values

    def get(self, key):
        """        """
        return self.values[key]


class Builder_config_class:
    def __init__(self):
        """        """

    def buildClass(self, lone_year = True, xaxis_limits = None):
        cfg = config_class()
        if lone_year:
            xlimits = [0.0, 400.0, 50.0]
        else:
            xlimits = xaxis_limits
        # Meta information for FLDS parameter:
        cfg.add('FLDS' , {
            'short_name':'FLDS',
            'long_name' : 'Downwelling longwave flux at surface',
            'units'     : 'W/m2',
            'xlimits'   : xlimits,
            'ylimits'   : [250.0, 330.1, 20.0]})
        # Meta information for FSDS parameter:
        cfg.add('FSDS', {
            'short_name': 'FSDS',
            'long_name' : 'Downwelling solar flux at surface',
            'units'     : 'W/m2',
            'xlimits'   : xlimits,
            'ylimits'   : [120.0, 200.1, 20.0]})
        # Meta information for FLDS parameter:
        cfg.add('FSDS', {
            'short_name': 'FSDS',
            'long_name' : 'Downwelling solar flux at surface',
            'units'     : 'W/m2',
            'xlimits'   : xlimits,
            'ylimits'   : [120.0, 200.1, 20.0]})
        # Meta information for PSL parameter:
        cfg.add('PSL', {
            'short_name': 'PSL',
            'long_name' : 'Sea level pressure',
            'units'     : 'Pa',
            'xlimits'   : xlimits,
            'ylimits'   : [95000.0, 102000.1, 1000.0]})
        # Meta information for QREFHT parameter:
        cfg.add('QREFHT', {
            'short_name': 'QREFHT',
            'long_name' : 'Reference height humidity',
            'units'     : 'kg/kg',
            'xlimits'   : xlimits,
            'ylimits'   : [0.005, 0.01, 0.001]})
        # Meta information for TOTPREC parameter:
        cfg.add('TOTPREC', {
            'short_name': 'TOTPREC',
            'long_name' : 'Total precipitations',
            'units'     : 'mm/s',
            'xlimits'   : xlimits,
            'ylimits'   : [0.0, 1e-4, 1e-5]})
        # Meta information for TOTPREC parameter:
        cfg.add('TREFHT', {
            'short_name': 'TREFHT',
            'long_name' : 'Reference height temperature',
            'units'     : 'K',
            'xlimits'   : xlimits,
            'ylimits'   : [260.0, 285.1, 5.0]})
        # Meta information for TOTPREC parameter:
        cfg.add('WIND', {
            'short_name': 'WIND',
            'long_name' : 'Wind speed',
            'units'     : 'm/s',
            'xlimits'   : xlimits,
            'ylimits'   : [0.0, 10.1, 1.0]})
        # Meta information for TOTPREC parameter:
        cfg.add('U', {
            'short_name': 'U',
            'long_name' : 'Zonal wind ',
            'units'     : 'm/s',
            'xlimits'   : xlimits,
            'ylimits'   : [0.0, 10.1, 5.0]})
        # Meta information for TOTPREC parameter:
        cfg.add('V', {
            'short_name': 'V',
            'long_name' : 'Meridional wind',
            'units'     : 'm/s',
            'xlimits'   : xlimits,
            'ylimits'   : [0.0, 10.1, 5.0]})
        return cfg

# =============================    End of module   =====================