# Public Transit Optimizer + Simulator

## map2graph/graph_data/

### stations.graphml - NYC bus stops stored in on a MultiDigraph
Usage:
> import osmnx as ox
> path = 'path/to/stations.graphml'
> G = ox.io.load_graphml()

This will load a multidigraph containing nodes representing NYC streets. Some nodes will have a 'bus_stops' attribute, containing the list of each bus stop id near that node. Some edges going from one bus stop to another will have a 'travel_time' attribute, containing the amount of seconds it takes to get from one bus stop to the next

### bus_info_dict.json - a json file containing a dictionary of each stopId and information associated with it
Usage:
> import json
> path = 'path/to/bus_info_dict.json'
> with open(path) as json_file
>   bus_info_dict = json.load(json_file)

This will load a dictionary containing stopIds as keys and information associated with that stop id. Most importantly, bus_info_dict[stopId]['osmid'] stores the osmid containing the specified stop. 

### all_route_lists.json - a json file containing a dictionary of all routes
Usage:
> import json
> path = 'path/to/all_route_lists.json'
> with open(path) as json_file
>   all_route_lists.json = json.load(json_file)

This will load a dictionary containing route names as keys and a list of stopIds as values. The list of stopIds are in order. 

## map2graph/busmap.py - contains the BusMap class

create a .env file with the following format:

  DATA_PATH='path/to/graph_data/'
  GRAPHML_PATH=${DATA_PATH}stations.graphml
  ROUTE_LISTS_PATH=${DATA_PATH}all_route_lists.json
  BUS_STOP_INFO_PATH=${DATA_PATH}bus_info_dict.json

Usage: 
> from busmap import BusMap
> myMap = BusMap()

### BusMap.plot_routes(route_names)

Params: 
  route_names - the list of route names you want to plot

Usage:
> myMap.plot_routes(["Q28 - BAY TERRACE BELL BL", "Q28 - FLUSHING MAIN ST STATION"])

displays a matplotlib showing each listed route on an NYC map

### BusMap.get_travel_time(route_name, startId, stopId)

Params:
  route_name - the name of the route where the stops exist
  startId - the stopId of the first stop in the route
  stopId - the stopId of the last stop in the route

Usage:
> myMap.get_travel_time("Q26 - FRESH MEADOWS HOLLIS COURT BL via 46 AV","MTA_504994", "MTA_502762")

Returns:
  the amount of seconds it takes to travel between the two inputted nodes


## Tripsim.py 
NEEDS TO CHANGE PATH BASED ON MACHINE
GRAPHML_PATH = "/PublicTransitOptimizer/map2graph/graph_data/stations.graphml"
ROUTE_LISTS_PATH = "/PublicTransitOptimizer/map2graph/graph_data/all_route_lists.json"
BUS_STOP_INFO_PATH = "/PublicTransitOptimizer/map2graph/graph_data/bus_info_dict.json"

### visualizetrip
Params:
  G - the Graph of New York
  routelists - From Route Lists (data from all_route_lists.json)
  busstopinfo - From Bus Stop info (data from bus_info_dict.json)
  routename - Name of route being used
  startstopid - ID of stop
  endstopid - ID of stop

Usage:
>visualizetrip(G, routelists, busstopinfo, routename, startid, targetid)
>#route = input("What route do you want to take")
 #start = input("What stop are you at?")
 #target = input("Where do you wanna go?")
>Then transfer to ids, the the function can make sense of them

Returns:
An text describing an error, displays a matplotlib graph that shows the map of all bus nodes in ny, with the routes.

### testOutMapv3.ipynb
DO NOT CHANGE busmap.py, THIS FUNCTION IMPLEMENTS busmap.py
## Purpose
If you run all blocks except for block multi-threading, it should print out 
the min,max amount of walking time and traveling time.
By that, we could judge whether or not will there be people mad about what the public transport
we have described previously.

## FinalProject307
Note Takes a long time to run
Usage:
>Test Max Flow for different examples of public transportation in NYC

