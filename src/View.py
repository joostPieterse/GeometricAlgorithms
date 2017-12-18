import tkinter as tk
from tkinter import messagebox

from Point import Point



class View(tk.Tk):
    def _resize(self):
        try:
            width = int(self.rectangle_width.get())
            height = int(self.rectangle_height.get())
            self.screen.config(width=width, height=height)
        except ValueError:
            messagebox.showinfo("Resize failed", "Invalid screen width/height")

    def __init__(self):
        super().__init__()

        self.title("Voronoi game")
        self.geometry("1800x1000")
        self.point_radius = 5

        self.screen = tk.Canvas(self, bg="white", width=1500, height=800)
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
        self.resize_button = tk.Button(self.right_frame, text="Resize", command=self._resize)
        self.resize_button.grid(row=2)

        self.resize_button = tk.Button(self.right_frame, text="Reset", command=self.reset)
        self.resize_button.grid(row=4)

    def resize(self, width, height):
        self.screen.config(width=width, height=height)

    def place_points(self, points):
        for point in points:
            self.screen.create_oval(point.x - self.point_radius, point.y - self.point_radius,
                                    point.x + self.point_radius, point.y + self.point_radius,
                                    fill="black")

    def reset(self):
        self.screen.delete("all")


if __name__ == "__main__":
    view = View()
    points = {Point(x * 100 + 50, y * 100 + 50, "player") for x in range(14) for y in range(9)}
    view.place_points(points)
    view.mainloop()
