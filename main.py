import pyrosm
import os
import matplotlib.pyplot as plt
import osmnx as ox
import networkx as nx
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
TARGET_FILE = "micro-Toronto.osm.pbf"

print(os.path.join(dir_path, TARGET_FILE))


# Get filepath to test PBF dataset
#fp = pyrosm.get_data(TARGET_FILE)
#print("Filepath to test data:", fp)

# Initialize the OSM object 
osm = pyrosm.OSM(TARGET_FILE)

# See the type
#print("Type of 'osm' instance: ", type(osm))

#drive_net.plot()
#plt.show()


nodes, edges = osm.get_network(network_type="driving", nodes=True)

# implement better speed adjustment and time calc
edges['maxspeed'] = ['50' if item == None else item for item in edges.maxspeed]
edges['travel_time_seconds'] = [(200 - float(item)) for item in edges.maxspeed]

#for e in edges:
#    if edges["maxspeed"] is None:
#        edges["maxspeed"] = 50
#    edges["maxspeed"] = edges["maxspeed"].astype(float).astype(pd.Int64Dtype())



G = osm.to_graph(nodes, edges, graph_type="networkx")

# make truly random at some point (pun intended)
random_points = ox.utils_geo.sample_points(G, 10)
random_node_ids = ox.distance.nearest_nodes(G, random_points.x.values, random_points.y.values)

# generate routes to/from all points? 2d array
# 

routes = []
travel_time_routes = []

for i in range(0, len(random_node_ids) - 1):
    print(f"########################## ROUTE {i} ###############")
    route = nx.shortest_path(G, random_node_ids[i], random_node_ids[i+1], weight="travel_time_seconds")
    for j in range(0, len(route) - 1):
        # sum up travel_time_seconds for the route
        e = G.get_edge_data(route[j], route[j+1])
        for item in e: print(str(e[item]['maxspeed']) + "--" + str(e[item]['travel_time_seconds']))
    # store travel_time_seconds for routes
    routes.append(route)
    #travel_time_routes.append()

route = nx.shortest_path(G, random_node_ids[len(random_node_ids) - 1], random_node_ids[0], weight="travel_time_seconds")
routes.append(route)

fig, ax = ox.plot_graph_routes(G, routes, route_colors=["r", "g", "b", "r", "g", "b", "r", "g", "b", "r"], route_linewidth=6, node_size=0, orig_dest_size=3)



#ox.plot_graph(G)

## main file, open map, plot functions for everything in other file