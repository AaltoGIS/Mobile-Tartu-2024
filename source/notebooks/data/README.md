# Data

Details about the bundled datasets.


## Helsinki

###  Helsinki_25April.osm.pbf
A sample dataset of central Helsinki region representing OpenStreetMap data in protocolbuffer binary format (PBF),
which was obtained from [Geofabrik](https://download.geofabrik.de/europe/finland.html).
The data is licensed under the [Open Data Commons Open Database License (ODbL)](https://www.openstreetmap.org/copyright).

### `GTFS.zip`

General Transit Feed Specification ([GTFS](https://developers.google.com/transit/gtfs/reference))
data representing the public transport schedules, stop locations, lines, etc.
The data was created by Helsinki Region Transport (HLS) and obtained from
[TransitFeeds.com](https://transitfeeds.com/p/helsinki-regional-transport/735).

This GTFS data set is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).


### `kantakaupunki.osm.pbf`

A sample dataset representing OpenStreetMap data in protocolbuffer binary format (PBF),
which was obtained from [Geofabrik](https://download.geofabrik.de/europe/finland.html).
The data is licensed under the [Open Data Commons Open Database License (ODbL)](https://www.openstreetmap.org/copyright).

We used [osmium](https://osmcode.org/osmium-tool/) to crop the data to the given extent.


### `population_points_2020.gpkg`, `population_grid_2020.gpkg`

A sample dataset representing the population of Helsinki.
The data is obtained from Helsinki Region Environmental Services (HSY).
The data is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The data is downloaded from the Helsinki Region Environmental Services’ (HSY)
*Web Feature Service (WFS)* endpoint (see the
[Helsinki Region Infoshare’s data description](https://hri.fi/data/en_GB/dataset/vaestotietoruudukko)).
We used [a script](scripts/download_population_grid.py), that we share with this package, to download
the data set and adapt it to the requirements of r5py’s documentation. Namely, we:

- reindexed the data,
- omitted some columns,
- renamed the remaining columns from Finnish to English
- reprojected the data to "EPSG:4326", and
- extracted centroids from the grid polygons (for the point data set)


## São Paulo

### `spo_gtfs.zip`

General Transit Feed Specification ([GTFS](https://developers.google.com/transit/gtfs/reference))
data representing the public transport schedules, stop locations, lines, etc.

In contrast to the GTFS data set for Helsinki, the São Paulo data also has schedules expressed
in frequencies rather than fixed departure times.

[This data set has been published by São Paulo Transporte S/A, the public transport company of the
city of São Paulo for open use, but without a specific license specified.](https://www.sptrans.com.br/desenvolvedores)


### `spo_osm.pbf`

A sample dataset representing OpenStreetMap data in protocolbuffer binary format (PBF),
which was obtained from [Geofabrik](https://download.geofabrik.de/europe/finland.html).
The data is licensed under the [Open Data Commons Open Database License (ODbL)](https://www.openstreetmap.org/copyright).


### `spo_hexgrid.csv`

A regular, hexagonally distributed, point grid data set over the extent of São Paulo, created by
the authors of [r5r](https://github.com/ipeaGIT/r5r/tree/master/r-package/inst/extdata/spo). This data
set is used in some of the tests.

# About the "LCA_gCO2_per_pkm_by_transport_mode.csv" CSV-file

The CSV file consists of GHG emissions per passenger-kilometer (g CO<sub>2</sub>/pkm) by transport modes derived from the mentioned LCA tool by ITF. The columns represent the different transport modes and the rows represent the GHG emissions. The GHG emissions of the transport modes have been divided into four separate components: vehicle component, fuel component, infrastructure component and operational services. The explanations of the acronyms (in the transport modes names) are: BEV = battery electric vehicle; HEV = hybrid electric vehicle; ICE = internal combustion engine; FCEV = fuel cell electric vehicle; PHEV = plug-in hybrid electric vehicle. 