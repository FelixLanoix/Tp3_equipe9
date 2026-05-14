import numpy as np


class Balle:
    def __init__(self, canvas, x, y, rayon, couleur):
        self.canvas = canvas
        self.rayon = rayon
        self.vx = 0
        self.vy = 0

        self.id = canvas.create_oval(
            x - rayon, y - rayon,
            x + rayon, y + rayon,
            fill=couleur,
            outline="black"
        )

    def coords(self):
        return self.canvas.coords(self.id)

    def centre(self):
        x1, y1, x2, y2 = self.coords()
        return np.array([(x1 + x2) / 2, (y1 + y2) / 2])

    def deplacer(self):
        self.canvas.move(self.id, self.vx, self.vy)

    def placer_centre(self, p):
        self.canvas.coords(
            self.id,
            p[0] - self.rayon,
            p[1] - self.rayon,
            p[0] + self.rayon,
            p[1] + self.rayon
        )
