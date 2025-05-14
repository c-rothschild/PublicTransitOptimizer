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
    
    def stopIds_to_nodes(self, stop_id_list):
        return list(map(lambda x: self.bus_stop_info[x]['osmid'], stop_id_list))
    
    def get_route_stopIds(self, route_name):
        return self.route_lists[route_name]
    
    def get_all_stops(self):
        return list(self.route_lists.keys())
    
    def set_stop_subgraph(self):
        ''' 
        create a subgraph comprised only of bus stations
        '''
        all_routes = self.get_all_stops()
        all_stop_nodes =  []

        for route in all_routes:
            stopIds = self.get_route_stopIds(route)
            all_stop_nodes.extend(self.stopIds_to_nodes(stopIds))
        
        self.stop_subgraph = self.G.subgraph(all_stop_nodes)

            


if __name__ == "__main__":
    # sample usage:
    myMap = BusMap()

    all_routes = myMap.get_all_stops()
    stops = myMap.get_route_stopIds(all_routes[0])
    myMap.set_stop_subgraph()

    path = nx.dijkstra_path(myMap.stop_subgraph,42973027,42736818, weight='travel_time')
    
    # ox.plot.plot_graph_route(myMap.G, path)
    
    print(myMap.stopIds_to_nodes(stops))



    myMap.plot_routes(route_names=all_routes)
    
    
    
