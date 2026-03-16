# --- executable.py ---
# --- Author: C. Feltman ---
# DESCRIPTION: execute the IRI code

#################
# --- IMPORTS ---
#################
from src.executable_toggles import dict_executable
from src.user_inputs.user_toggles import UserToggles
from src.executable_classes import ExecutableClasses


# Generate the Configuration File for this run
ExecutableClasses().generate_run_JSON()

# re-run everything
if dict_executable['regen_EVERYTHING']==1:
    for key in dict_executable.keys():
        dict_executable[key] = 1

if dict_executable['regen_plasma_environment']==1:
    if UserToggles.useEphemerisData:
        print('\n--- Regenerating Plasma Environment IRI profile from ephemeris ---', end='\n')
        from src.plasma_environment.plasma_environment_from_ephemeris_generator import generate_IRI_profile_from_ephemeris
        generate_IRI_profile_from_ephemeris()
    else:
        print('\n--- Regenerating Plasma Environment IRI profile ---', end='\n')
        from src.plasma_environment.plasma_environment_generator import generate_IRI_profile
        generate_IRI_profile()

if dict_executable['regen_geomagnetic_field']==1:
    print('\n--- Regenerating geomagnetic field ---', end='\n')
    from src.geomagnetic_field.geomagnetic_field_generator import geomagnetic_field_generator
    geomagnetic_field_generator()


if dict_executable['regen_conductivity'] == 1:
    print('\n--- Calculating Ionospheric Conductivity ---', end='\n')
    from src.conductivity.IRI_conductivity_generator import generate_IRI_conductivity
    generate_IRI_conductivity()

