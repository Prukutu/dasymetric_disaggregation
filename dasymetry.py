import geopandas

# TODO: write disaggregate_data method
# TODO: document all methods
#### HOLA LUIS ESTE ES UN INTENTO DE PUSH
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
            filename: string describing parcel file name, including absolute
            path to directory containing the files, if not the current working
            directory.

            Output:
            -------
            parcel_df: GeoDataFrame object containing parcel data and geometry.
        """

        print('Loading parcel data...')

        self.parcel_df = geopandas.read_file(filename)

        print(filename + ' loaded!')

        return self.parcel_df

    def load_source_data(self, filename):
        """ Method to load source data and geometry. Uses geopandas to load a
            shapefile into a GeoDataFrame.

            Input:
            ------
            filename: string describing parcel file name, including absolute
            path to directory containing the files, if not the current working
            directory.

            Output:
            -------
            source_df: GeoDataFrame object containing parcel data and geometry.
        """

        print('Loading source data...')
        # Load data to disaggregate into all parcels.
        self.source_df = geopandas.read_file(filename)

        return self.source_df

    def disaggregate_data(self, parceldata, sourcedata):
        # Following the work of Dahal and McPhearson (in preparation)
        # If
        return None

    def write_output(self, outputfilename, outputdir='output/'):

        return None
