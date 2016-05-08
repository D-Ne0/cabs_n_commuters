import sys

from errors import ERR_INPUT_FILE_NOT_FOUND
from errors import ERR_INPUT_FILE_EMPTY
from errors import ERR_COMMUTERS_CABS_STR
from errors import ERR_LESS_COMMUTER_LOCATIONS
from errors import ERR_LESS_CAB_LOCATIONS
from errors import ERR_MISSING_DEST_LOCATION
from kmeans import Point, kmeans

"""
Write a utility that takes as input the location of m commuters and n cabs and
a destination location, and outputs optimised cab routes for picking up all
commuters (on a shared basis) and dropping them off at the destination.
"""

def main():

    # Input file that contains the input for
    # commuters, cabs and destination location
    input_file = 'sample_input.txt'

    if len(sys.argv) == 2:
        input_file = sys.argv[1]

    # Parse input file
    commuters, cabs, destination = parse_input_file(input_file)
    # Create clusters of commuters
    clusters = kmeans(commuters, cabs)


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


if __name__ == "__main__":
    main()
