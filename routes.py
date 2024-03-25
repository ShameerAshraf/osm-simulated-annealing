import networkx as nx

# generate random points, get nearest nodes

# getting routes between source-target

# adding speedlimits
def road_class_to_kmph(road_class):
    """
    Returns a speed limit value based on road class, 
    using typical Finnish speed limit values within urban regions.
    """
    if road_class == "motorway":
        return 100
    elif road_class == "motorway_link":
        return 80
    elif road_class in ["trunk", "trunk_link"]:
        return 60
    elif road_class == "service":
        return 30
    elif road_class == "living_street":
        return 20
    else:
        return 50

# swap edges in route, check if total length has decreased
def swap_if_less(G, routes, index_1, index_2, total_travel_time):

    print(f"Old Total Travel Time: {total_travel_time}")

    # create copy of routes to modify and check new travel times
    new_routes = list(routes)
    
    source_1 = new_routes[index_1][0]
    dest_1 = new_routes[index_1][len(new_routes[index_1]) - 1]

    source_2 = new_routes[index_2][0]
    dest_2 = new_routes[index_2][len(new_routes[index_2]) - 1]

    # get new paths from 4d array

    # reverse either section of loop to find shorter routes "outside" the edges first
    
    # reverse edges in between
    for i in range(index_1 + 1, index_2):
        temp = nx.shortest_path(G, new_routes[i][len(new_routes[i]) - 1], new_routes[i][0])
        travel_time = nx.path_weight(G, temp, "travel_time_seconds")
        print(f"travel_time_{i}: {travel_time}")
        new_routes[i] = temp

    # find shorter path with/without edge in map using shorter outside route

    new_1 = nx.shortest_path(G, source_1, source_2, weight="travel_time_seconds")
    travel_time_1 = nx.path_weight(G, new_1, "travel_time_seconds")
    print(f"travel_time_{index_1}: {travel_time_1}")

    new_2 = nx.shortest_path(G, dest_1, dest_2, weight="travel_time_seconds")
    travel_time_2 = nx.path_weight(G, new_2, "travel_time_seconds")
    print(f"travel_time_{index_2}: {travel_time_2}")

    # check travel time of new_routes 

    new_routes[index_1] = new_1
    new_routes[index_2] = new_2

    new_total_travel_time = 0
    for j in range(0, len(new_routes)):
        travel_time = nx.path_weight(G, new_routes[j], "travel_time_seconds")
        print(f"travel_time_{j}: {travel_time}")
        new_total_travel_time += travel_time

    print(f"New Total Travel Time: {new_total_travel_time}")

    # work on function to check if route should be modified
    modifying_route = new_total_travel_time < total_travel_time

    if modifying_route:
        return new_routes, new_total_travel_time, modifying_route

    return routes, total_travel_time, False