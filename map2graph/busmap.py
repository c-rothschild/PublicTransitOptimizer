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

MTA_API_KEY = os.getenv('MTA_API_KEY')
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


    def load_routes(self):
        """
        adds route name(s) to bus stop dict
        """

        self.routes = {}

        #iterate through each route in route_lists
        for route_name in self.route_lists.keys():
            for stop in self.route_lists[route_name]:
                self.bus_stop_info[stop]['diroutes'] = self.bus_stop_info[stop].get('diroutes', []) + [route_name]
                self.bus_stop_info[stop]['diroutes'] = list(set(self.bus_stop_info[stop]['diroutes'] ))

        filename = BUS_STOP_INFO_PATH
        with open(filename, 'w') as file:
            json.dump(self.bus_stop_info, file, indent=4)



    def plot_route(self, route_name):
        '''
        plot a given bus route on a map
        find the route name you would like to plot by searching through all_route_lists.json or self.routes
        '''
        route_list = self.route_lists[route_name]
        osmid_list = list(map(lambda x: self.bus_stop_info[x]['osmid'], route_list))
        ox.plot.plot_graph_route(self.G, osmid_list)
    
            


if __name__ == "__main__":
    myMap = BusMap()
    myMap.plot_route('M101 - LIMITED EAST VILLAGE 3 AV-6 ST via LEX')
    
    
    
