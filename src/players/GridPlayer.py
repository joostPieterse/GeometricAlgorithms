from Point import Point

from math import sqrt, ceil
from random import uniform

class GridPlayer:

    def get_points(self, number_of_points, settings, points=None):
        if number_of_points == 0:
            return []
        color = "red"
        if points is not None:
            color = "blue"
        size = ceil(sqrt(number_of_points))
        points = []
        width = settings['width'] / size
        height = settings['height'] / ceil(number_of_points / size)
        for i in range(size):
            for j in range(size):
                if len(points) < number_of_points:
                    # Prevents points from being colinear
                    points.append(Point(width * (j + 0.5) + uniform(0, 1), height * (i + 0.5) + uniform(0, 1), color))
        print(points)
        return points
