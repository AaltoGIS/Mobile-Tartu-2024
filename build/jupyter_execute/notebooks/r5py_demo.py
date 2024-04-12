#!/usr/bin/env python
# coding: utf-8

# # Python: Basic usage of `r5py`
# 
# ```{admonition} Credits:
# 
# This tutorial was written by Henrikki Tenkanen, Christoph Fink & Willem Klumpenhouwer (i.e. `r5py` developer team).
# 
# ```
# ## Getting started
# 
# ### Run these codes in Binder
# 
# Before you can run this Notebook, and/or do any programming, you need to launch the Binder instance. You can find buttons for activating the python environment at the top-right of this page which look like this:
# 
# ![Launch Binder](../img/launch_binder.png)
# 
# ### Working with Jupyter Notebooks
# 
# Jupyter Notebooks are documents that can be used and run inside the JupyterLab programming environment containing the computer code and rich text elements (such as text, figures, tables and links). 
# 
# **A couple of hints**:
# 
# - You can **execute a cell** by clicking a given cell that you want to run and pressing <kbd>Shift</kbd> + <kbd>Enter</kbd> (or by clicking the "Play" button on top)
# - You can **change the cell-type** between `Markdown` (for writing text) and `Code` (for writing/executing code) from the dropdown menu above. 
# 
# See **further details and help for** [**using Notebooks and JupyterLab from here**](https://pythongis.org/part1/chapter-01/nb/04-using-jupyterlab.html). 
# 
# 
# ## Introduction
# 
# **R5py** is a Python library for routing and calculating travel time matrices on multimodal transport networks (walk, bike, public transport and car).
# It provides a simple and friendly interface to R<sup>5</sup> (*the Rapid Realistic Routing on Real-world and Reimagined networks*) which is a [routing engine](https://github.com/conveyal/r5) developed by [Conveyal](https://conveyal.com/). `R5py` is designed to interact with [GeoPandas](https://geopandas.org) GeoDataFrames, and it is inspired by [r5r](https://ipeagit.github.io/r5r) which is a similar wrapper developed for R. `R5py` exposes some of R5’s functionality via its [Python API](reference.html), in a syntax similar to r5r’s. At the time of this writing, only the computation of travel time matrices has been fully implemented. Over time, `r5py` will be expanded to incorporate other functionalities from R5. 

# ## Data requirements
# 
# ### Data for creating a routable network
# 
# When calculating travel times with `r5py`, you typically need a couple of datasets: 
# 
# - **A road network dataset from OpenStreetMap** (OSM) in Protocolbuffer Binary (`.pbf`) -format: 
#   - This data is used for finding the fastest routes and calculating the travel times based on walking, cycling and driving. In addition, this data is used for walking/cycling legs between stops when routing with transit. 
#   - *Hint*: Sometimes you might need modify the OSM data beforehand, e.g. by cropping the data or adding special costs for travelling (e.g. for considering slope when cycling/walking). When doing this, you should follow the instructions at [Conveyal website](https://docs.conveyal.com/prepare-inputs#preparing-the-osm-data). For adding customized costs for pedestrian and cycling analyses, see [this repository](https://github.com/RSGInc/ladot_analysis_dataprep).
# 
# - **A transit schedule dataset** in General Transit Feed Specification (GTFS.zip) -format (optional):
#    - This data contains all the necessary information for calculating travel times based on public transport, such as stops, routes, trips and the schedules when the vehicles are passing a specific stop. You can read about [GTFS standard from here](https://developers.google.com/transit/gtfs/reference).
#    - *Hint*: `r5py` can also combine multiple GTFS files, as sometimes you might have different GTFS feeds representing e.g. the bus and metro connections. 
# 
# 
# ### Data for origin and destination locations
# 
# In addition to OSM and GTFS datasets, you need data that represents the origin and destination locations (OD-data) for routings. This data is typically stored in one of the geospatial data formats, such as Shapefile, GeoJSON or GeoPackage. As `r5py` is build on top of `geopandas`, it is easy to read OD-data from various different data formats. 
# 
# 
# ### Where to get these datasets?
# 
# Here are a few places from where you can download the datasets for creating the routable network:
# 
# - **OpenStreetMap data in PBF-format**:
# 
#   - [pyrosm](https://pyrosm.readthedocs.io/en/latest/basics.html#protobuf-file-what-is-it-and-how-to-get-one)  -library. Allows downloading data directly from Python (based on GeoFabrik and BBBike).
#   - [pydriosm](https://pydriosm.readthedocs.io/en/latest/quick-start.html#download-data) -library. Allows downloading data directly from Python (based on GeoFabrik and BBBike).
#   - [GeoFabrik](http://download.geofabrik.de/) -website. Has data extracts for many pre-defined areas (countries, regions, etc).
#   - [BBBike](https://download.bbbike.org/osm/bbbike/) -website. Has data extracts readily available for many cities across the world. Also supports downloading data by [specifying your own area or interest](https://extract.bbbike.org/).
#   - [Protomaps](https://protomaps.com/downloads/osm) -website. Allows to download the data with custom extent by specifying your own area of interest.
# 
# 
# - **GTFS data**:  
#   - [Transitfeeds](https://transitfeeds.com/) -website. Easy to navigate and find GTFS data for different countries and cities. Includes current and historical GTFS data. Notice: The site will be depracated in the future.  
#   - [Mobility Database](https://database.mobilitydata.org) -website. Will eventually replace TransitFeeds -website. 
#   - [Transitland](https://www.transit.land/operators) -website. Find data based on country, operator or feed name. Includes current and historical GTFS data.
# 
# ### Sample datasets
# 
# In the following tutorial, we use various open source datasets:
# - The point dataset for Helsinki has been obtained from [Helsinki Region Environmental Services](https://www.hsy.fi/en/environmental-information/open-data/avoin-data---sivut/population-grid-of-helsinki-metropolitan-area/) (HSY) licensed under a Creative Commons By Attribution 4.0. 
# - The street network for Helsinki is a cropped and filtered extract of OpenStreetMap (© OpenStreetMap contributors, [ODbL license](https://www.openstreetmap.org/copyright))
# - The GTFS transport schedule dataset for Helsinki is a cropped and minimised copy of Helsingin seudun liikenne’s (HSL) open dataset [Creative Commons BY 4.0](https://www.hsl.fi/hsl/avoin-data#aineistojen-kayttoehdot).

