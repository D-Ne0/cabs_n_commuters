import sys

from errors import ERR_INPUT_FILE_NOT_FOUND
from errors import ERR_INPUT_FILE_EMPTY
from errors import ERR_COMMUTERS_CABS_STR
from errors import ERR_LESS_COMMUTER_LOCATIONS
from errors import ERR_LESS_CAB_LOCATIONS
from errors import ERR_MISSING_DEST_LOCATION
from kmeans import Point
from models import Commuter, Cab


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

