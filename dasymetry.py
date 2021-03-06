import geopandas
import pandas
# TODO: write disaggregate_data method
# TODO: document all methods

class DasymetryDisaggregate:

    """ Class collecting tools to disaggregate socio-demographic data into
        discrete parcels.
    """

    def __init__(self):

        # Add any top-level parameters here.

        return None

    def load_parcels(self, filename, fid='bbl'):

        """ Method to load parcel geometry. Uses geopandas to load a shapefile
            into a GeoDataFrame.

            Input:
            ------
            filename (str): string describing parcel file name, including
            absolute path to directory containing the files, if not the current
            working directory.

            fid (str): Name of the column name that identifies each parcel.
            Default bbl from NYC MapPLUTO.

            Output:
            -------
            parcel_df: GeoDataFrame object containing parcel data and geometry.
        """

        # Make the feature id a class attribute
        self.parcel_fid = fid

        print('Loading parcel data...')

        self.parcel_df = geopandas.read_file(filename)

        print(filename + ' loaded!')

        # Make all column names lowercase
        self.parcel_df.columns = map(str.lower, self.parcel_df.columns)

        # Make fid into the GeoDataFrame index.
        self.parcel_df.set_index(fid, inplace=True)

        return self.parcel_df

    def load_source_data(self, filename, fid='blockid10'):

        """ Method to load source data and geometry. Uses geopandas to load a
            shapefile into a GeoDataFrame.

            Input:
            ------
            filename (str): string describing parcel file name, including
            absolute path to directory containing the files, if not the current
            working directory.

            fid (str): Name of the column name that identifies each parcel.
            Default BLOCKID10, from US Census.

            Output:
            -------
            source_df: GeoDataFrame object containing parcel data and geometry.
        """

        # Make the feature id a class attribute
        self.source_fid = fid

        print('Loading source data...')
        # Load data to disaggregate into all parcels.
        self.source_df = geopandas.read_file(filename)
        self.source_df.columns = map(str.lower, self.source_df.columns)

        print(filename + ' loaded!')

        # Make fid into the GeoDataFrame index.
        self.source_df.set_index(fid, inplace=True)

        return self.source_df

    def generate_intersects(self):
        """ Create two GeoDataFrames containing of (a) parcels whose centroids
            lie within each census block, and (b) census blocks whose centroids
            lie within each parcel.

        """

        # Create copies of the source shapefiles, substituting their geometry
        # for their centroids (point feature)
        def polygon_to_point(df):
            df_with_centroid = df.copy()
            df_with_centroid['geometry'] = df.centroid

            return df_with_centroid

        # Join all points that lie in a polygon with that feature
        def find_intersects(df_polygon, df_centroids):
            datasubset = [geopandas.sjoin(df_polygon.loc[[k]],
                                                 df_centroids)
                                 for k in df_polygon.index]
            return pandas.concat(datasubset)

        # Then, we find the two "centroid in polygon datasets"
        parcel_centroid = polygon_to_point(self.parcel_df)
        source_centroid = polygon_to_point(self.source_df)

        self.blocks_in_parcels = find_intersects(self.parcel_df,
                                                 source_centroid)

        # We only care about tax lots that contain > 1 census blocks, like
        # in Stuyvesant Town (1 parcel, 15 tax lots). Keep only duplicates.
        self.blocks_in_parcels = self.blocks_in_parcels[self.blocks_in_parcels.index.duplicated(keep=False)]

        self.parcels_in_blocks = find_intersects(self.source_df,
                                                 parcel_centroid)

    def source_aggregator(self, fieldname):
        """ Method that takes parcels that contain more than one source block,
            aggregates the data, then assign its sum to the parcel.

            Input:
            ======
            self.source_df:
            self.parcel_df:
            self.blocks_in_parcels

            Output:
            =======
            Writes the aggregated block data to parcel_df
        """
        source_data=self.source_df
        lots_data=self.blocks_in_parcels

        # Group lots_data by lot index, then sum all values under fieldname

        data_sums = lots_data.groupby(lots_data.index).sum()[fieldname]
        lotnames = data_sums[lots_data.index].unique()

        # Write the sums to their respective lots in parcel_df
        self.parcel_df.loc[data_sums.index, fieldname] = data_sums.values

        return None

    def pop_misc_parks(fieldname, remaining_pop, misc_lots, parks_lots, top_den_allowed):

        total_misc_area = sum(misc_lots["lotarea"])
        misc_lots["area_ratio"] = misc_lots["lotarea"]/total_misc_area

        total_parks_area = sum(parks_lots["lotarea"])
        parks_lots["area_ratio"] = parks_lots["lotarea"]/total_parks_area

        if len(misc_lots) > 0 & len(parks_lots) > 0:

            pop_den = float(remaining_pop)/total_misc_area

            if pop_den <= top_den_allowed:

                misc_lots[fieldname] = misc_lots["area_ratio"]*remaining_pop

                remaining_pop = remaining_pop - sum(misc_lots[fieldname])

                self.parcel_df.loc[misc_lots.index, fieldname] = misc_lots[fieldname].values

            elif pop_den > top_den_allowed:

                misc_lots[fieldname] = top_den_allowed*misc_lots["lotarea"]

                self.parcel_df.loc[misc_lots.index, fieldname] = misc_lots[fieldname].values

                remaining_pop = remaining_pop - sum(misc_lots[fieldname])

                pop_den_parks = float(remaining_pop)/total_parks_area

                if pop_den_parks <=5:

                    parks_lots[fieldname] = parks_lots["area_ratio"]*remaining_pop

                    self.parcel_df.loc[parks_lots.index, fieldname] = parks_lots[fieldname].values

                    remaining_pop = remaining_pop - sum(parks_lots[fieldname])

                elif pop_den_parks > 5:

                    parks_lots[fieldname] = 5*parks_lots["lotarea"]

                    self.parcel_df.loc[parks_lots.index, fieldname] = parks_lots[fieldname].values

                    remaining_pop = remaining_pop - sum(parks_lots[fieldname])

        elif len(misc_lots) > 0 & len(parks_lots) == 0:

            pop_den = float(remaining_pop)/total_misc_area

            if pop_den <= top_den_allowed:

                misc_lots[fieldname] = misc_lots["area_ratio"]*remaining_pop

                self.parcel_df.loc[misc_lots.index, fieldname] = misc_lots[fieldname].values

                remaining_pop = remaining_pop - sum(misc_lots[fieldname])

            elif pop_den > top_den_allowed:

                misc_lots[fieldname] = top_den_allowed*misc_lots["lotarea"]

                self.parcel_df.loc[misc_lots.index, fieldname] = misc_lots[fieldname].values

                remaining_pop = remaining_pop - sum(misc_lots[fieldname])

        elif len(misc_lots) == 0 & len(parks_lots) > 0:

            pop_den_parks = float(remaining_pop)/total_parks_area

            if pop_den_parks <=5:

                parks_lots[fieldname] = parks_lots["area_ratio"]*remaining_pop

                self.parcel_df.loc[parks_lots.index, fieldname] = parks_lots[fieldname].values

                remaining_pop = remaining_pop - sum(parks_lots[fieldname])

            elif pop_den_parks > 5:

                parks_lots[fieldname] = 5*parks_lots["lotarea"]

                self.parcel_df.loc[parks_lots.index, fieldname] = parks_lots[fieldname].values

                remaining_pop = remaining_pop - sum(parks_lots[fieldname])

        elif len(misc_lots) == 0 & len(parks_lots) == 0:

            pass

        return(remaining_pop)



    def source_disaggregator(self, fieldname, top_hh_size, top_den_allowed):


        for index in self.parcels_in_blocks.index:
            population_disaggregate = self.parcels_in_blocks.loc[index,fieldname]
            subset_lots = lots[lots.centroid.intersects(blocks)] #####NEED TO REPLACE WITH THE MAGIC FROM LUIS
            res_units = sum(subset_lots["unitsres"])

            if res_units > 0:

                res_pop_ratio = population_disaggregate/res_units

                subset_lots_residential = subset_lots[subset_lots["unitres"]>0]


                subset_lots_residential["res_ratio"] = subset_lots_residential["unitres"]/res_units

                subset_lots_misc = subset_lots_non_residential[(subset_lots_non_residential["bldgclass"].str.contains("^I")) | (subset_lots_non_residential["bldgclass"].str.contains("^M")) | (subset_lots_non_residential["bldgclass"].str.contains("^N")) | (subset_lots_non_residential["bldgclass"].str.contains("Y3")) | (subset_lots_non_residential["bldgclass"].str.contains("^W"))]

                subset_lots__parks = subset_lots_non_residential[subset_lots_non_residential["landuse"]=="09"]

                if res_pop_ratio <= top_hh_size:

                    subset_lots_residential[fieldname] = subset_lots_residential["res_ratio"] * population_disaggregate

                    self.parcel_df.loc[subset_lots_residential.index, fieldname] = subset_lots_residential[fieldname].values

                elif res_pop_ratio > top_hh_size:

                    # if only resunits in block
                    if len(subset_lots_residential) == len(subset_lots) | len(subset_lots__parks) == 0 & len(subset_lots_misc) == 0:

                        subset_lots_residential[fieldname] = subset_lots_residential["res_ratio"] * population_disaggregate

                        self.parcel_df.loc[subset_lots_residential.index, fieldname] = subset_lots_residential[fieldname].values

                    # more than residential
                    elif len(subset_lots_residential) < len(subset_lots):

                        subset_lots_residential[fieldname] = subset_lots_residential["unitsres"] * top_hh_size

                        self.parcel_df.loc[subset_lots_residential.index, fieldname] = subset_lots_residential[fieldname].values

                        remaining_pop = population_disaggregate - sum(subset_lots_residential[fieldname])

                        # Function that distributes remaining population across the misc. lots and parks.
                        remaining_pop = pop_misc_parks(fieldname, remaining_pop, subset_lots_misc, subset_lots__parks, top_den_allowed)

                    # What if there is still population after distributing it across res, misc and parks? then we add it to the one already allocated in the
                    # residential lots and re-write it in the parcel_df.
                    if remaining_pop > 0:

                        subset_lots_residential[fieldname] = subset_lots_residential[fieldname] + (subset_lots_residential["res_ratio"]*remaining_pop)
                        self.parcel_df.loc[subset_lots_residential.index, fieldname] = subset_lots_residential[fieldname].values

            elif res_units == 0:

                # prepare subsets of the non residential lots (which may be all, actually), those that have misc use, and parks
                subset_lots_non_residential = subset_lots[subset_lots["unitres"]==0]

                subset_lots_misc = subset_lots_non_residential[(subset_lots_non_residential["bldgclass"].str.contains("^I")) | (subset_lots_non_residential["bldgclass"].str.contains("^M")) | (subset_lots_non_residential["bldgclass"].str.contains("^N")) | (subset_lots_non_residential["bldgclass"].str.contains("Y3")) | (subset_lots_non_residential["bldgclass"].str.contains("^W"))]

                subset_lots__parks = subset_lots_non_residential[subset_lots_non_residential["landuse"]=="09"]

                #distribute population across misc and parks using the function
                remaining_pop = pop_misc_parks(fieldname, population_disaggregate, subset_lots_misc, subset_lots__parks, top_den_allowed)

                # If there is population left, but no residential lots, we allocate them in the misc uses.
                if remaining_pop > 0:

                    if len(subset_lots_misc) > 0:

                        total_misc_area = sum(subset_lots_misc["lotarea"])
                        subset_lots_misc["area_ratio"] = subset_lots_misc["lotarea"]/total_misc_area

                        subset_lots_misc[fieldname] = subset_lots_misc["area_ratio"]*remaining_pop

                        self.parcel_df.loc[subset_lots_misc.index, fieldname] = subset_lots_misc[fieldname].values + self.parcel_df.loc[subset_lots_misc.index, fieldname]

                    # If misc lots not available, we distribute the remaining population across the entire subset of non_residential lots.
                    elif len(subset_lots_misc) == 0:

                        total_nonres_area = sum(subset_lots_non_residential["lotarea"])
                        subset_lots_non_residential["area_ratio"] = subset_lots_non_residential["lotarea"]/total_misc_area

                        subset_lots_non_residential[fieldname] = subset_lots_non_residential["area_ratio"]*remaining_pop

                        self.parcel_df.loc[subset_lots_non_residential.index, fieldname] = subset_lots_non_residential[fieldname].values

        return None # I understand that the function does not need to return anything, since we already wrote the values in self.parcel_df

    def disaggregate_data(self, fieldname, top_hh_size = 2.8, top_den_allowed = 55):

        """ Disaggregate fieldname from source_df into parcels.

            Input:
            ------
            fieldname (str): Name of field to be disaggregated. Must exist in
            source_df

            kwargs:
            -------
            top_hh_size (float): maximum number of people to allocate to a
            residential unit.

            Output:
            -------
            parcel_df (GeoDataFrame): GeoDataFrame with source data
            disaggregated to each parcel.
        """

        # Following the work of Dahal and McPhearson (in preparation)
        # 1) check if fieldname exists in the sourcedata
        msg = 'Error: fieldname does not exist in source data!'
        assert fieldname in self.source_df.columns, msg

        # 2) create columns in parceldata with the names of fieldnames
        self.parcel_df[fieldname] = 0

        # 3) are there entities from sourcedata located within entities of parcel data (MORE THAN ONE ENTITY)?
        self.source_df_centroids = self.source_df.centroid
        self.parcel_df = self.intersect_counter(self.source_df_centroids, self.parcel_df)

        #### 3.1) subset lots that have sourcedata entities within / subset lots that have no sourcedata entities within (count <=1)
        self.blocks_in_parcels = self.parcel_df[self.parcel_df["count"] > 1]
        self.parcels_in_blocks = self.parcel_df[self.parcel_df["count"] <= 1]

        #### 3.2) aggregate data of sourcedata within blocks_in_parcels --> loop that goes lot by lot and aggregates the info of
        #### the centroids within

        #### First we need to check whether there is one or more rows in the blocks_in_parcels dataset!

        if len(self.blocks_in_parcels) > 0:

            self.aggregated_lots = source_aggregator(fieldname)

        #### 4) take parcels_in_blocks and run disaggregation

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

            drop_geometry (bool): Whether to drop geometry column in output
            (default False)

            driver (str): Supported file driver. Check fiona.supported_drivers
            for compatibility.

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
