
import iri2016.profile as iri
from datetime import datetime, timedelta
from matplotlib.pyplot import figure, show

time_start_stop = (datetime(2020, 6, 1, 0, 0, 0), datetime(2020, 6, 2))
time_step = timedelta(minutes=30)
alt_km_range = (100, 500, 10.)
glat = 82
glon = -147.5

sim = iri.IRI(time_start_stop, time_step, alt_km_range, glat, glon)

print(sim)