#class used to interact with bus routes in nyc

import networkx as nx
import osmnx as ox
import json
import os
from dotenv import load_dotenv

load_dotenv()

MTA_API_KEY = os.getenv('MTA_API_KEY')
GRAPHML_PATH = os.getenv('GRAPHML_PATH')
ROUTE_LISTS_PATH = os.getenv('ROUTE_LISTS_PATH')
BUS_STOP_INFO_PATH = os.getenv('BUS_STOP_INFO_PATH')

class BusMap:

    def __init__(self):
        self.graph = ox.io.load_graphml(filepath=GRAPHML_PATH)

        with open(ROUTE_LISTS_PATH) as json_file:
            self.route_lists = json.load(json_file)

        with open(BUS_STOP_INFO_PATH) as json_file:
            self.bus_stop_info = json.load(json_file)


    def load_routes(self, route_lists):
        """
        store items in route list as dictionary of multidigraphs
        """

        self.routes = {}

        #iterate through each route in route_lists
    
    def load_route(self, route_list, route_name): 
        """
        loads an individual route to data
        """
        for stop in route_list:
            # add route name to stop info
            self.bus_stop_info[stop]['diroutes'] = self.bus_stop_info[stop].get('diroutes', []) + [route_name]
            print(f"{route_name} added to stop {stop}")



myMap = BusMap()

print(myMap.routes)



