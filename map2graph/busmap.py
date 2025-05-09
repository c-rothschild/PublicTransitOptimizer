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


    def set_route_node_lists(self, file_path=False):
        self.route_node_lists = {}
        for name, route_list in tqdm(self.route_lists.items(), desc="Processing dictionary"):
            self.route_node_lists[name] = self.get_route_node_list(route_list) 
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.route_node_lists, file, indent=4)


    def get_route_node_list(self, route_list):
        osmid_list = list(map(lambda x: self.bus_stop_info[x]['osmid'], route_list))
        full_route = []
        for i in range(1, len(osmid_list)):
            path = ox.routing.shortest_path(self.G, osmid_list[i - 1], osmid_list[i])

            if not path:
                print(f'error: {(osmid_list[i - 1], osmid_list[i])}')
            else:
                full_route.extend(path[1:])
        return full_route



    def plot_route(self, route_name):
        route_list = self.route_lists[route_name]
        osmid_list = list(map(lambda x: self.bus_stop_info[x]['osmid'], route_list))
        print(osmid_list)
        ox.plot.plot_graph_route(self.G, osmid_list)
    
    def load_route_node_lists(self, file_path):
        with open(file_path) as json_file:
            self.route_node_lists = json.load(json_file)
            


if __name__ == "__main__":
    myMap = BusMap()
    myMap.load_route_node_lists('map2graph/graph_data/route_node_lists.json')
    #ox.plot.plot_graph_route(myMap.G, list(myMap.route_node_lists.values())[0])
    print(myMap.G.get_edge_data(42430633,3270031002))
    
    
    
