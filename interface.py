import tkinter as tk
import numpy as np
import json
from balles import Balle

LARGEUR, HAUTEUR = 900, 500

jeu = tk.Tk()
jeu.title("billard")

canvas = tk.Canvas(jeu, width=LARGEUR, height=HAUTEUR)
canvas.pack()

canvas.create_rectangle(50, 50, 850, 450, fill="#561010", outline="")
canvas.create_rectangle(80, 80, 820, 420, fill="#268844", outline="")

with open("balles.json", "r") as fichier:
    data = json.load(fichier)

friction = data["friction"]
rayon = data["rayon"]

liste_balles = []

for i in data["balles"]:
    balle = Balle(
        canvas,
        i["x"],
        i["y"],
        rayon,
        i["couleur"]
    )
    liste_balles.append(balle)

balle_blanche = liste_balles[0]

angle = tk.Spinbox(jeu, from_=0, to=360, width=15)
angle.pack()

vitesse = tk.Entry(jeu, width=15)
vitesse.pack()

historique = []
future = []
epsilon = 0.05
vx = 0
vy = 0

pos_initiale = balle_blanche.coords()


def lancer():
    global vx, vy, future

    future = []

    angle_deg = float(angle.get())
    vitesse_val = float(vitesse.get())

    angle_rad = np.deg2rad(angle_deg)

    vx = vitesse_val * np.cos(angle_rad)
    vy = -vitesse_val * np.sin(angle_rad)


def deplacer():
    global vx, vy

    x1, y1, x2, y2 = balle_blanche.coords()

    if x1 <= 80 or x2 >= 820:
        vx = -vx

    if y1 <= 80 or y2 >= 420:
        vy = -vy

    vx = vx * (1 - friction)
    vy = vy * (1 - friction)

    if np.linalg.norm([vx, vy]) <= epsilon:
        vx = 0
        vy = 0

    if vx != 0 or vy != 0:
        historique.append(balle_blanche.coords())
        balle_blanche.deplacer(vx, vy)

    jeu.after(16, deplacer)


def reset():
    global vx, vy, historique, future

    vx = 0
    vy = 0

    historique = []
    future = []

    balle_blanche.placer(pos_initiale)


def retour_arriere():
    global vx, vy

    vx = 0
    vy = 0

    if len(historique) > 10:
        for i in range(10):
            future.append(historique.pop())

        balle_blanche.placer(historique[-1])
    else:
        print("Impossible de revenir en arrière")


def retour_avant():
    global vx, vy

    vx = 0
    vy = 0

    if len(future) >= 10:
        for i in range(10):
            historique.append(future.pop())

        balle_blanche.placer(historique[-1])
    else:
        print("Impossible d'avancer")


bouton1 = tk.Button(jeu, text="lancer", command=lancer)
bouton1.pack()

bouton2 = tk.Button(jeu, text="reset", command=reset)
bouton2.pack()

bouton3 = tk.Button(jeu, text="<--", command=retour_arriere)
bouton3.pack()

bouton4 = tk.Button(jeu, text="-->", command=retour_avant)
bouton4.pack()

deplacer()
jeu.mainloop()