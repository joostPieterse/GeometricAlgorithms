from Point import Point

from math import sqrt, ceil


class GridPlayer:
    def __init__(self):
        self.color = "blue"

    def get_points(self, number_of_points, settings, points=None):
        color = "blue"
        if points is not None:
            color = "red"
        size = ceil(sqrt(number_of_points))
        points = set()
        width = settings['width'] / size
        height = settings['height'] / ceil(number_of_points / size)
        for i in range(size):
            for j in range(size):
                if len(points) < number_of_points:
                    points.add(Point(width * (j + 0.5), height * (i + 0.5), color))
        return points
