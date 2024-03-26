import pyrosm
import os
import matplotlib.pyplot as plt
import osmnx as ox
import networkx as nx
import pandas as pd
import random

from multiprocessing import Process

from routes import road_class_to_kmph, swap_if_less
from plotting import create_roc, create_roc_swapped

POINTS_IN_ROUTE = 15

def route_verifier(routes):
    for i in range(0, len(routes) - 1):
        if routes[i][len(routes[i]) - 1] != routes[i+1][0]:
            print(f"Error in comparing {i} and {i+1}")
            return False

    if routes[len(routes) - 1][len(routes[len(routes) - 1]) - 1] != routes[0][0]:
            print(f"Error in comparing last and first")
            return False

    return True
        

def plot_async(G, routes, route_colors, iteration, travel_time):
    fig, ax = ox.plot_graph_routes(G, routes, 
    route_colors=route_colors, 
    route_linewidth=6, node_size=0,
    show=False, close=False)

    fig.suptitle(f"Iteration {iteration}")
    ax.set_title(f"Travel time: {travel_time} seconds")
    plt.show()


def main():
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

    # generate random points, get nearest nodes
    random_points = ox.utils_geo.sample_points(G, POINTS_IN_ROUTE)
    random_node_ids = ox.distance.nearest_nodes(G, random_points.x.values, random_points.y.values)

    # generate routes to/from all points? 4d array????
    # paths[source][destination] = route[nodes]

    routes = []
    total_travel_time = 0

    for i in range(0, len(random_node_ids) - 1):
        print(f"############### ROUTE {i} ###############")
        route = nx.shortest_path(G, random_node_ids[i], random_node_ids[i+1], weight="travel_time_seconds")

        # sum up travel_time_seconds for the route
        travel_time = nx.path_weight(G, route, "travel_time_seconds")
        print("####### TRAVEL TIME " + str(travel_time) + " #######")

        # store routes and corresponding travel_time_seconds for routes
        routes.append(route)
        total_travel_time += travel_time

    route = nx.shortest_path(G, random_node_ids[len(random_node_ids) - 1], random_node_ids[0], weight="travel_time_seconds")
    travel_time = nx.path_weight(G, route, "travel_time_seconds")
    print(f"############### ROUTE {len(random_node_ids) - 1} ###############")
    print("####### TRAVEL TIME " + str(travel_time) + " #######")
    routes.append(route)
    total_travel_time += travel_time
    print("####### TOTAL TRAVEL TIME FOR ORIGINAL ROUTE " + str(total_travel_time) + " #######")

    #fig, ax = ox.plot_graph_routes(G, routes, route_colors=["r", "g", "b", "r", "g", "b", "r", "g", "b", "r"], route_linewidth=6, node_size=0)

    route_colors = create_roc(POINTS_IN_ROUTE)

    # draw base graph
    draw = Process(target=plot_async, args=(G, routes, route_colors, 0, total_travel_time))
    draw.start()


    for iteration in range(1, 201):

        # run one step of SA based on user input
        #in_string = input("Enter any string to continue OR quit to quit\n")
        #if in_string == "quit":
        #    break
        #else:
        #    print("Step in simulated annealing")
        
        # generate random indexes, store bigger index in index_2
        # call if Math.abs(index2 - index1) > 1

        index_1 = random.randrange(10)
        index_2 = random.randrange(10)

        if abs(index_2 - index_1) > 1:
            if index_1 > index_2:
                index_1, index_2 = index_2, index_1

            routes, total_travel_time, changed = swap_if_less(G, routes, index_1, index_2, total_travel_time)

            if changed and iteration > 180:
                route_colors = create_roc_swapped(POINTS_IN_ROUTE, index_1, index_2)
                
                # draw async
                draw = Process(target=plot_async, args=(G, routes, route_colors, iteration, total_travel_time))
                draw.start()
            #else:
            #    route_colors=["r", "g", "b", "r", "g", "b", "r", "g", "b", "r", "g", "b", "r", "g", "b", "r", "g", "b", "r", "g"]

            elif (iteration % 20) == 0:
                #draw async
                route_colors = create_roc(POINTS_IN_ROUTE)
                draw = Process(target=plot_async, args=(G, routes, route_colors, iteration, total_travel_time))
                draw.start()


    print("\n ### CLOSE ALL GRAPH WINDOWS ###\n")
    draw.join()

    #ox.plot_graph(G)

if __name__ == '__main__':
    main()