# ## Installation
# 
# Before you can start using `r5py`, you need install it and a few libraries. Check [installation instructions](../installation.md) for more details. 

# ## Getting started with `r5py`
# 
# In this tutorial, we will learn how to calculate travel times with `r5py` between locations spread around the city center area of Helsinki, Finland. 
# 
# ### Load and prepare the origin and destination data
# 
# Let's start by downloading a sample dataset into a geopandas `GeoDataFrame` that we can use as our destination locations. To make testing the library easier, we have prepared a helper `r5py.sampledata.helsinki` which can be used to easily download the sample data sets for Helsinki (including population grid, GTFS data and OSM data). The population grid data covers the city center area of Helsinki and contains information about residents of each 250 meter cell:

# In[1]:


import geopandas as gpd
import osmnx as ox
import r5py.sampledata.helsinki as helsinki_data

pop_grid_fp = helsinki_data.population_grid
pop_grid = gpd.read_file(pop_grid_fp)
pop_grid.head()


# The `pop_grid` GeoDataFrame contains a few columns, namely `id`, `population` and `geometry`. The `id` column with unique values and `geometry` columns are required for `r5py` to work. If your input dataset does not have an `id` column with unique values, `r5py` will throw an error. 
# 
# To get a better sense of the data, let's create a map that shows the locations of the polygons and visualise the number of people living in each cell:

# In[6]:


pop_grid.explore("population", cmap="Reds")


# #### Convert polygon layer to points
# 
# Lastly, we need to convert the Polygons into points because **r5py expects that the input data is represented as points**. We can do this by making a copy of our grid and calculating the centroid of the Polygons. 
# 
# *Note: You can ignore the UserWarning raised by geopandas about the geographic CRS. The location of the centroid is accurate enough for most purposes.*

# In[15]:


# Convert polygons into points
points = pop_grid.copy()
points["geometry"] = points.centroid
points.explore(max_zoom=13, color="red")


# #### Retrieve the origin location by geocoding an address
# 
# Let's geocode an address for Helsinki Railway Station into a GeoDataFrame using `osmnx` and use that as our **origin** location:

# In[11]:


from shapely.geometry import Point 

address = "Railway station, Helsinki, Finland"
lat, lon = ox.geocode(address)

# Create a GeoDataFrame out of the coordinates
origin = gpd.GeoDataFrame({"geometry": [Point(lon, lat)], "name": "Helsinki Railway station", "id": [0]}, index=[0], crs="epsg:4326")
origin.explore(max_zoom=13, color="red", marker_kwds={"radius": 12})


# ### Load transport network
# 
# Virtually all operations of `r5py` require a transport network. In this example, we use data from Helsinki metropolitan area, which you can easily obtain from the `r5py.sampledata.helsinki` library. To import the street and public transport networks, instantiate an `r5py.TransportNetwork` with the file paths to the OSM extract and the GTFS files. 

# In[16]:


from r5py import TransportNetwork

# Get the filepaths to sample data (OSM and GTFS)
helsinki_osm = helsinki_data.osm_pbf
helsinki_gtfs = helsinki_data.gtfs

