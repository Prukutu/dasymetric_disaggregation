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
            filename (str): string describing parcel file name, including absolute
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
            filename (str): string describing parcel file name, including absolute
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

    def disaggregate_data(self, fieldnames, max_hh_size=2.8):

        self.disaggregate_df = []
        # Following the work of Dahal and McPhearson (under review)
        # 1) check if the fieldnames exist in the sourcedata
        # 2) create columns in parceldata with the names of fieldnames
        # 3) are there entities from sourcedata located within entities of parcel data?

        #### 3.1) subset lots that have sourcedata entities within
        #### 3.2) aggregate data of sourcedata within englobing lot
        #### 3.3) output: two subsets:

        ######## 3.3.1) One of lots with aggregated data
        ######## 3.3.2) Another one with the rest of the lots.

        #### !!!!!! If there were no lots with source entities within, then only output 3.3.2).

        #### 4) take output 3.3.2 and run disaggregation

        #### 4.1) Loop per sourcedata entity
        #### 4.2) Retrieve total population / number from sourcedata
        #### 4.3) Subset lots that fall within the entity
        #### 4.4) Sum of ResUnits in the subset lots

        ######## 4.4.1) ResUnits > 0?

        ############ 4.4.1.1) people per residential unit =< top_hh_size?

        ################ 4.4.1.1.1) population in lot = people per residential units * nr of ResUnits in lot

        ############ 4.4.1.2) people per residential unit > top_hh_size?

        ################ 4.4.1.2.1) population in lot = people per residential units * top_hh_size
        ################ 4.4.2.2.2) remaining population in miscelanous units (areal weighted)
        ################ 4.4.2.2.3) remaining population in parks (areal weighted)

        ######## 4.4.2) ResUnits = 0?

        ############ 4.4.2.1) areal weighted distribution across lots of block (start by misc, then parks)

        # 5) merge the two subsets of aggregatd / disaggregated lotsdata

        # 6) go get a beer

        return None

    def write_output(self, outputfilename,
                     outputdir='output/',
                     drop_geometry=False,
                     driver='ESRI Shapefile'):

        """ Write self.disaggregate_df to outputfilename in directory
            outtputdir. By default, output file includes geometry features,
            but they may be skipped when saving in non-geometric file types.

            Input:
            ------
            outputfilename (str): File name of the output file(s)

            outputdir (str): Directory path to save data (default = ./output/)

            drop_geometry (bool): Whether to drop geometry column in output (default False)

            driver (str): Supported file driver. Check fiona.supported_drivers for
            compatibility.

            Output:
            -------
            None
        """
        # geopandas supports fiona drivers, so we check if driver kwarg is valid
        from fiona import supported_drivers

        msg = 'Kwarg driver is not supported!, check fiona.supported_drivers!'
        assert driver in supported_drivers.keys(), msg

        spatial_drivers = ('ESRI Shapefile', 'GeoJSON')
        if drop_geometry is True and driver in spatial_drivers:
            raise ValueError('Cannot drop geometry with ' + spatial_driver)

        if drop_geometry is True:
            outstring = outputdir + outputfilename
            disaggregate_df.drop(columns=['geometry']).to_file(outstring,
                                                               driver=driver)

        else:
            disaggregate_df.to_file(outstring, driver=driver)

        return None
