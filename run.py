import sys

from algorithm import get_group_cab_distances
from algorithm import optimal_total_distance
from algorithm import add_destination_distance
from kmeans import kmeans
from utils import parse_input_file, print_answer

"""
Program that takes input file as input containing the location 
of m commuters and n cabs and a destination location, and 
outputs optimised cab routes for picking up all commuters (on a 
shared basis) and dropping them off at the destination.
"""

# Sample input file
# Change the number in the end to test with a new sample file
SAMPLE_INPUT_FILE = 'sample_input_0.txt'

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


if __name__ == "__main__":
    # Calling the main function
    main()
