
import numpy as np
import pandas as pd
import os
import sys
import copy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import configparser
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')
## Find the home directory
MACHDIR = os.path.expanduser("~")

## Path to the configuration file
fullpath_config = "/home/mdshadman_amin/dev/CMIP/hotter_config.ini"
def setup_directories(fullpath_config):
    
    #
    ## Load configuration from setup file
    config = configparser.ConfigParser()
    config.read(fullpath_config)
    
    base_directory = config['SETUP']['base_directory'].format(MACHDIR)
    output_directory = config['SETUP']['output_directory'].format(MACHDIR)
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory) 
    
    ## Set up paths to system scripts
    for folderin in ['model','support','demo','test','model/respiration']:

        sys.path.append(base_directory + folderin)
    
    return config, base_directory, output_directory
## Setup folders
config, base_directory, output_directory = setup_directories(fullpath_config)

## Print out the locations of folders
print('location of the primary scripts for the HOTTER model and HOTTER demo')
print(base_directory)
print('\n')

print('location for HOTTER demo outputs')
print(output_directory)
import hotter_main
import hotter_optimization

import helper_scripts

#
## Print HOTTERs document string
print(hotter_main.hotter_flux.__doc__)

