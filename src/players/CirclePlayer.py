from random import uniform

from Point import Point

from math import pi, cos, sin

class CirclePlayer:
    def __init__(self, radius):
        self.radius = radius

    def get_points(self, number_of_points, settings, points=None):
        self.radius = min(self.radius, settings['width'] / 2, settings['height'] / 2)
        self.color = "red"
        if points is not None:
            self.color = "blue"
        points = []
        for i in range(number_of_points):
            angle = i / number_of_points * 2 * pi
            points.append(Point(self.radius * cos(angle) + settings['width'] / 2 + uniform(0, 10), self.radius * sin(angle) + settings['height'] / 2 + uniform(0, 10), self.color))
        return points
