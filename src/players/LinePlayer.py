from Point import Point

from random import uniform

class LinePlayer:

    def get_points(self, number_of_points, settings, points=None):
        self.color = "red"
        if points is not None:
            self.color = "blue"
        return [Point((i + 1) * settings['width'] / (number_of_points + 1), settings['height'] / 2 + uniform(0, 10), self.color) for i in range(number_of_points)]

