from Point import Point
from random import randint


class RandomPlayer:
    def __init__(self):
        self.color = "blue"

    def get_points(self, number_of_points, settings, points=None):
        return {Point(randint(0, settings['width']), randint(0, settings['height']), "red") for i in range(number_of_points)}
