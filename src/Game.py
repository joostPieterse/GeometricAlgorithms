from Point import Point
from View import View
from players.GridPlayer import GridPlayer
from players.LargestFacePlayer import LargestFacePlayer
from players.LongestEdgePlayer import LongestEdgePlayer
from players.RandomPlayer import RandomPlayer
from players.CirclePlayer import CirclePlayer
from players.LinePlayer import LinePlayer
import Delaunay
import Voronoi
import logging
import sys
from random import shuffle

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(asctime)s - %(message)s")


class Game:
    def __init__(self, initial_settings):
        self.settings = initial_settings
        self.points = []

        # Delaunay triangulations
        self.delaunay_triangulation = []
        self.n = 0
        self.voronoi_areas = {"red": 0, "blue": 0}

    def start(self):
        if self.settings['player1'] == "grid":
            player1 = GridPlayer()
        elif self.settings['player1'] == "circle":
            player1 = CirclePlayer(300)
        elif self.settings['player1'] == "line":
            player1 = LinePlayer()
        else:
            player1 = RandomPlayer()

        logging.info("Get player 1's points")
        points1 = player1.get_points(number_of_points=self.settings['number_of_points1'], settings=self.settings)
        delaunay_triangulation_player1 = Delaunay.computeDelaunay(points1)
        voronoi_player1 = Voronoi.computeVoronoi(delaunay_triangulation_player1, self.settings['width'], self.settings['height'])
        if self.settings['player2'] == "grid":
            player2 = GridPlayer()
        elif self.settings['player2'] == "circle":
            player2 = CirclePlayer(300)
        elif self.settings['player2'] == "line":
            player2 = LinePlayer()
        elif self.settings['player2'] == "longest Delaunay edge":
            player2 = LongestEdgePlayer(delaunay_triangulation_player1)
        elif self.settings['player2'] == "largest Voronoi face":
            player2 = LargestFacePlayer(voronoi_player1)
        else:
            player2 = RandomPlayer()
        logging.info("Get player 2's points")
        points2 = player2.get_points(number_of_points=self.settings['number_of_points2'], settings=self.settings,
                                     points=points1)
        self.points = points1 + points2
        shuffle(self.points)
        logging.info("Compute Delaunay triangulation")

        self.delaunay_triangulation = Delaunay.computeDelaunay(self.points)
        logging.info("Compute Voronoi diagram")
        self.voronoi_diagram = Voronoi.computeVoronoi(self.delaunay_triangulation, self.settings['width'], self.settings['height'])
        self.voronoi_areas = Voronoi.get_area_percentages(self.voronoi_diagram, self.settings['width'], self.settings['height'])


    def prev(self):
        self.n = self.n - 1
        self.delaunay_triangulation = Delaunay.computeDelaunay(self.points[0:self.n])

if __name__ == "__main__":
    initial_settings = {
        "width": 1000,
        "height": 600,
        "number_of_points1": 10,
        "number_of_points2": 8,
        "player1": "random",
        "player2": "longest Delaunay edge"
    }
    totalAreaBlue = 0
    averageAreaBlue = 0
    for i in range (0, 100):
        game = Game(initial_settings)
        game.start()
        totalAreaBlue = totalAreaBlue + game.voronoi_areas["blue"]
        averageAreaBlue = totalAreaBlue / 100
  #      print("Areas:", game.voronoi_areas)
  #      print("Total Area blue: ", totalAreaBlue)
        print("Average blue area: ", averageAreaBlue)
    #view = View(game)
    #view.mainloop()
