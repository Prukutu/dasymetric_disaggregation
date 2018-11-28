import sys

sys.path.append('/home/luis/github/dasymetric_disaggregation/')

import dasymetry

dasy = dasymetry.Dasymetry()

df = dasy.load_parcels('SIMapPLUTO.shp')
