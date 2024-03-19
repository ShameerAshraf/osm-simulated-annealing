import pyrosm
import os
import matplotlib.pyplot as plt
import osmnx as ox
import networkx as nx

dir_path = os.path.dirname(os.path.realpath(__file__))
TARGET_FILE = "mini-Toronto.osm.pbf"

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
G = osm.to_graph(nodes, edges, graph_type="networkx")

#import pdb
#pdb.set_trace()

random_points = ox.utils_geo.sample_points(G, 10)
random_node_ids = ox.distance.nearest_nodes(G, random_points.x.values, random_points.y.values)

routes = []
for i in range(0, len(random_node_ids) - 1):
    route = nx.shortest_path(G, random_node_ids[i], random_node_ids[i+1], weight='weight')
    routes.append(route)

route = nx.shortest_path(G, random_node_ids[len(random_node_ids) - 1], random_node_ids[0], weight='weight')
routes.append(route)

fig, ax = ox.plot_graph_routes(G, routes, route_colors=["r", "g", "b", "r", "g", "b", "r", "g", "b", "r"], route_linewidth=6, node_size=0, orig_dest_size=3)


#ox.plot_graph(G)

## main file, open map, plot functions for everything in other file