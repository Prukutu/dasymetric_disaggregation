import sys
import unittest

import geopandas

sys.path.append('/home/luis/github/dasymetric_disaggregation/')
import dasymetry

dasy = dasymetry.Dasymetry()
parcel_df = dasy.load_parcels('SIMapPLUTO.shp')

# Do a few tests on our data loading methods
class TestDataLoadMethods(unittest.TestCase):

    def test_parcel_df_type(self):
        self.assertEqual(type(parcel_df), geopandas.GeoDataFrame)

suite = unittest.TestLoader().loadTestsFromTestCase(TestDataLoadMethods)
unittest.TextTestRunner(verbosity=2).run(suite)
