import sys
import unittest

import geopandas
import matplotlib.pyplot as plt

sys.path.append('/home/luis/github/dasymetric_disaggregation/')
import dasymetry

dasy = dasymetry.DasymetryDisaggregate()
datadir = '/home/luis/github/dasymetric_disaggregation/testdata/'
source_df = dasy.load_source_data(datadir + 'manhattan_test_source.shp')
parcel_df = dasy.load_parcels(datadir + 'manhattan_test.shp')

# Make projections consistent
parcel_df = parcel_df.to_crs(source_df.crs)

dasy.disaggregate_data('pop10')

# Do a few tests on our data loading methods
class TestDataLoadMethods(unittest.TestCase):

    def test_parcel_df_type(self):
        self.assertIs(type(parcel_df), geopandas.GeoDataFrame)

    def test_source_df_type(self):
        self.assertIs(type(source_df), geopandas.GeoDataFrame)


suite = unittest.TestLoader().loadTestsFromTestCase(TestDataLoadMethods)
unittest.TextTestRunner(verbosity=2).run(suite)
