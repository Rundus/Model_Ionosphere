# --- generate_run ---


def generate_IRI_profile():

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
    alt_km_range = (RunToggles.alt_km_range_start, RunToggles.alt_km_range_end, RunToggles.alt_km_range_rez)

    # Form the time range
    start_datetime = dt.datetime(int(RunToggles.start_year),int(RunToggles.start_month),int(RunToggles.start_day), int(RunToggles.start_hour),int(RunToggles.start_minute),int(RunToggles.start_second))
    end_datetime = dt.datetime(int(RunToggles.end_year), int(RunToggles.end_month), int(RunToggles.end_day), int(RunToggles.end_hour), int(RunToggles.end_minute), int(RunToggles.end_second))
    time_start_stop = (start_datetime, end_datetime)



    # Form the latitude range
    glat_range = RunToggles.glat

    # Form the longitude range
    glon_range =RunToggles.glon

    # PERFORM THE RUN
    glons = np.linspace(10,15,10)
    glats = np.linspace(10, 15, 10)

    for glon in tqdm(glons):
        for glat in glats:
            sim = iri.timeprofile(tlim= time_start_stop,
                                  dt=RunToggles.time_step,
                                  altkmrange= alt_km_range,
                                  glat= glon,
                                  glon= glat)


    # output the results
    data_dict_output = {}
    data_dict_output = {**data_dict_output, **{'Epoch': [np.array([dt.datetime.strptime(str(val.to_numpy()), '%Y-%m-%dT%H:%M:%S.%f') for val in sim['time']]), {'DEPEND_0': None}]}}
    data_dict_output = {**data_dict_output, **{'alt': [np.array(sim['alt_km']), {'DEPEND_0': None,'UNITS':'km'}]}}

    for key in sim.keys():

        data = deepcopy(sim[key])
        attrs = {}

        if len(np.shape(data)) > 1:
            if len(np.shape(data)) == 2:
                attrs = {**attrs, **{'DEPEND_0':'Epoch','DEPEND_1':'alt'}}
            elif len(np.shape(data)) == 4:
                attrs = {**attrs, **{'DEPEND_0': 'Epoch','DEPEND_1':'alt','DEPEND_2':'glat','DEPEND_3':'glon'}}
        else:
            if len(data) == len(data_dict_output['Epoch'][0]):
                attrs = {**attrs, **{'DEPEND_0':'Epoch'}}

        # write out to the data_dict
        data_dict_output = {**data_dict_output,
                            **{f'{key}':[data,attrs]}}


    stl.outputDataDict(outputPath=f'{folder_path}/IRI_{RunToggles.start_year}{RunToggles.start_month}{RunToggles.start_day}_to_{RunToggles.end_year}{RunToggles.end_month}{RunToggles.end_day}.cdf', data_dict=data_dict_output)
