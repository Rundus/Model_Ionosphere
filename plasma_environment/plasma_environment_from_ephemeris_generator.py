# --- generate_run ---
# TODO: update the iri2016 model with the latest space weather indicies
import spacepy.pycdf


def generate_IRI_profile_from_ephemeris():
    # import the relevant parameter
    from src.run_toggles import RunToggles
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

    # Check if this specific run has been made
    folder_path = f'{RunToggles.output_path}/{RunToggles.start_year}/{RunToggles.start_month}/{RunToggles.start_day}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # --- --- --- --- --- --
    # --- CREATE THE RUN ---
    # --- --- --- --- --- --

    # Form the altitude range
    alt_km_range_params = (RunToggles.alt_km_range_start, RunToggles.alt_km_range_end, RunToggles.alt_km_range_rez)
    N_alt_km_range = int( (RunToggles.alt_km_range_end - RunToggles.alt_km_range_start) / RunToggles.alt_km_range_rez) + 1
    alt_km_range = np.linspace(RunToggles.alt_km_range_start, RunToggles.alt_km_range_end, N_alt_km_range)

    # get the specific epoch/glat/glon range
    data_dict_ephemeris = stl.loadDictFromFile(RunToggles.path_to_ephemeris_data)
    low_idx = np.abs(data_dict_ephemeris[f'{RunToggles.ephemeris_time_key_name}'][0] - RunToggles.ephemeris_start_time).argmin()
    high_idx = np.abs(data_dict_ephemeris[f'{RunToggles.ephemeris_time_key_name}'][0] - RunToggles.ephermeris_stop_time).argmin()

    Epoch_range = data_dict_ephemeris[f'{RunToggles.ephemeris_time_key_name}'][0][low_idx:high_idx]
    glon_range = data_dict_ephemeris[f'{RunToggles.ephemeris_glon_key_name}'][0][low_idx:high_idx]
    glat_range = data_dict_ephemeris[f'{RunToggles.ephemeris_glat_key_name}'][0][low_idx:high_idx]

    # --- downsample the data ---

    # get the data's sample rate
    deltaT = (spacepy.pycdf.lib.datetime_to_tt2000(Epoch_range[1]) - spacepy.pycdf.lib.datetime_to_tt2000(Epoch_range[0]))/1E9
    num_points = round(RunToggles.ephemeris_time_resolution/deltaT)
    Epoch_range=Epoch_range[::num_points]
    glon_range = glon_range[::num_points]
    glat_range = glat_range[::num_points]

    # --- RUN THE IRI MODEL ---
    # prepare the output
    example_var = np.zeros(shape=(len(Epoch_range), int((RunToggles.alt_km_range_end - RunToggles.alt_km_range_start) / RunToggles.alt_km_range_rez) + 1))
    data_dict_output = {
        'alt_ephemeris':[np.array(Epoch_range), deepcopy(data_dict_ephemeris[f'{RunToggles.ephemeris_time_key_name}'][1])],
        'glon_ephemeris':[np.array(glon_range), deepcopy(data_dict_ephemeris[f'{RunToggles.ephemeris_glon_key_name}'][1])],
        'glat_ephemeris':[np.array(glat_range), deepcopy(data_dict_ephemeris[f'{RunToggles.ephemeris_glat_key_name}'][1])],
        'Epoch': [Epoch_range, {'DEPEND_0': 'Epoch'}],
        'alt': [alt_km_range, {'UNITS': 'km','LABLAXIS':'altitude'}],
        'ne': [deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'cm!A-3!N', 'VAR_TYPE':'data','LABLAXIS':'Plasma Density'}],
        'Te': [deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt', 'UNITS': 'K', 'VAR_TYPE':'data','LABLAXIS':'Electron Temp.'}],
        'Tn' : [deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'K', 'VAR_TYPE':'data','LABLAXIS':'Neutral Temp.'}],
        'Ti':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'K', 'VAR_TYPE':'data','LABLAXIS':'Ion Temp.'}],
        'nO+':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'m!A-3!N', 'VAR_TYPE':'data','LABLAXIS':'O+'}],
        'nH+':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'m!A-3!N', 'VAR_TYPE':'data','LABLAXIS':'H+'}],
        'nHe+':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'m!A-3!N', 'VAR_TYPE':'data','LABLAXIS':'He+'}],
        'nO2+':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'m!A-3!N', 'VAR_TYPE':'data','LABLAXIS':'O2+'}],
        'nNO+':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'m!A-3!N', 'VAR_TYPE':'data','LABLAXIS':'NO+'}],
        'nN+':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'m!A-3!N', 'VAR_TYPE':'data','LABLAXIS':'N+'}],
        'nCI': [deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt', 'UNITS': None, 'VAR_TYPE':'support_data'}],
        'NmF2':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'m!A-3!N', 'VAR_TYPE':'support_data'}],
        'hmF2':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'km'}],
        'NmF1':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'m!A-3!N'}],
        'hmF1':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'km'}],
        'NmE':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'m!A-3!N'}],
        'hmE':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'km'}],
        'TEC':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'m!A-3!N'}],
        'EqVertIonDrift':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':'m/s'}],
        'foF2':[deepcopy(example_var), {'DEPEND_0': 'Epoch', 'DEPEND_1': 'alt','UNITS':None}],
    }

    # calculate the IRI runs
    for tmeIdx in tqdm(range(len(Epoch_range))):

        # get the IRI input data
        epochVal = Epoch_range[tmeIdx]
        glonVal = glon_range[tmeIdx]-180
        glatVal = glat_range[tmeIdx]

        # --- Construct the relevant epoch range ---
        # Note: The iri2016 module only accepts time ranges <=2016, so we necessarily have to push back our time-window to then, but on the same day. We also
        # have to update the iri model input parameters to our given day e.g. F10.7cm index etc
        seconds_since_Jan1st_in_ephmeris_data = (spacepy.pycdf.lib.datetime_to_tt2000(epochVal) - spacepy.pycdf.lib.datetime_to_tt2000(dt.datetime(Epoch_range[0].year,1,1)))/1E9
        epochVal_2016 = dt.datetime(2016,1,1) + dt.timedelta(seconds=seconds_since_Jan1st_in_ephmeris_data)

        sim = iri.IRI(time=epochVal_2016,
                      altkmrange=alt_km_range_params,
                      glat=float(glatVal),
                      glon=float(glonVal))


        for key in sim.keys():
            data_dict_output[key][0][tmeIdx] = deepcopy(sim[key])


    # --- OUTPUT THE DATA ---

    stl.outputDataDict(
        outputPath=f'{folder_path}/IRI_{RunToggles.start_year}{RunToggles.start_month}{RunToggles.start_day}_to_{RunToggles.end_year}{RunToggles.end_month}{RunToggles.end_day}_profile.cdf',
        data_dict=data_dict_output)
