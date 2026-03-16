# --- spatial_environment_generator ---


def spatial_environment_generator():

    # import the relevant parameter
    from src.user_inputs.user_toggles import UserToggles
    from spacepy import pycdf
    import os
    import datetime as dt
    import iri2016.profile as iri
    import spaceToolsLib as stl
    from copy import deepcopy
    import numpy as np
    from tqdm import tqdm
    import warnings
    import itertools
    warnings.filterwarnings("ignore")

    # --- --- --- --- --- --
    # --- CREATE THE RUN ---
    # --- --- --- --- --- --

    # Form the altitude range
    alt_km_range_params = (UserToggles.alt_km_range_start, UserToggles.alt_km_range_end, UserToggles.alt_km_range_rez)
    N_alt_km_range = int( (UserToggles.alt_km_range_end - UserToggles.alt_km_range_start) / UserToggles.alt_km_range_rez) + 1
    alt_km_range = np.linspace(UserToggles.alt_km_range_start, UserToggles.alt_km_range_end, N_alt_km_range)

    # get the specific epoch/glat/glon range
    data_dict_ephemeris = stl.loadDictFromFile(UserToggles.path_to_ephemeris_data)
    low_idx = np.abs(data_dict_ephemeris[f'{UserToggles.ephemeris_time_key_name}'][0] - UserToggles.ephemeris_start_time).argmin()
    high_idx = np.abs(data_dict_ephemeris[f'{UserToggles.ephemeris_time_key_name}'][0] - UserToggles.ephermeris_stop_time).argmin()

    Epoch_range = data_dict_ephemeris[f'{UserToggles.ephemeris_time_key_name}'][0][low_idx:high_idx]
    glon_range = data_dict_ephemeris[f'{UserToggles.ephemeris_glon_key_name}'][0][low_idx:high_idx]
    glat_range = data_dict_ephemeris[f'{UserToggles.ephemeris_glat_key_name}'][0][low_idx:high_idx]

    # --- downsample the data ---

    # get the data's sample rate
    deltaT = (pycdf.lib.datetime_to_tt2000(Epoch_range[1]) - pycdf.lib.datetime_to_tt2000(Epoch_range[0]))/1E9
    num_points = round(UserToggles.ephemeris_time_resolution/deltaT)
    Epoch_range=Epoch_range[::num_points]
    glon_range = glon_range[::num_points]
    glat_range = glat_range[::num_points]

    # --- RUN THE IRI MODEL ---
    # prepare the output
    example_var = np.zeros(shape=(len(Epoch_range), int((UserToggles.alt_km_range_end - UserToggles.alt_km_range_start) / UserToggles.alt_km_range_rez) + 1))
    data_dict_output = {
        'alt_ephemeris':[np.array(Epoch_range), deepcopy(data_dict_ephemeris[f'{UserToggles.ephemeris_time_key_name}'][1])],
        'glon_ephemeris':[np.array(glon_range), deepcopy(data_dict_ephemeris[f'{UserToggles.ephemeris_glon_key_name}'][1])],
        'glat_ephemeris':[np.array(glat_range), deepcopy(data_dict_ephemeris[f'{UserToggles.ephemeris_glat_key_name}'][1])],
        'Epoch': [Epoch_range, {'DEPEND_0': 'Epoch'}],
        'alt': [alt_km_range, {'UNITS': 'km','LABLAXIS':'altitude'}],
    }

    # --- OUTPUT THE DATA ---
    stl.outputDataDict(
        outputPath=f'{UserToggles.run_folder_path}/spatial_environment',
        data_dict=data_dict_output)
