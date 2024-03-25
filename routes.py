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
    
    source_1 = routes[index_1][0]
    dest_1 = routes[index_1][len(routes[index_1]) - 1]

    source_2 = routes[index_2][0]
    dest_2 = routes[index_2][len(routes[index_2]) - 1]

    # get new paths from 4d array

    # reverse either section of loop to find shorter routes "outside" the edges first
    
    # reverse edges in between
    for i in range(index_1 + 1, index_2):
        temp = nx.shortest_path(G, routes[i][len(routes[i]) - 1], routes[i][0])
        routes[i] = temp

    # find shorter path with/without edge in map using shorter outside route

    new_1 = nx.shortest_path(G, source_1, source_2, weight="travel_time_seconds")
    travel_time_1 = nx.path_weight(G, new_1, "travel_time_seconds")
    print(f"travel_time_1: {travel_time_1}")

    new_2 = nx.shortest_path(G, dest_1, dest_2, weight="travel_time_seconds")
    travel_time_2 = nx.path_weight(G, new_2, "travel_time_seconds")
    print(f"travel_time_2: {travel_time_2}")

    # check before swapping to new

    routes[index_1] = new_1
    routes[index_2] = new_2

    return routes