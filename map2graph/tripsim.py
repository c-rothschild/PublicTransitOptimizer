import networkx as nx
import osmnx as ox
import json
import matplotlib.pyplot as plt
import random

GRAPHML_PATH = "/PublicTransitOptimizer/map2graph/graph_data/stations.graphml"
ROUTE_LISTS_PATH = "/PublicTransitOptimizer/map2graph/graph_data/all_route_lists.json"
BUS_STOP_INFO_PATH = "/PublicTransitOptimizer/map2graph/graph_data/bus_info_dict.json"


def visualizetrip(G,routelists,busstopinfo,routename,startstopid,endstopid):

    if routename not in routelists:
        return "route is not a route "

    routestopids = routelists[routename]
    if startstopid == endstopid:
        return "no"
    if startstopid not in routestopids:
        return "start node is not in route"
    if endstopid not in routestopids:
        return "end node is not in the route"

    startnode = busstopinfo[startstopid]['osmid']
    endnode = busstopinfo[endstopid]['osmid']

    routenodeids = []
    for stopid in routestopids:
        routenodeids.append(busstopinfo[stopid]['osmid'])


    routenodesset = set(routenodeids)
    subgraph = G.subgraph(routenodesset)

    try:
        pathnodes = nx.dijkstra_path(subgraph, source=startnode, target=endnode, weight='traveltime')
    except nx.NetworkXNoPath:
        return "nopaths found"

    fig, ax = plt.subplots()

    ox.plot_graph(G, node_color='#808080',show=False, close=False, node_size=5, ax=ax)

    routenodes = []
    routex = []
    routey = []
    for nodeid in pathnodes:
        routenodes.append(G.nodes[nodeid]) 
    
    for node in routenodes:
        routex.append(node['x'])
        routey.append(node['y'])
    ax.plot(routex, routey, color='red', linewidth=3)

    ax.plot(G.nodes[startnode]['x'], G.nodes[startnode]['y'],'go')
    ax.plot(G.nodes[endnode]['x'], G.nodes[endnode]['y'],'ro')

    ax.set_axis_off()
    traveltime = calculatetraveltime(G, routelists[routename], busstopinfo, startstopid, endstopid)
    traveltime /= 60
    plt.title(str(busstopinfo[startstopid]['name'])+" to "+str(busstopinfo[endstopid]['name'])+ 
              " will likely take "+str(round(traveltime))+" minutes", fontdict={'fontsize': 8})
    plt.show()

def calculatetraveltime(G,route,busstopinfo,startId,stopId):
    startindex = route.index(startId)
    traveltime = 0

    for idx in range(startindex + 1, len(route)):
        prevosmid = busstopinfo[route[idx - 1]]['osmid']
        curosmid = busstopinfo[route[idx]]['osmid']
        traveltime += G.edges[(prevosmid, curosmid, 0)]['travel_time']
        if (route[idx] == stopId):
            return traveltime

    raise KeyError(f'Stop {stopId} not found in route')

G = ox.io.load_graphml(GRAPHML_PATH)
with open(ROUTE_LISTS_PATH) as f:
    routelists = json.load(f)
with open(BUS_STOP_INFO_PATH) as f:
    busstopinfo = json.load(f)

#Random Usage to see some routes end to end
#routename = random.choice(list(routelists.keys()))
#startid = routelists[routename][0]
#targetid = routelists[routename][len(routelists[routename])-1]

#routename = "M15 - EAST HARLEM 125 ST via 1 AV"
#startid = "MTA_405083"
#targetid = "MTA_401731"

routename = input("What route do you want to take? ")
startname = input("What stop are you at? ")
targetname = input("Where do you want to go? ")
startid = None
targetid = None

busstopitems = busstopinfo.items()

for item in busstopitems:
    stopid = item[0]
    stopdata = item[1]
    if stopdata['name'] == startname:
        startid = stopid
        break

for item in busstopitems:
    tarid = item[0]
    stopdata = item[1]
    if stopdata['name'] == targetname:
        targetid = tarid
        break

if startid is None:
    print("Start stop  not found.")
    exit()
if targetid is None:
    print("Target stop  not found.")
    exit()

visualizetrip(G, routelists, busstopinfo, routename, startid, targetid)
