import sys

from errors import ERR_INPUT_FILE_NOT_FOUND
from errors import ERR_INPUT_FILE_EMPTY
from errors import ERR_COMMUTERS_CABS_STR
from errors import ERR_LESS_COMMUTER_LOCATIONS
from errors import ERR_LESS_CAB_LOCATIONS
from errors import ERR_MISSING_DEST_LOCATION
from kmeans import Point, kmeans, get_distance

"""
Write a utility that takes as input the location of m commuters and n cabs and
a destination location, and outputs optimised cab routes for picking up all
commuters (on a shared basis) and dropping them off at the destination.
"""

# Sample input file
# Change the number in the end to test with a new sample file
SAMPLE_INPUT_FILE = 'sample_input_0.txt'

class Commuter(Point):
    """
    Commuter location class
    """

    def __init__(self, coords):
        """
        coords - tuple of values i.e (x,y)
        """

        super(Commuter, self).__init__(coords)


class Cab(Point):
    """
    Cab location class
    """

    def __init__(self, coords):
        """
        coords - tuple of values i.e (x,y)
        """

        super(Cab, self).__init__(coords)


def main():

    # Input file that contains the input for
    # commuters, cabs and destination location
    input_file = "sample_inputs/%s" % SAMPLE_INPUT_FILE

    if len(sys.argv) == 2:
        input_file = sys.argv[1]

    # Parse input file
    commuters, cabs, destination = parse_input_file(input_file)
    # Create clusters of commuters
    clusters = kmeans(commuters, cabs)
    # Centroid of each cluster represents virtual centre of
    # each commuter group
    groups = [c.centroid for c in clusters]
    # Find distance between each commuter group and cab
    all_distances = get_group_cab_distances(groups, cabs)
    # Find optimal total distance and route travelled by all the cabs
    optimal_distance, optimal_route = optimal_total_distance(
                                        all_distances, groups, cabs)
    # Add total distance between group and destination to optimal distance
    optimal_distance = add_destination_distance(optimal_distance,
                            groups, destination)
    # Print answer
    print_answer(optimal_distance, optimal_route, clusters, cabs)


def parse_input_file(input_file):
    """
    Parses the input file based on following format.

    First line contains two integers(m and n space separated),
    indicating number of commuters and cabs. Next m lines contain
    commuter locations. Next n lines contain cab locations.
    Finally, last line contains destination location. Locations
    are in format: x,y

    Returns a tuple of commuters, cab and destination location.
    """

    commuters = []
    cabs = []
    destination = None

    try:
        f = open(input_file, 'r')
    except (OSError, IOError) as e:
        if e.errno == 2:
            print ERR_INPUT_FILE_NOT_FOUND
        else:
            print e.strerror
        sys.exit(1)

    lines_list = f.read().splitlines()
    lines_len = len(lines_list)

    try:
        if lines_len == '0':
            raise Exception(ERR_INPUT_FILE_EMPTY)
        # Parse m and n values
        try:
            m = int(lines_list[0].split(' ')[0])
            n = int(lines_list[0].split(' ')[1])
        except:
            raise Exception(ERR_COMMUTERS_CABS_STR % lines_list[0])
        # Less number of commuter locations
        if lines_len < (m+1):
            raise Exception(ERR_LESS_COMMUTER_LOCATIONS % (m, lines_len-1))
        # Less number of commuter locations
        if lines_len < (m+n+1):
            raise Exception(ERR_LESS_CAB_LOCATIONS % (n, lines_len-m-1))
        # Destination location missing
        if lines_len < (m+n+2):
            raise Exception(ERR_MISSING_DEST_LOCATION)
        # Parse commuter locations
        for i in range(m):
            coords_str = lines_list[i+1]
            coords = Point.get_coords_from_str(coords_str)
            commuter = Commuter(coords)
            commuters.append(commuter)
        # Parse cab locations
        for i in range(n):
            coords_str = lines_list[i+1+m]
            coords = Point.get_coords_from_str(coords_str)
            cab = Cab(coords)
            cabs.append(cab)
        # Parse destination location
        coords_str = lines_list[1+m+n]
        coords = Point.get_coords_from_str(coords_str)
        destination = Point(coords)
    except Exception as e:
        print e
        sys.exit(1)

    return (commuters, cabs, destination)


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


def print_answer(optimal_distance, optimal_route, groups, cabs):
    """
    Prints final answer
    """

    if optimal_distance == -1:
        print 'Sorry, no optimal route could be found :('

    print 'Optimal route taken:'
    for i, r in enumerate(optimal_route):
        print '    %d. Group %s was picked up by Cab %s.' % (
                i+1, groups[r[0]].points, cabs[r[1]])
    print "\nOptimal total distance travelled by all the cabs: %f" % optimal_distance


if __name__ == "__main__":
    # Calling the main function
    main()
