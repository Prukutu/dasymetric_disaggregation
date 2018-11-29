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

        print('Loading parcel data...')

        self.parcel_df = geopandas.read_file(filename)

        print(filename + ' loaded!')

        return self.parcel_df

    def load_source_data(self, filename):
        # Load data to disaggregate. Join with geometry
        return None

    def disaggregate_data(self, parceldata, sourcedata):
        # Following the work of Dahal and McPhearson (in preparation)

        return None