transport_network = TransportNetwork(
    # OSM data
    helsinki_osm,
    
    # A list of GTFS file(s)
    [
        helsinki_gtfs
    ]
)


# At this stage, `r5py` has created the routable transport network and it is stored in the `transport_network` variable. We can now start using this network for doing the travel time calculations. 

# ### Compute travel time matrix from one to all locations
# 
# A travel time matrix is a dataset detailing the travel costs (e.g., time) between given locations (origins and destinations) in a study area. To compute a travel time matrix with `r5py` based on public transportation, we first need to initialize an `r5py.TravelTimeMatrixComputer` -object. As inputs, we pass following arguments for the `TravelTimeMatrixComputer`:
# - `transport_network`, which we created in the previous step representing the routable transport network. 
# - `origins`, which is a GeoDataFrame with one location that we created earlier (however, you can also use multiple locations as origins).
# - `destinations`, which is a GeoDataFrame representing the destinations (in our case, the `points` GeoDataFrame). 
# - `departure`, which should be Python's `datetime` -object (in our case standing for "22nd of February 2022 at 08:30") to tell `r5py` that the schedules of this specific time and day should be used for doing the calculations. 
#    - *Note*: By default, `r5py` summarizes and calculates a median travel time from all possible connections within one hour from given depature time (with 1 minute frequency). It is possible to adjust this time window using `departure_time_window` -parameter ([see details here]((https://r5py.readthedocs.io/en/stable/reference.html#r5py.RegionalTask))). 
# - `transport_modes`, which determines the travel modes that will be used in the calculations. These can be passed using the options from the `r5py.TransportMode` -class. 
#   - *Hint*: To see all available options, run `help(r5py.TransportMode)`.  
# 
# ```{note} In addition to these ones, the constructor also accepts many other parameters [listed here](https://r5py.readthedocs.io/en/stable/reference.html#r5py.RegionalTask), such as walking and cycling speed, maximum trip duration, maximum number of transit connections used during the trip, etc. 
# ```
# Now, we will first create a `travel_time_matrix_computer` instance as described above:

# In[20]:


import datetime
from r5py import TravelTimeMatrixComputer, TransportMode

# Initialize the tool
travel_time_matrix_computer = TravelTimeMatrixComputer(
    transport_network,
    origins=origin,
    destinations=points,
    departure=datetime.datetime(2022,2,22,8,30),
    transport_modes=[TransportMode.TRANSIT, TransportMode.WALK]
)


# In[23]:


# To see all available transport modes, uncomment following
# help(TransportMode)


# Running this initializes the `TravelTimeMatrixComputer`, but any calculations were not done yet.
# To actually run the computations, we need to call `.compute_travel_times()` on the instance, which will calculate the travel times between all points:

# In[24]:


travel_time_matrix = travel_time_matrix_computer.compute_travel_times()
travel_time_matrix.head()


# As a result, this returns a `pandas.DataFrame` which we stored in the `travel_time_matrix` -variable. The values in the `travel_time` column are travel times in minutes between the points identified by `from_id` and `to_id`. As you can see, the `id` value in the `from_id` column is the same for all rows because we only used one origin location as input. 
# 
# To get a better sense of the results, let's create a travel time map based on our results. We can do this easily by making a table join between the `pop_grid` GeoDataFrame and the `travel_time_matrix`. The key in the `travel_time_matrix` table is the column `to_id` and the corresponding key in `pop_grid` GeoDataFrame is the column `id`. Notice that here we do the table join with the original the Polygons layer (for visualization purposes). However, the join could also be done in a similar manner with the `points` GeoDataFrame.

# In[33]:


join = pop_grid.merge(travel_time_matrix, left_on="id", right_on="to_id")
join.head()


# Now we have the travel times attached to each point, and we can easily visualize them on a map:

# In[34]:


m = join.explore("travel_time", cmap="Greens", max_zoom=13)
m = origin.explore(m=m, color="red", marker_kwds={"radius": 10})
m


# ### Compute travel time matrix from all to all locations
# 
# Running the calculations between all points in our sample dataset can be done in a similar manner as calculating the travel times from one origin to all destinations. 
# Since, calculating these kind of all-to-all travel time matrices is quite typical when doing accessibility analyses, it is actually possible to calculate a cross-product between all points just by using the `origins` parameter (i.e. without needing to specify a separate set for destinations). `r5py` will use the same points as destinations and produce a full set of origins and destinations:
# 

# In[35]:


travel_time_matrix_computer = TravelTimeMatrixComputer(
    transport_network,
    origins=points,
    departure=datetime.datetime(2022,2,22,8,30),
    transport_modes=[TransportMode.TRANSIT, TransportMode.WALK]
)
travel_time_matrix_all = travel_time_matrix_computer.compute_travel_times()
travel_time_matrix_all.head()


