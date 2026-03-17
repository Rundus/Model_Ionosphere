def geomagnetic_field_generator():
    # --- common imports ---
    import spaceToolsLib as stl
    import numpy as np
    from tqdm import tqdm
    from glob import glob
    from copy import deepcopy
    from src.user_inputs.user_toggles import UserToggles
    from spacepy import pycdf
    import datetime as dt

    # prepare the output
    data_dict_output = {}

    #######################
    # --- LOAD THE DATA ---
    #######################
    data_dict_spatial = stl.loadDictFromFile(f'{UserToggles.run_folder_path}/spatial_environment.cdf')
    Epoch_range = data_dict_spatial['Epoch_model'][0]
    glon_range = data_dict_spatial['glons_model'][0]
    glat_range = data_dict_spatial['glats_model'][0]
    alts_range = data_dict_spatial['alts_model'][0]

    ##############################
    # --- GENERATE THE B-FIELD ---
    ##############################
    example_var = np.zeros(shape=(len(Epoch_range), len(alts_range)))
    data_dict_output = {
        'Epoch_model': deepcopy(data_dict_spatial['Epoch_model']),
        'alts_model': deepcopy(data_dict_spatial['alts_model']),
        '|B|': [deepcopy(example_var), {'DEPEND_1': 'alts_model', 'DEPEND_0': 'Epoch_model', 'UNITS': 'T', 'LABLAXIS': '|B|', 'VAR_TYPE': 'data'}],
    }

    for tmeIdx in tqdm(range(len(data_dict_spatial['Epoch_model'][0]))):

        times = [Epoch_range[tmeIdx] for i in range(len(alts_range))]
        for idx,epochVal in enumerate(times):
            seconds_since_Jan1st_in_ephmeris_data = (pycdf.lib.datetime_to_tt2000(epochVal) - pycdf.lib.datetime_to_tt2000(dt.datetime(Epoch_range[0].year, 1, 1))) / 1E9
            times[idx] = dt.datetime(2016, 1, 1) + dt.timedelta(seconds=seconds_since_Jan1st_in_ephmeris_data)

        lats = [glat_range[tmeIdx] for i in range(len(alts_range))]
        longs = [glon_range[tmeIdx] for i in range(len(alts_range))]

        # Get the Chaos model
        B = stl.CHAOS(lats, longs, np.array(alts_range) , times)
        Bmag = (1E-9) * np.array([np.linalg.norm(Bvec) for Bvec in B])

        # store the data
        data_dict_output['|B|'][0][tmeIdx] = Bmag

    outputPath = rf'{UserToggles.run_folder_path}/geomagnetic_field.cdf'
    stl.outputDataDict(outputPath, data_dict_output)


