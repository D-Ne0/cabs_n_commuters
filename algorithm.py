from kmeans import get_distance

"""
Utilities for calculating optimal route and distance.

Bit-masking algorithm is used to calculate all possible
total distance travlled by all the cabs.
"""


def get_group_cab_distances(groups, cabs):
    """
    Finds distance between each commuter group and
    cab and store it in 2D array
    """
    all_distances = []
    for group in groups:
        d = []
        for cab in cabs:
            d.append(get_distance(group, cab))
        all_distances.append(d)
    return all_distances


def optimal_total_distance(distances, groups, cabs):
    """
    Finds total optimal distance travlled by all the cabs

    Approach used is bit-masking which takes all the ways
    to assign a cab to a group and calculates total distance
    travelled by cabs.

    Returns tuple
    """

    # Initiallizaing optimal distance negative because
    # no case has been eavaluated yet.
    optimal_distance = -1
    # Optimal route in form commuter and cab allocation
    optimal_route = []
    # Total commuter groups
    total_groups = len(groups)
    # Total cabs
    total_cabs = len(cabs)
    # Total number of ways to assign a cab to each group
    total_assignments = pow(2, total_groups*total_cabs)

    # Evaluating each way of assigning cabs to commuters
    for i in xrange(total_assignments):
        bin_repr = bin(i)[2:]
        # Reverse binary string
        bin_repr_rev = bin_repr[::-1]
        # Check if its valid bin repr
        is_valid, route = is_valid_way_to_assign_cab(
                            bin_repr_rev, total_groups,
                            total_cabs)
        if is_valid:
            total_distance = calculate_distance(distances, route)
            if (optimal_distance == -1 or
                total_distance < optimal_distance):
                optimal_distance = total_distance
                optimal_route = route

    return (optimal_distance, optimal_route)


def is_valid_way_to_assign_cab(bin_repr, total_groups, total_cabs):
    """
    Checks if this bin representation is a possible way to
    assign cabs to groups. Only condition to check is that
    each group is assigned cab only once and each cab is taken
    only once.

    Returns tuple
    """

    # Is valid way to assign cab
    is_valid = True
    # Stores which group is assgned which cab
    route = []
    # Keeps track of how many times a group is assigned cab
    group_visited = [0 for i in range(total_groups)]
    # Keeps track of how many times a cab is taken
    cab_visited = [0 for i in range(total_cabs)]
    for i,b in enumerate(bin_repr):
        # Index of the group which is assigned cab now
        group_index = i / total_cabs
        # Index of the cab which is taken now
        cab_index = i % total_cabs
        if b == '1':
            # Increment group visited
            group_visited[group_index] += 1
            # Increment cab visited
            cab_visited[cab_index] += 1
            route.append((group_index, cab_index))

    # Each group must be visited only once
    for v in group_visited:
        if v != 1:
            is_valid = False
            break

    # Each cab must be visited atmost once
    for v in cab_visited:
        if v > 1:
            is_valid = False
            break

    return (is_valid, route)


def calculate_distance(distances, route):
    """
    Finds total distance travlled by all the cabs in given route
    """

    total_distance = 0
    for r in route:
        group_index = r[0]
        cab_index = r[1]
        total_distance += distances[group_index][cab_index]

    return total_distance


def add_destination_distance(optimal_distance, groups, destination):
    """
    Adds total distance travelled from each group location to
    destination to the optimal distance.
    """

    if optimal_distance == -1:
        return optimal_distance

    total_distance = 0
    for g in groups:
        total_distance += get_distance(g, destination)

    optimal_distance += total_distance

    return optimal_distance

