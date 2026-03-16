# --- TRACERS_ephemeris_to_conductivity ---
# Input a series of TRACERS empheris datum and calculate an ionospheric conductivity
# profile based on the geomagnetic field lines crossed

# imports
import PyIRI
import PyIRI.edp_update as ml  # Legacy PyIRI formalism (Fourier + empirical)
import PyIRI.sh_library as sh  # Updated PyIRI using spherical harmonics
import matplotlib.pyplot as plt
import numpy as np


def TRACERS_ephemeris_to_conductivity():
    # Specify date
    year = 2020
    month = 4
    day = 1

    # Specify solar activity index (F10.7 in SFU)
    F107 = 100

    # Select base coefficient set: 0 = CCIR, 1 = URSI
    ccir_or_ursi = 0

    # Location of interest: 10°E, 20°N
    alon = np.array([10.])
    alat = np.array([20.])

    # Time grid: Universal Time from 0 to 24 in 15-minute steps
    hr_res = 0.25
    aUT = np.arange(0, 24, hr_res)

    # Height grid: 90 km to 700 km in 1 km steps
    alt_res = 1
    alt_min = 90
    alt_max = 700
    aalt = np.arange(alt_min, alt_max, alt_res)

    # Coefficient sources and model options
    foF2_coeff = 'CCIR'  # Options: 'CCIR' or 'URSI'
    hmF2_model = 'SHU2015'  # Options: 'SHU2015', 'AMTB2013', 'BSE1979'
    coord = 'GEO'  # Coordinate system: 'GEO', 'QD', or 'MLT'
    coeff_dir = None  # Use default coefficient path

    # ----------------------------------------
    # Run PyIRI (Spherical Harmonics version)
    # ----------------------------------------
    # Compute ionospheric parameters for F2, F1, and E layers
    (F2,
     F1,
     E,
     sun,
     mag,
     EDP) = sh.IRI_density_1day(year,
                                month,
                                day,
                                aUT,
                                alon,
                                alat,
                                aalt,
                                F107,
                                coeff_dir=coeff_dir,
                                foF2_coeff=foF2_coeff,
                                hmF2_model=hmF2_model,
                                coord=coord)

    # Compute parameters for the sporadic E (Es) layer
    Es = sh.sporadic_E_1day(year,
                            month,
                            day,
                            aUT,
                            alon,
                            alat,
                            F107,
                            coeff_dir=coeff_dir,
                            coord=coord)


TRACERS_ephemeris_to_conductivity()