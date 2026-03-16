import  datetime as dt

class UserToggles:

    # --- TOGGLES ---

    # use a satellite path to generate IRI height profiles along those geographic points
    useEphemerisData = True
    path_to_ephemeris_data = '/home/connor/Data/SATELLITES/TRACERS/ead/2025/09/27/ts2/ts2_def_ead_20250927_v0.10.1.cdf'
    ephemeris_glat_key_name = 'ts2_ead_lat_geod'
    ephemeris_glon_key_name = 'ts2_ead_lon_geod'
    ephemeris_time_key_name = 'Epoch'

    ephemeris_start_time = dt.datetime(2025,9,27,22, 16,00,00)
    ephermeris_stop_time = dt.datetime(2025,9,27,22, 22,00,00)

    ephemeris_time_resolution = 1 # in seconds. NOTE:  it's VERY important to down-sample data, otherwise it will take FOREVER to compile

    # --- IRI ALTITUDE RANGE ---
    alt_km_range_start = 90
    alt_km_range_end = 300
    alt_km_range_rez = 5

    #############################
    # --- MANUAL TIME TOGGLES ---
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # --- TIME RANGE ---
    start_year = '2020'
    start_month = '06'
    start_day = '01'
    start_hour = '00'
    start_minute = '00'
    start_second = '00'

    end_year = '2020'
    end_month = '06'
    end_day = '01'
    end_hour = '02'
    end_minute = '00'
    end_second = '00'
    time_step = dt.timedelta(minutes=30)

    # --- GEOPHYSICAL RANGE ---
    glat = 65,
    glon = -147.5

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$


    # File I/O
    output_path = '/home/connor/Data/MODELS/Ionosphere/'