import tkinter as tk
from tkinter import messagebox
import math

class View(tk.Tk):
    def start(self):
        self.screen.delete('all')
        try:
            width = int(self.rectangle_width.get())
            height = int(self.rectangle_height.get())
            self.game.settings['width'] = width
            self.game.settings['height'] = height
            self.screen.config(width=width, height=height)
        except ValueError:
            messagebox.showinfo("Start failed", "Invalid screen width/height")
            return
        num_p1 = int(self.num_points1.get())
        num_p2 = int(self.num_points2.get())
        self.game.settings['number_of_points1'] = num_p1
        self.game.settings['number_of_points2'] = num_p2

        self.game.settings['player1'] = self.player1.get()
        self.game.settings['player2'] = self.player2.get()
        self.game.start()
        self.draw_points(self.game.points)
        self.draw_delaunay(self.game.delaunay_triangulation)
        self.draw_voronoi(self.game.voronoi_diagram)

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.title("Voronoi game")
        self.state('zoomed')
        self.point_radius = 2

        self.screen = tk.Canvas(self, bg="white", width=self.game.settings['width'],
                                height=self.game.settings['height'])
        self.right_frame = tk.Frame(self, width=300, height=800)
        self.right_frame.pack_propagate(0)

        self.right_frame.pack(side=tk.RIGHT)
        self.screen.pack(side=tk.LEFT)

        tk.Label(self.right_frame, text="Rectangle width: ").grid(row=0, column=0)
        tk.Label(self.right_frame, text="Rectangle height: ").grid(row=1, column=0)
        self.rectangle_width = tk.Entry(self.right_frame)
        self.rectangle_width.insert(tk.END, self.game.settings['width'])
        self.rectangle_width.grid(row=0, column=1)
        self.rectangle_height = tk.Entry(self.right_frame)
        self.rectangle_height.insert(tk.END, self.game.settings['height'])
        self.rectangle_height.grid(row=1, column=1)

        tk.Label(self.right_frame, text="Number of points for player 1: ").grid(row=2, column=0)
        tk.Label(self.right_frame, text="Number of points for player 2: ").grid(row=3, column=0)
        self.num_points1 = tk.Entry(self.right_frame)
        self.num_points1.insert(tk.END, self.game.settings['number_of_points1'])
        self.num_points1.grid(row=2, column=1)
        self.num_points2 = tk.Entry(self.right_frame)
        self.num_points2.insert(tk.END, self.game.settings['number_of_points2'])
        self.num_points2.grid(row=3, column=1)

        tk.Label(self.right_frame, text="Select player 1: ").grid(row=4, column=0)
        tk.Label(self.right_frame, text="Select player 2: ").grid(row=5, column=0)
        self.player1 = tk.StringVar(self.right_frame)
        self.player1_dropdown = tk.OptionMenu(self.right_frame, self.player1, *["random", "grid"])
        self.player1.set(self.game.settings['player1'])
        self.player1_dropdown.grid(row=4, column=1)
        self.player2 = tk.StringVar(self.right_frame)
        self.player2_dropdown = tk.OptionMenu(self.right_frame, self.player2, *["random", "grid"])
        self.player2.set(self.game.settings['player2'])
        self.player2_dropdown.grid(row=5, column=1)

        self.start_button = tk.Button(self.right_frame, text="Start game", command=self.start)
        self.start_button.grid(row=6)

    def _resize(self):
        try:
            width = int(self.rectangle_width.get())
            height = int(self.rectangle_height.get())
            self.screen.config(width=width, height=height)
        except ValueError:
            messagebox.showinfo("Resize failed", "Invalid screen width/height")

    def resize(self, width, height):
        self.screen.config(width=width, height=height)

    def draw_points(self, points):
        for point in points:
            self.screen.create_oval(point.x - self.point_radius, point.y - self.point_radius,
                                    point.x + self.point_radius, point.y + self.point_radius,
                                    fill=point.color)

    def draw_delaunay(self, delaunay_triangulation):
        for triangle in delaunay_triangulation:
            self.screen.create_line(triangle[0].x, triangle[0].y, triangle[1].x, triangle[1].y)
            self.screen.create_line(triangle[0].x, triangle[0].y, triangle[2].x, triangle[2].y)
            self.screen.create_line(triangle[1].x, triangle[1].y, triangle[2].x, triangle[2].y)


    def draw_voronoi(self, faces):
        for point, face in faces.items():
            voronoi_points = faces[point]
            coordinates = [p for p in voronoi_points]
            coordinates.sort(key=lambda p: math.atan2(point.y - p[1], point.x - p[0]))
            coordinates.append(coordinates[0])
            print("coordinates for drawing", point, coordinates)
            self.screen.create_polygon(coordinates, outline='green', fill=point.color, stipple='gray25')