# In[36]:


travel_time_matrix_all.tail()


# In[37]:


len(travel_time_matrix_all)


# As we can see from the outputs above, now we have calculated travel times between all points (n=92) in the study area. Hence, the resulting DataFrame has almost 8500 rows (92x92=8464). Based on these results, we can for example calculate the median travel time to or from a certain point, which gives a good estimate of the overall accessibility of the location in relation to other points:

# In[38]:


median_times = travel_time_matrix_all.groupby("from_id")["travel_time"].median()
median_times


# To estimate, how long does it take in general to travel between locations in our study area (i.e. what is the baseline accessibility in the area), we can calculate the mean (or median) of the median travel times showing that it is approximately 22 minutes:

# In[39]:


median_times.mean()


# Naturally, we can also visualize these values on a map:

# In[42]:


overall_access = pop_grid.merge(median_times.reset_index(), left_on="id", right_on="from_id")
overall_access.head()


# In[43]:


overall_access.explore("travel_time", cmap="Blues", scheme="natural_breaks", k=4)


# In out study area, there seems to be a bit poorer accessibility in the Southern areas and on the edges of the region (i.e. we wittness a classic edge-effect here). 

# ## Advanced usage
# 
# ### Compute travel times with a detailed information about the routing results

# In case you are interested in more detailed routing results, it is possible to use `DetailedItinerariesComputer`. This will provide not only the same information as in the previous examples, but it also brings much more detailed information about the routings. When using this functionality, `r5py` produces information about the used routes for each origin-destination pair (with possibly multiple alternative routes), as well as individual trip segments and information about the used modes, public transport route-id information (e.g. bus-line number), distanes, waiting times and the actual geometry used. 
# 
# **Note:** *Computing detailed itineraries is significantly more time-consuming than calculating simple travel times. As such, think twice whether you actually need the detailed information output from this function, and how you might be able to limit the number of origins and destinations you need to compute.*

# In[47]:


from r5py import DetailedItinerariesComputer

# Take a small sample of destinations for demo purposes
points_sample = points.sample(3)

travel_time_matrix_computer = DetailedItinerariesComputer(
    transport_network,
    origins=origin,
    destinations=points_sample,
    departure=datetime.datetime(2022,2,22,8,30),
    transport_modes=[TransportMode.TRANSIT, TransportMode.WALK],
    
    # With following attempts to snap all origin and destination points to the transport network before routing
    snap_to_network=True,
)
travel_time_matrix_detailed = travel_time_matrix_computer.compute_travel_details()
travel_time_matrix_detailed.head()


# As you can see, the result contains much more information than earlier, see the following table for explanations:
# 
# | Column             | Description                                                                                             | Data type          |
# | ------------------ | --------------------------------------------------------------------------------------------------------| -------------------|
# | **from_id**        | the origin of the trip this segment belongs to                                                          | any, user defined  |
# | **to_id**          | the destination of the trip this segment belongs to                                                     | any, user defined  |
# | **option**         | sequential number for different trip options found                                                      | int                |
# | **segment**        | sequential number for segments of the current trip options                                              | int                |
# | **transport_mode** | the transport mode used on the current segment                                                          | r5py.TransportMode |
# | **departure_time** | the transit departure date and time used for current segment                                            | datetime.datetime  |
# | **distance**       | the travel distance in metres for the current segment                                                   | float              |
# | **travel_time**    | The travel time for the current segment                                                                 | datetime.timedelta |
# | **wait_time**      | The wait time between connections when using public transport                                           | datetime.timedelta |
# | **route**          | The route number or id for public transport route used on a segment                                     | str                |
# | **geometry**       | The path travelled on a current segment (with transit, stops connected with straight lines by default)  | shapely.LineString |
# 

# ### Compute travel times for different percentiles
# 
# Because `r5py` calculates travel times for all possible transit departure possibilities within an hour (with one minute frequency), we basically get a distribution of travel times. It is possible to gather and return information about the travel times at different percentiles of this distribution based on all computed trips (sorted from the fastest to slowest connections). By default, the returned time in `r5py` is the median travel time (i.e. `50`). You can access these percentiles by using a parameter `percentiles` which accepts a list of integers representing different percentiles, such as `[25, 50, 75]` which returns the travel times at those percentiles:

# In[21]:


travel_time_matrix_computer = TravelTimeMatrixComputer(
    transport_network,
    origins=origin,
    destinations=points,
    departure=datetime.datetime(2022,2,22,8,30),
    transport_modes=[TransitMode.TRANSIT, LegMode.WALK],
    percentiles=[25, 50, 75],
)
travel_time_matrix_detailed = travel_time_matrix_computer.compute_travel_times()
travel_time_matrix_detailed.head()

