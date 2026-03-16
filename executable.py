# --- executable.py ---
# --- Author: C. Feltman ---
# DESCRIPTION: execute the IRI code

#################
# --- IMPORTS ---
#################
from executable_toggles import dict_executable
from user_inputs.user_toggles import UserToggles


# re-run everything
if dict_executable['regen_EVERYTHING']==1:
    for key in dict_executable.keys():
        dict_executable[key] = 1

if dict_executable['regen_IRI_profile']==1:
    if RunToggles.useEphemerisData:
        print('\n--- Regenerating IRI profile from ephemeris ---', end='\n')
        from src.IRI_profile.IRI_profile_from_ephemeris_generator import generate_IRI_profile_from_ephemeris
        generate_IRI_profile_from_ephemeris()
    else:
        print('\n--- Regenerating IRI profile ---', end='\n')
        from src.IRI_profile.IRI_profile_generator import generate_IRI_profile
        generate_IRI_profile()

if dict_executable['regen_IRI_conductivity'] == 1:
    print('\n--- Calculating IRI Conductivity ---', end='\n')
    from src.conductivity.IRI_conductivity_generator import generate_IRI_conductivity
    generate_IRI_conductivity()

