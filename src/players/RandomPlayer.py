from Point import Point
from random import uniform


class RandomPlayer:

    def get_points(self, number_of_points, settings, points=None):
        self.color = "red"
        if points is not None:
            self.color = "blue"
        return [Point(uniform(0, settings['width']), uniform(0, settings['height']), self.color) for i in range(number_of_points)]
