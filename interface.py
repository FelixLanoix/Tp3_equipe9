import tkinter as tk
import numpy as np
import json
from balles import Balle


class Fichierjson(Exception):
    pass

class Collision(Exception):
    pass

class Friction(Exception):
    pass

class ZeroBalle(Exception):
    pass




LARGEUR, HAUTEUR = 900, 500

jeu = tk.Tk()
jeu.title("billard")

canvas = tk.Canvas(jeu, width=LARGEUR, height=HAUTEUR)
canvas.pack()

canvas.create_rectangle(50, 50, 850, 450, fill="#561010", outline="")
canvas.create_rectangle(80, 80, 820, 420, fill="#268844", outline="")
try:
    with open("balles.json", "r") as fichier:
        data = json.load(fichier)

except FileNotFoundError:
    raise Fichierjson("Le fichier balles.json est introuvable")


friction = data["friction"]
rayon = data["rayon"]

if friction < 0 or friction > 1:
    raise Friction("La friction doit être entre 0 et 1")

liste_balles = []

for info in data["balles"]:
    balle = Balle(
        canvas,
        info["x"],
        info["y"],
        rayon,
        info["couleur"]
    )
    liste_balles.append(balle)

if len(liste_balles) == 0:
    raise ZeroBalle("Il n'y a pas de balle")

balle_blanche = liste_balles[0]


titre_angle = tk.Label(text= "Angle")
titre_angle.pack()

angle = tk.Spinbox(jeu, from_=0, to=360, width=15)
angle.pack()

titre_vitesse = tk.Label(text= "Vitesse")
titre_vitesse.pack()

vitesse = tk.Entry(jeu, width=15)
vitesse.pack()


historique = []
future = []
epsilon = 0.05
vx = 0
vy = 0

pos_initiale = [balle.coords() for balle in liste_balles]

def lancer():
    global future

    try:
        future = []

        angle_deg = float(angle.get())
        vitesse_val = float(vitesse.get())

        angle_rad = np.deg2rad(angle_deg)

        balle_blanche.vx = vitesse_val * np.cos(angle_rad)
        balle_blanche.vy = -vitesse_val * np.sin(angle_rad)

    except:
        raise ValueError("nombre invalide")

def deplacer():
    
    historique.append([balle.coords() for balle in liste_balles])

    for balle in liste_balles:
        balle.vx = balle.vx * (1 - friction)
        balle.vy = balle.vy * (1 - friction)

        if np.linalg.norm([balle.vx, balle.vy]) <= epsilon:
            balle.vx = 0
            balle.vy = 0

    for i in range(len(liste_balles)):
        for j in range(i + 1, len(liste_balles)):
            gerer_collision(liste_balles[i], liste_balles[j])

    for balle in liste_balles:
        x1, y1, x2, y2 = balle.coords()

        if x1 <= 80 or x2 >= 820:
            balle.vx = -balle.vx

        if y1 <= 80 or y2 >= 420:
            balle.vy = -balle.vy

        balle.deplacer()

    jeu.after(16, deplacer)

def reset():
    global historique, future

    historique = []
    future = []

    for i in range(len(liste_balles)):
        liste_balles[i].placer_centre(pos_initiale[i])
        liste_balles[i].vx = 0
        liste_balles[i].vy = 0

def retour_arriere():
    global historique, future

    if len(historique) > 10:
        for i in range(10):
            future.append(historique.pop())

        positions = historique[-1]

        for i in range(len(liste_balles)):
            liste_balles[i].placer_centre(positions[i])
            liste_balles[i].vx = 0
            liste_balles[i].vy = 0
    else:
        print("Impossible de revenir en arrière")

def retour_avant():
    global historique, future

    if len(future) >= 10:
        for i in range(10):
            historique.append(future.pop())

        positions = historique[-1]

        for i in range(len(liste_balles)):
            liste_balles[i].placer_centre(positions[i])
            liste_balles[i].vx = 0
            liste_balles[i].vy = 0
    else:
        print("Impossible d'avancer")


def gerer_collision(b1, b2):
    if rayon <= 0:
        raise Collision("Le rayon doit être positif")

    p1 = b1.centre()
    p2 = b2.centre()

    direction = p2 - p1
    distance = np.linalg.norm(direction)

    if distance == 0:
        return

    if distance < 0:
        raise Collision("Distance de la collision invalide")

    if distance <= 2 * rayon:
        n = direction / distance

        chevauchement = 2 * rayon - distance

        p1 = p1 - (chevauchement / 2) * n
        p2 = p2 + (chevauchement / 2) * n

        b1.placer_centre(p1)
        b2.placer_centre(p2)

        v1 = np.array([b1.vx, b1.vy])
        v2 = np.array([b2.vx, b2.vy])

        v_rel = np.dot(v1 - v2, n)

        if v_rel > 0:
            b1.vx, b1.vy = v1 - v_rel * n
            b2.vx, b2.vy = v2 + v_rel * n

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