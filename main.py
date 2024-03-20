import pyrosm
import os
import matplotlib.pyplot as plt
import osmnx as ox
import networkx as nx
import pandas as pd

from multiprocessing import Process

from routes import road_class_to_kmph

from pdb import set_trace as qwe

def plot_async(G, routes):
    fig, ax = ox.plot_graph_routes(G, routes, route_colors=["r", "g", "b", "r", "g", "b", "r", "g", "b", "r"], route_linewidth=6, node_size=0)

def main():
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

    # Parse roads that can be driven by car
    #roads = osm.get_network(network_type="driving")
    #roads.plot(figsize=(10,10))


    nodes, edges = osm.get_network(network_type="driving", nodes=True)

    # Plot the data
    #ax = edges.plot(figsize=(10,10), color="gray", lw=1.0)
    #ax = nodes.plot(ax=ax, color="red", markersize=2)

    # Zoom in to take a closer look
    #ax.set_xlim([24.9375, 24.945])
    #ax.set_ylim([60.17, 60.173])

    # implement better speed adjustment and time calc
    #edges['maxspeed'] = ['50' if item == None else item for item in edges.maxspeed]
    #edges['travel_time_seconds'] = [(200 - float(item)) for item in edges.maxspeed]

    # Separate rows with / without speed limit information 
    mask = edges["maxspeed"].isnull()
    edges_without_maxspeed = edges.loc[mask].copy()
    edges_with_maxspeed = edges.loc[~mask].copy()

    # Apply the function and update the maxspeed
    edges_without_maxspeed["maxspeed"] = edges_without_maxspeed["highway"].apply(road_class_to_kmph)
    #edges_without_maxspeed.head(5).loc[:, ["maxspeed", "highway"]]

    # merge with/without speed
    edges = pd.concat([edges_with_maxspeed, edges_without_maxspeed])
    edges["maxspeed"] = edges["maxspeed"].astype(int)

    #visualize maxspeed on map
    #ax = edges.plot(column="maxspeed", figsize=(10,10), legend=True)

    # assign travel time for edges
    edges["travel_time_seconds"] = edges["length"] / (edges["maxspeed"]/3.6)

    # create G
    G = osm.to_graph(nodes, edges, graph_type="networkx")

    random_points = ox.utils_geo.sample_points(G, 10)
    random_node_ids = ox.distance.nearest_nodes(G, random_points.x.values, random_points.y.values)

    # generate routes to/from all points? 2d array
    # 

    routes = []
    travel_time_routes = []

    for i in range(0, len(random_node_ids) - 1):
        print(f"########################## ROUTE {i} ###############")
        route = nx.shortest_path(G, random_node_ids[i], random_node_ids[i+1], weight="travel_time_seconds")

        # sum up travel_time_seconds for the route
        travel_time = nx.path_weight(G, route, "travel_time_seconds")
        print("TRAVEL TIME " + str(travel_time))

        #for j in range(0, len(route) - 1):
            # sum up travel_time_seconds for the route
            #print(nx.path_weight(G, route, "travel_time_seconds"))
            #e = G.get_edge_data(route[j], route[j+1])
            #for item in e: print(str(e[item]['maxspeed']) + "--" + str(e[item]['travel_time_seconds']))

        # store routes and corresponding travel_time_seconds for routes
        routes.append(route)
        travel_time_routes.append(travel_time)

    route = nx.shortest_path(G, random_node_ids[len(random_node_ids) - 1], random_node_ids[0], weight="travel_time_seconds")
    travel_time = nx.path_weight(G, route, "travel_time_seconds")
    routes.append(route)
    travel_time_routes.append(travel_time)

    #fig, ax = ox.plot_graph_routes(G, routes, route_colors=["r", "g", "b", "r", "g", "b", "r", "g", "b", "r"], route_linewidth=6, node_size=0)

    #draw async
    draw = Process(target=plot_async, args=(G, routes))
    draw.start()

    qwe()

    draw.join()
    #ox.plot_graph(G)

    ## main file, open map, plot functions for everything in other file

if __name__ == '__main__':
    main()