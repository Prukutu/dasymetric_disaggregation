import sys
import unittest

import geopandas

sys.path.append('/home/luis/github/dasymetric_disaggregation/')
import dasymetry

dasy = dasymetry.DasymetryDisaggregate()
datadir = '/home/luis/github/dasymetric_disaggregation/testdata/'

# Do a few tests on our data loading methods
class TestDataLoadMethods(unittest.TestCase):

    def test_parcel_df_type(self):
        parcel_df = dasy.load_parcels(datadir + 'SIMapPLUTO.shp')
        self.assertIs(type(parcel_df), geopandas.GeoDataFrame)

    def test_source_df_type(self):
        source_df = dasy.load_source_data(datadir + 'tabblock2010_36_pophu.shp')
        self.assertIs(type(source_df), geopandas.GeoDataFrame)


suite = unittest.TestLoader().loadTestsFromTestCase(TestDataLoadMethods)
unittest.TextTestRunner(verbosity=2).run(suite)
