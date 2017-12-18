from Point import Point
from View import View
from players.RandomPlayer import RandomPlayer


class Game:
    def __init__(self, initial_settings):
        self.settings = initial_settings

    def start(self):
        player1 = RandomPlayer()
        player2 = RandomPlayer()
        points1 = player1.get_points(number_of_points=10, settings=self.settings)
        points2 = player2.get_points(number_of_points=10, settings=self.settings, points=points1)
        self.points = points1.union(points2)


if __name__ == "__main__":
    initial_settings = {
        "width": 1500,
        "height": 800
    }
    game = Game(initial_settings)
    view = View(game)
    view.mainloop()
