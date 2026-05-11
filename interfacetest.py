import tkinter as tk

LARGEUR, HAUTEUR = 900, 500

root = tk.Tk()
root.title("Billard 2D")

canvas = tk.Canvas(root, width=LARGEUR, height=HAUTEUR)
canvas.pack()

# Table
canvas.create_rectangle(50, 50, 850, 450, fill="#3E1F1F", outline="")
canvas.create_rectangle(80, 80, 820, 420, fill="#00ff4c", outline="")

# Trous
holes = [
    (80, 80), (450, 80), (820, 80),
    (80, 420), (450, 420), (820, 420)
]

root.mainloop()

for x, y in holes:
    canvas.create_oval(x-22, y-22, x+22, y+22, fill="black", outline="")

# Boules
def create_ball(x, y, r, color):
    return canvas.create_oval(
        x-r, y-r,
        x+r, y+r,
        fill=color,
        outline="black"
    )

white_ball = create_ball(250, 250, 12, "white")
red_ball = create_ball(600, 250, 12, "red")
black_ball = create_ball(630, 230, 12, "black")
