from kmeans import Point


class Commuter(Point):
    """
    This class represents a commuter at a location.
    """

    def __init__(self, coords):
        """
        coords - tuple of values i.e (x,y)
        """

        super(Commuter, self).__init__(coords)


class Cab(Point):
    """
    This class represents a Cab at a location. 
    """

    def __init__(self, coords):
        """
        coords - tuple of values i.e (x,y)
        """

        super(Cab, self).__init__(coords)

