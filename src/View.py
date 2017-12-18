import tkinter as tk
from tkinter import messagebox


class View(tk.Tk):
    def start(self):
        self.screen.delete('all')
        try:
            width = int(self.rectangle_width.get())
            height = int(self.rectangle_height.get())
            self.game.settings['width'] = width
            self.game.settings['height'] = height
            self.screen.config(width=width, height=height)
            self.game.start()
            self.place_points(self.game.points)
        except ValueError:
            messagebox.showinfo("Start failed", "Invalid screen width/height")


    def __init__(self, game):
        super().__init__()
        self.game = game
        self.title("Voronoi game")
        self.geometry("1800x1000")
        self.point_radius = 2

        self.screen = tk.Canvas(self, bg="white", width=self.game.settings['width'], height=self.game.settings['height'])
        self.right_frame = tk.Frame(self, width=300, height=800)
        self.right_frame.pack_propagate(0)

        self.right_frame.pack(side=tk.RIGHT)
        self.screen.pack(side=tk.LEFT)

        tk.Label(self.right_frame, text="Rectangle width: ").grid(row=0, column=0)
        tk.Label(self.right_frame, text="Rectangle height: ").grid(row=1, column=0)
        self.rectangle_width = tk.Entry(self.right_frame)
        self.rectangle_width.grid(row=0, column=1)
        self.rectangle_height = tk.Entry(self.right_frame)
        self.rectangle_height.grid(row=1, column=1)
        self.start_button = tk.Button(self.right_frame, text="Start game", command=self.start)
        self.start_button.grid(row=2)

    def resize(self, width, height):
        self.screen.config(width=width, height=height)

    def place_points(self, points):
        for point in points:
            self.screen.create_oval(point.x - self.point_radius, point.y - self.point_radius,
                                    point.x + self.point_radius, point.y + self.point_radius,
                                    fill=point.color)

    def draw_faces(self, faces):
        pass
