class Balle:
    def __init__(self, canvas, x, y, rayon, couleur):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.rayon = rayon
        self.couleur = couleur
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

    def deplacer(self, vx, vy):
        self.canvas.move(self.id, vx, vy)

    def placer(self, coords):
        self.canvas.coords(self.id, *coords)