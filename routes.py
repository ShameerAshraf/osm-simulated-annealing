import networkx as nx

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

# do the math
def p_accept_new(t1, t2):
    if t1 > t2:
        return True
    else:
        return False

# swap edges in route, check if total length has decreased
def swap_if_less(G, routes, index_1, index_2, total_travel_time):

    print(f"Old Total Travel Time: {total_travel_time}")

    # create copy of routes to modify and check new travel times
    new_routes = list(routes)
    
    source_1 = new_routes[index_1][0]
    dest_1 = new_routes[index_1][len(new_routes[index_1]) - 1]

    source_2 = new_routes[index_2][0]
    dest_2 = new_routes[index_2][len(new_routes[index_2]) - 1]

    # get new paths from 4d array??

    # todo: reverse either section of loop to find shorter routes "outside" the edges first
    # reverse edges in between
    new_pos = 0
    for i in range(index_1 + 1, index_2):
        temp = nx.shortest_path(G, routes[i][len(routes[i]) - 1], routes[i][0])
        travel_time = nx.path_weight(G, temp, "travel_time_seconds")
        print(f"travel_time_{i}: {travel_time}")
        new_routes[index_2 - 1 - new_pos] = temp
        new_pos += 1

    new_1 = nx.shortest_path(G, source_1, source_2, weight="travel_time_seconds")
    travel_time_1 = nx.path_weight(G, new_1, "travel_time_seconds")
    print(f"travel_time_{index_1}: {travel_time_1}")

    new_2 = nx.shortest_path(G, dest_1, dest_2, weight="travel_time_seconds")
    travel_time_2 = nx.path_weight(G, new_2, "travel_time_seconds")
    print(f"travel_time_{index_2}: {travel_time_2}")

    new_routes[index_1] = new_1
    new_routes[index_2] = new_2

    # check travel time of new_routes
    new_total_travel_time = 0
    for j in range(0, len(new_routes)):
        travel_time = nx.path_weight(G, new_routes[j], "travel_time_seconds")
        print(f"travel_time_{j}: {travel_time}")
        new_total_travel_time += travel_time

    print(f"New Total Travel Time: {new_total_travel_time}")

    # todo: work on function to check if route should be modified
    modifying_route = p_accept_new(total_travel_time, new_total_travel_time)

    if modifying_route:
        return new_routes, new_total_travel_time, modifying_route

    return routes, total_travel_time, False