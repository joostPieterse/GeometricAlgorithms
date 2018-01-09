from Point import Point
from View import View
from players.GridPlayer import GridPlayer
from players.RandomPlayer import RandomPlayer
import Delaunay
import Voronoi

class Game:
    def __init__(self, initial_settings):
        self.settings = initial_settings
        self.points = []

        # Delaunay triangulations
        self.delaunay_triangulation = []
        self.n = 0

    def start(self):
        if self.settings['player1'] == "grid":
            player1 = GridPlayer()
        else:
            player1 = RandomPlayer()
        if self.settings['player2'] == "grid":
            player2 = GridPlayer()
        else:
            player2 = RandomPlayer()
        points1 = player1.get_points(number_of_points=self.settings['number_of_points1'], settings=self.settings)
        points2 = player2.get_points(number_of_points=self.settings['number_of_points2'], settings=self.settings,
                                     points=points1)
        self.points = points1 + points2
        #self.points = [Point(190, 646, "red"), Point(808, 629, "red"), Point(1033, 94, "blue"), Point(1139, 466, "blue")]
        self.delaunay_triangulation = Delaunay.computeDelaunay(self.points)
        self.voronoi_diagram = Voronoi.computeVoronoi(self.delaunay_triangulation, self.settings['width'], self.settings['height'])


    def prev(self):
        self.n = self.n - 1
        self.delaunay_triangulation = Delaunay.computeDelaunay(self.points[0:self.n])

if __name__ == "__main__":
    initial_settings = {
        "width": 1500,
        "height": 800,
        "number_of_points1": 10,
        "number_of_points2": 8,
        "player1": "random",
        "player2": "random"
    }
    game = Game(initial_settings)
    view = View(game)
    view.mainloop()
