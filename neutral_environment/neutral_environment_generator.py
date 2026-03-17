# --- ionoNeutralEnvironment_Generator ---
# get the NRLMSIS data and export the neutral environment

def neutral_environment_generator(**kwargs):

    # --- common imports ---
    import spaceToolsLib as stl
    import numpy as np
    from tqdm import tqdm
    from glob import glob
    from copy import deepcopy
    from src.user_inputs.user_toggles import UserToggles
    from src.neutral_environment.neutral_toggles import NeutralsToggles
    import spaceweather as sw


    # --- file-specific imports ---
    from numpy import datetime64, squeeze
    import pymsis


    #######################
    # --- LOAD THE DATA ---
    #######################
    # get the geomagnetic field data dict
    data_dict_spatial = stl.loadDictFromFile(glob(rf'{UserToggles.run_folder_path}/spatial_environment.cdf')[0])
    Epoch_range = data_dict_spatial['Epoch_model'][0]
    glon_range = data_dict_spatial['glons_model'][0]
    glat_range = data_dict_spatial['glats_model'][0]
    alts_range = data_dict_spatial['alts_model'][0]


    ############################
    # --- PREPARE THE OUTPUT ---
    ############################
    example_var = np.zeros(shape=(len(Epoch_range), len(alts_range)))

    data_dict_output = {
        'Epoch_model':deepcopy(data_dict_spatial['Epoch_model']),
        'alts_model': deepcopy(data_dict_spatial['alts_model']),
        'rho_n': [deepcopy(example_var), {}],
        'N2': [deepcopy(example_var), {}],
        'O2': [deepcopy(example_var), {}],
        'O': [deepcopy(example_var),{}],
        'HE': [deepcopy(example_var),{}],
        'H': [deepcopy(example_var),{}],
        'AR': [deepcopy(example_var),{}],
        'N': [deepcopy(example_var),{}],
        'ANOMALOUS_O': [deepcopy(example_var),{}],
        'NO': [deepcopy(example_var),{}],
        'Tn': [deepcopy(example_var),{}],
        'm_eff_n': [deepcopy(example_var),{}]
    }

    # --- Get the Spaceweather indices ---
    sw_indices = sw.sw_daily(update=True)
    target_datetime = data_dict_spatial['Epoch_model'][0][0]
    target_date = f'{target_datetime.year}-{target_datetime.month}-{target_datetime.day}'
    f107 = sw_indices['f107_adj'].loc[target_date]
    f107a = sw_indices['f107_81ctr_adj'].loc[target_date]
    aps = [
            [sw_indices['Ap0'].loc[target_date],
            sw_indices['Ap3'].loc[target_date],
            sw_indices['Ap6'].loc[target_date],
            sw_indices['Ap9'].loc[target_date],
            sw_indices['Ap12'].loc[target_date],
            sw_indices['Ap15'].loc[target_date],
            sw_indices['Ap18'].loc[target_date]]
           ]

    ##############################
    # --- GET THE NRLMSIS DATA ---
    ##############################

    for tmeIdx in tqdm(range(len(data_dict_spatial['Epoch_model'][0]))):

        timeVal = Epoch_range[tmeIdx]
        glonVal = glon_range[tmeIdx]
        glatVal = glat_range[tmeIdx]
        date=datetime64(timeVal)

        #  output is of the shape (1, 1, 1, len(alts),11), use squeeze to Get rid of the single dimensions
        NRLMSIS_data = squeeze(pymsis.calculate(date, glonVal, glatVal, alts_range, f107, f107a, aps))

        for var in pymsis.Variable: # note, "var" is just an index

            # Make some naming/attribute adjustments
            varData = NRLMSIS_data[:,var]

            if var.name =='MASS_DENSITY':
                varUnits = 'kg m!A-3!N'
                varName = 'rho_n'

            elif var.name =='TEMPERATURE':
                varUnits = 'K'
                varName = 'Tn'
            else:
                varUnits = 'm!A-3!N'
                varName = var.name

            # store the data
            data_dict_output[f'{varName}'][0][tmeIdx] = deepcopy(varData)

            # Set the attributes once
            if tmeIdx == 0:
                data_dict_output[f'{varName}'][1] = {'DEPEND_0':'Epoch_model','DEPEND_1':'alts_model','UNITS': varUnits, 'LABLAXIS': f'{varName}', 'VAR_TYPE': 'data'}


    # add the total neutral density
    n_n = np.array([data_dict_output[f"{key}"][0] for key in NeutralsToggles.wNeutrals])
    data_dict_output = {**data_dict_output, **{'nn': [np.sum(n_n,axis=0), {'DEPEND_0':'Epoch_model','DEPEND_1':'alts_model', 'UNITS': 'm!A-3!N', 'LABLAXIS': 'nn', 'VAR_TYPE':'data'}]}}

    # add the effective neutral mass
    m_eff_n = np.sum(np.array( [stl.netural_dict[key]*data_dict_output[f"{key}"][0] for key in NeutralsToggles.wNeutrals]), axis=0)/data_dict_output['nn'][0]
    data_dict_output = {**data_dict_output, **{'m_eff_n': [m_eff_n, {'DEPEND_0':'Epoch_model','DEPEND_1':'alts_model', 'UNITS': 'kg', 'LABLAXIS': 'm_eff_n', 'VAR_TYPE':'data'}]}}

    #####################
    # --- OUTPUT DATA ---
    #####################
    outputPath = rf'{UserToggles.run_folder_path}/neutral_environment.cdf'
    stl.outputDataDict(outputPath, data_dict_output)
