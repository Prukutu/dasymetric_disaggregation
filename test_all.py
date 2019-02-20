import dasymetry as dasy
import geopandas as gp

disagg = dasy.DasymetryDisaggregate()

parcels = disagg.load_parcels('testdata/MN_PLUTO_SUBSET.shp')
source = disagg.load_source_data('testdata/nad_subset.shp')

disagg.generate_intersects()

disagg.source_aggregator('pop10')

print(disagg.parcel_df['pop10'].dropna().describe())
