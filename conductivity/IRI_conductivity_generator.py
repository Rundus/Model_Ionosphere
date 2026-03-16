# --- generate IRI_conductivity ---
# Get the data from generate_IRI_profile(_from_ephemeris).py and
# calculate the ionospheric conductivity: height integrated or otherwise

#################
# --- IMPORTS ---
#################
from src.run_toggles import RunToggles
import os
import spaceToolsLib as stl

def generate_IRI_conductivity():



    # --- load the relevant IRI data ---
    # Check if this specific run has been made
    folder_path = f'{RunToggles.output_path}/{RunToggles.start_year}/{RunToggles.start_month}/{RunToggles.start_day}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    data_dict_profile = stl.loadDictFromFile(f'{folder_path}/IRI_{RunToggles.start_year}{RunToggles.start_month}{RunToggles.start_day}_to_{RunToggles.end_year}{RunToggles.end_month}{RunToggles.end_day}_profile.cdf')

    ####################################
    # --- calculate the conductivity ---
    ####################################


