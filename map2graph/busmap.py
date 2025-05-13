#class used to interact with bus routes in nyc

import networkx as nx
import osmnx as ox
import json
import os
from dotenv import load_dotenv
import asyncio
import aiohttp
from tqdm import tqdm
import geopandas as gpd

load_dotenv()

# MTA_API_KEY = os.getenv('MTA_API_KEY')
GRAPHML_PATH = os.getenv('GRAPHML_PATH')
ROUTE_LISTS_PATH = os.getenv('ROUTE_LISTS_PATH')
BUS_STOP_INFO_PATH = os.getenv('BUS_STOP_INFO_PATH')


class BusMap:

    def __init__(self):
        self.G = ox.io.load_graphml(GRAPHML_PATH)

        with open(ROUTE_LISTS_PATH) as json_file:
            self.route_lists = json.load(json_file)

        with open(BUS_STOP_INFO_PATH) as json_file:
            self.bus_stop_info = json.load(json_file)

    def plot_routes(self, route_names):
        '''
        plot a list of given bus routes on a map
        find the route name you would like to plot by searching through all_route_lists.json or self.routes
        '''
        routes = []
        for route_name in route_names:
            route_list = self.route_lists[route_name]
            node_list = list(map(lambda x: self.bus_stop_info[x]['osmid'], route_list))
            # ignore empty routes
            if len(node_list) == 0:
                continue
            routes.append(node_list)
        ox.plot.plot_graph_routes(self.G, routes)
    
    def get_travel_time(self, route_name, startId, stopId):
        ''' 
        get travel time between two stops
        '''
        route = self.route_lists[route_name]
        startIdx = route.index(startId)

        travel_time = 0

        for idx in range(startIdx + 1, len(route)):
            prevosmid = self.bus_stop_info[route[idx -1]]['osmid']
            curosmid = self.bus_stop_info[route[idx]]['osmid']
            travel_time += myMap.G.edges[(prevosmid, curosmid, 0)]['travel_time']
            if(route[idx] == stopId):
                return travel_time
            
        raise KeyError(f'Stop {stopId} not found in route')

    
            


if __name__ == "__main__":
    myMap = BusMap()
    all_routes = list(myMap.route_lists.keys())
    print(myMap.get_travel_time("Q26 - FRESH MEADOWS HOLLIS COURT BL via 46 AV","MTA_504994", "MTA_502762"))
    #myMap.plot_routes(route_names=all_routes[:20])
    
    
    
