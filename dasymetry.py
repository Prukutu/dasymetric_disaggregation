import geopandas

# TODO: write disaggregate_data method
# TODO: document all methods

class DasymetryDisaggregate:
    """ Class collecting tools to disaggregate socio-demographic data into
        discrete parcels.
    """

    def __init__(self):

        # Add any top-level parameters here.

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
        self.parcel_df.columns = map(str.lower, self.parcel_df.columns)

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
        self.source_df.columns = map(str.lower, self.source_df.columns)

        return self.source_df

    def intersect_counter(self, centroids, boundaries):
        """ A function that will count the number of centroids that fall within
            the boundaries of another layer.

            Input:
            ------
            centroids (float): Centroid coordinates of each source layer to
            disaggregate.

            boundaries (polygon ??): Boundaries of the target layer.
        """
        boundaries["count"] = 0

        for i, bound in enumerate(boundaries):
            # inter_count=0
            CD = boundaries.loc[[i]]
            inter_count = sum(centroids.intersects(CD))
            boundaries.loc[i,"count"] = inter_count
        
        return boundaries
    
    def source_aggregator (self, fieldname):
        source_data=self.source_df
        lots_data=self.lots_to_aggregateblocks
        for index in lots_data.index: #### !!!! I USE INDEXES IN THE LOOP BECAUSE THEY DONT GO 1 BY 1 ANYMORE AFTER THE SUBSET !!!!
            lot = lots_data[[index]] # subsample one single lot
            subset = source_data[source_data.centroid.intersects(lot)] # subset blocks that locate within the subsampled lot
            lots_data.loc[index, fieldname] = sum(subset[fieldname]) # Sum of all the values of the fieldname written in the column of aggregated values
            
        return lots_data
    
    def source_disaggregator (self, fieldname, top_hh_size):
        lots = self.lots_to_disaggregateblocks
        blocks = self.source_df
        for index in blocks.index:
            population_disaggregate = source_df.loc[index,fieldname]
            subset_lots = lots[lots.centroid.intersects(blocks)]
            res_lots = sum(subset_lots["unitsres"])
            
            if res_lots > 0:
                
                res_pop_ratio = population_disaggregate/res_lots
                subset_lots_residential = subset_lots[subset_lots["unitres"]>0]
                
                if res_pop_ratio <= top_hh_size:
                                       
                    subset_lots_residential[fieldname] = res_pop_ratio * subset_lots["unitres"]
                    lots.loc[lots.bbl.isin(subset_lots.bbl), [fieldname]] = subset_lots_residential[[fielname]]
                    
                else if population_disaggregate > top_hh_size:
                    
                    subset_lots_residential[fieldname] = res_pop_ratio * top_hh_size
                    remaining_pop = population_disaggregate - sum(subset_lots_residential[fieldname])
                    
            
            else if res_lots == 0:
            
    def disaggregate_data(self, fieldname, top_hh_size = 2.8):
        # Following the work of Dahal and McPhearson (in preparation)
        # 1) check if fieldname exists in the sourcedata
        assert(fieldname in list(self.source_df)), "Error: fieldname does not exist in source data!"

        # 2) create columns in parceldata with the names of fieldnames
        self.parcel_df[fieldname] = 0

        # 3) are there entities from sourcedata located within entities of parcel data (MORE THAN ONE ENTITY)?
        self.source_df_centroids = self.source_df.centroid
        self.parcel_df = intersect_counter(self.source_df_centroids, self.parcel_df)

        #### 3.1) subset lots that have sourcedata entities within / subset lots that have no sourcedata entities within (count <=1)
        self.lots_to_aggregateblocks = self.parcel_df[self.parcel_df["count"] > 1]
        self.lots_to_disaggregateblocks = self.parcel_df[self.parcel_df["count"] <= 1]
        
        #### 3.2) aggregate data of sourcedata within lots_to_aggregateblocks --> loop that goes lot by lot and aggregates the info of 
        #### the centroids within
        
        #### First we need to check whether there is one or more rows in the lots_to_aggregateblocks dataset!
        if len(lots_to_aggregateblocks) > 0:
            self.aggregated_lots = source_aggregator(fieldname)            

        #### 4) take lots_to_disaggregateblocks and run disaggregation
        
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
