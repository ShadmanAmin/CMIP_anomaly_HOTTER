#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 16:51:28 2021

@author: gquetin


Convert temperature and dewpoint temperature [C] to VPD [hPa]


"""

import numpy as np



def vapor_pressure(T):
    
    '''
    Input:
        T - temperature in Celcius [C]
        
    Output:
        Saturation pressure in hectPascal [hPa]
        
    based on:
        https://www.weather.gov/epz/wxcalc_vaporpressure
        
    To calculate saturation vapor pressure, use temperature
    To calculate actual vapor pressure, use dewpoint temperature
    '''
    
    # calculate the vapor pressure
    e = 6.11*10**((7.5*T)/(237.7 + T))
    
    return e


def vpd_from_temperature_dewpoint(T,Td):
    
    '''
    Input:
        T - temperature in Celcius [C]
        Td - dewpoint temperature in Celccius [C]
        
    Output:
        vpd - vapor pressure deficit in hPa
        
    Larger numbers are for drier air
    
    '''
    # calculate the saturation vapor pressure
    es = vapor_pressure(T)
    
    # calculate the actual vapor pressure
    e = vapor_pressure(Td)
    
    
    vpd = es - e
    
    return vpd



def vpd_from_temperature_rh(T,Rh):
    
    '''
    Input:
        T - temperature in Celcius [C]
        RH - Relative Humidity [%]
        
    Output:
        vpd - vapor pressure deficit in hPa
        
    Larger numbers are for drier air
    
    '''
    # calculate the saturation vapor pressure
    es = vapor_pressure(T)
    
    # calculate the actual vapor pressure
    e = (Rh/100) * es
    
    
    vpd = es - e
    
    return vpd


#%%
if __name__ == '__main__':
    
    T = np.linspace(0,45,10)
    Td = T - 20
    
    vpd = vpd_from_temperature_dewpoint(T,Td)
    
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(1,1)
    ax.plot(T,vpd)
    ax.set_title('Simple Test')
    ax.set_xlabel('T [C]')
    ax.set_ylabel('VPD [hPa]')