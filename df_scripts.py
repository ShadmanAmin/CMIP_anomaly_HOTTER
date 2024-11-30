import os
import sys
import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
import glob



def met_to_vpd(air_temp, rh):
    vpd = (0.611 * np.exp((17.27 * air_temp) / (air_temp + 237.3)) * (1 - rh / 100))
    return vpd

def process_directory_for_hotter_metprep(directory, rh_dataframe):
    processed_data = {}

    # Use glob to find all files matching the pattern for met files
    met_files = glob.glob(os.path.join(directory, '*_met_df.csv'))

    for base_file_path in met_files:
        # Extract the location from the file name
        location = base_file_path.split('_')[3]
        
        # Read the base met data (2000-2014)
        base_met_df = pd.read_csv(base_file_path)
        base_met_df['D'] = base_met_df['D'] * 100
        base_met_df['time'] = pd.to_datetime(base_met_df['time'])
        base_met_df = base_met_df.resample('M', on='time').mean()
        base_met_df = base_met_df.reset_index()
        base_met_df['time'] = base_met_df['time'].dt.strftime('%Y-%m')
        
        # Find the corresponding anomaly file
        anomaly_file_pattern = location + '_anomaly_df.csv'
        anomaly_file_path = os.path.join(directory, anomaly_file_pattern)

        if os.path.exists(anomaly_file_path):
            # Read the anomaly data
            anomaly_df = pd.read_csv(anomaly_file_path)
            anomaly_df['time'] = pd.to_datetime(anomaly_df[['year', 'month']].assign(day=1), errors='coerce')
            anomaly_df = anomaly_df.drop(columns=['year', 'month'])
            anomaly_df['time'] = anomaly_df['time'].dt.strftime('%Y-%m')
            anomaly_df = anomaly_df[(anomaly_df['time'] > '2085-12-30') & (anomaly_df['time'] <= '2100-12-30')]
            
            # Merge base met data with the anomaly data on 'time'
            merged_df = pd.merge(base_met_df, anomaly_df, on='time', how='outer')

            # Extract the relevant series from base_met_df
            tair_series = base_met_df['tair'].to_list()
            psis_series = base_met_df['psis']
            ca_series = base_met_df['Ca']
            al_series = base_met_df['al']
            time_series = base_met_df['time']

            # Model and scenario lists
            model_list = ['CanESM5', 'E3SM-1-1', 'NorESM2-MM']
            scenario_list = ['ssp245', 'ssp585']
            specific_data = {}

            # Loop through each model and scenario combination
            for model in model_list:
                for scenario in scenario_list:
                    # Filter the dataframe based on the model and scenario
                    filtered_data = merged_df[(merged_df['model'] == model) & (merged_df['scenario'] == scenario)].copy()
                    filtered_data.reset_index(drop=True, inplace=True)
                    new_df = pd.DataFrame()
                    new_df['model'] = filtered_data['model']
                    new_df['scenario'] = filtered_data['scenario']
                    new_df['time'] = time_series.values
                    future_tair = []
                    for i in range(len(filtered_data)):
                        future_tair.append(tair_series[i] + filtered_data.iloc[i]['tas_anomaly'])
                    new_df['future_tair'] = pd.Series(future_tair)
                    new_df['psis'] = psis_series.values
                    new_df['Ca'] = ca_series.values
                    new_df['al'] = al_series.values

                    # Store the new dataframe in the dictionary with a key as (model, scenario)
                    specific_data[(model, scenario)] = new_df

            # Select the appropriate RH column based on the location
            rh_column = f"{location}_rh"
            if rh_column in rh_dataframe.columns:
                for (model, scenario), data in specific_data.items():
                    # Merge RH data and calculate VPD
                    rh_merger = pd.merge(data, rh_dataframe[['time', rh_column]], on='time', how='left')
                    rh_merger['D'] = met_to_vpd(rh_merger['future_tair'], rh_merger[rh_column])
                    specific_data[(model, scenario)]['D'] = rh_merger['D'] * 100
            else:
                print(f"Warning: RH data for {location} not found in rh_dataframe")

            # Store processed data
            for (model, scenario), data in specific_data.items():
                processed_data[(location, model, scenario)] = data

    return processed_data



