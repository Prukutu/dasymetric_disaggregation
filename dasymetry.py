import geopandas

# TODO: write disaggregate_data method
# TODO: document all methods
class DasymetryDisaggregate:
    """ Class collecting tools to disaggregate socio-demographic data into
        discrete parcels.
    """

    def __init__(self):

        return None

    def load_parcels(self, filename):
        """ Method to load parcel geometry. Uses geopandas to load a shapefile
            into a GeoDataFrame.

            Input:
            ------
            filename: string describing parcel file name. Directory must contain
            all relevant files.

            Output:
            -------
            parcel_df: GeoDataFrame object containing parcel data and geometry.
        """

        print('Loading parcel data...')

        self.parcel_df = geopandas.read_file(filename)

        print(filename + ' loaded!')

        return self.parcel_df

    def load_source_data(self, filename):
        # Load data to disaggregate into all parcels.
        return None

    def disaggregate_data(self, parceldata, sourcedata):
        # Following the work of Dahal and McPhearson (in preparation)

        return None
