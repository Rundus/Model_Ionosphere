# --- generate_run ---
# TODO: update the iri2016 model with the latest space weather indicies


def generate_IRI_profile_from_ephemeris():
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

    # --- load the data ---
    data_dict_spatial = stl.loadDictFromFile(f'{UserToggles.run_folder_path}/spatial_environment.cdf')
    Epoch_range = data_dict_spatial['Epoch_model'][0]
    glon_range = data_dict_spatial['glons_model'][0]
    glat_range = data_dict_spatial['glats_model'][0]
    alts_range = data_dict_spatial['alts_model'][0]

    # --- --- --- --- --- --
    # --- CREATE THE RUN ---
    # --- --- --- --- --- --

    # --- RUN THE IRI MODEL ---
    # prepare the output
    example_var = np.zeros(shape=(len(Epoch_range), len(alts_range)))
    data_dict_output = {
        'Epoch': deepcopy(data_dict_spatial['Epoch_model']),
        'alt': deepcopy(data_dict_spatial['alts_model']),
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
        seconds_since_Jan1st_in_ephmeris_data = (pycdf.lib.datetime_to_tt2000(epochVal) - pycdf.lib.datetime_to_tt2000(dt.datetime(Epoch_range[0].year,1,1)))/1E9
        epochVal_2016 = dt.datetime(2016,1,1) + dt.timedelta(seconds=seconds_since_Jan1st_in_ephmeris_data)

        sim = iri.IRI(time=epochVal_2016,
                      altkmrange=(UserToggles.alt_km_range_start,UserToggles.alt_km_range_end,UserToggles.alt_km_range_rez),
                      glat=float(glatVal),
                      glon=float(glonVal))

        for key in sim.keys():
            data_dict_output[key][0][tmeIdx] = deepcopy(sim[key])

    # --- OUTPUT THE DATA ---
    stl.outputDataDict(
        outputPath=f'{UserToggles.run_folder_path}/plasma_environment_IRI.cdf',
        data_dict=data_dict_output)
