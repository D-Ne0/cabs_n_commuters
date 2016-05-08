import math

from errors import ERR_INVALID_COORDS
from errors import ERR_EMPTY_CLUSTER


# When do we say the optimization has 'converged' and stop updating clusters
CUTOFF = 0.5

class Point(object):
    """
    A point in cartesian co-ordinates i.e (x,y)
    """

    def __init__(self, coords):
        """
        coords - tuple of values i.e (x,y)
        """

        self.coords = coords

    def __repr__(self):
        """
        String representation of this object
        """

        return str(self.coords)

    @classmethod
    def get_coords_from_str(cls, coords_str, delimiter=','):
        """
        Converts a string co-ordinate in to a tuple
        i.e. 'x,y' -> (x,y)
        """

        try:
            x = int(coords_str.split(delimiter)[0])
            y = int(coords_str.split(delimiter)[1])
        except:
            raise Exception(ERR_INVALID_COORDS % coords_str)
        return (x, y)


class Cluster(object):
    """
    A set of points and their centroid
    """

    def __init__(self, points):
        """
        points - A list of point objects
        """

        if len(points) == 0:
            raise Exception(ERR_EMPTY_CLUSTER)
        # The points that belong to this cluster
        self.points = points
        # Set up the initial centroid
        self.centroid = self.calculate_centroid()

    def __repr__(self):
        """
        String representation of this object
        """

        return str(self.points)

    def calculate_centroid(self):
        """
        Find a center point for a group of points
        """

        num_points = len(self.points)
        # Get list of all co-ordinates of this cluster 
        coords = [p.coords for p in self.points]
        # Reformat that so all x's are together, all y's etc.
        unzipped = zip(*coords)
        # Calculate the mean for each dimension
        centroid_coords = tuple([math.fsum(d_list)/num_points for d_list in unzipped])
 
        return Point(centroid_coords)

    def update_centroid(self, points):
        """
        Returns the distance between the previous centroid
        and the new after recalculating and storing the new
        centroid.
        """

        old_centroid = self.centroid
        self.points = points
        self.centroid = self.calculate_centroid()
        shift = get_distance(old_centroid, self.centroid)

        return shift


def kmeans(points, centroids):
    """
    points - all data points
    centroids - all centroids
    """

    # Create clusters using centroids
    clusters = [Cluster([p]) for p in centroids]

    # Loop through the dataset until the clusters stablize
    while True:
        # Create a list of lists to hold the points in each 
        # cluster
        lists = [[] for c in clusters]
        cluster_count = len(clusters)

        for p in points:
            # Smallest distance between point and each cluster. 
            smallest_distance = -1
            # Set the cluster that point belongs to.
            cluster_index = -1
            for i in range(cluster_count):
                # Calculate distance of that point to each other 
                # cluster's centeroid
                distance = get_distance(p, clusters[i].centroid)
                # If it's closer to that cluster's centroid or
                # smalles_distace=-1 update what we think the 
                # smallest distance is, and set the point to that 
                # cluster
                if (distance < smallest_distance or
                    smallest_distance == -1):
                    smallest_distance = distance
                    cluster_index = i
            # Set cluster points
            if cluster_index > -1:
                lists[cluster_index].append(p)

        # Set our buggest shift to zero for this iteration
        biggest_shift = 0.0

        updated_clusters = []
        for i in range(cluster_count):
            if len(lists[i]) == 0:
                continue
            # Calculate how far the centroid moved in this 
            # iteration
            shift = clusters[i].update_centroid(lists[i])
            # Keep track of the largest move from all cluster 
            # centroid updates
            biggest_shift = max(biggest_shift, shift)
            # Add this cluster
            updated_clusters.append(clusters[i])

        clusters = updated_clusters

        # If the centroids have stopped moving much, say we are 
        # done!
        if biggest_shift < CUTOFF:
            break

    return clusters


def get_distance(a, b):
    """
    Returns Euclidean distance between two points.
    """

    ret = reduce(lambda x,y: x + pow((a.coords[y]-b.coords[y]),2),range(2),0.0)
    ret = math.sqrt(ret)

    return ret
