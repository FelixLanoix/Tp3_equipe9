import tkinter as tk 
import numpy as np
LARGEUR, HAUTEUR = 900, 500

jeu = tk.Tk()

jeu.title("billard")

canvas = tk.Canvas(jeu, width= LARGEUR, height= HAUTEUR)
canvas.pack()

canvas.create_rectangle(LARGEUR - 850, HAUTEUR - 450, LARGEUR - 50, HAUTEUR - 50, fill="#3E1F1F", outline="")
canvas.create_rectangle(LARGEUR - 820, HAUTEUR - 420, LARGEUR - 80, HAUTEUR - 80, fill="#00ff4c", outline="")

angle = tk.Spinbox(jeu, from_=0, to= 360, width= 15)
angle.pack()

vitesse = tk.Entry(jeu, width= 15)
vitesse.pack()

etiquette1 = None
def ball(x, y, r, couleur):
    return canvas.create_oval(
        x-r, y-r,
        x+r, y+r,
        fill=couleur  ,
        outline="black"
    )
    


balle_blanche = ball(250, HAUTEUR/2, 12, "white")

vx = 0
vy = 0

def lancer():
    global vx, vy

    angle_deg = float(angle.get())
    vitesse_val = float(vitesse.get())

    angle_rad = np.deg2rad(angle_deg)

    vx = vitesse_val * np.cos(angle_rad)
    vy = -vitesse_val * np.sin(angle_rad)

def deplacer():
    global vx, vy

    x1, y1, x2, y2 = canvas.coords(balle_blanche)

    if x1 <= 80 or x2 >= 820:
        vx = -vx
    if y1 <= 80 or y2 >= 420:
        vy = -vy

    canvas.move(balle_blanche, vx, vy)
    jeu.after(16, deplacer)

bouton1 = tk.Button(jeu, text= "lancer",command= lancer)
bouton1.pack()

deplacer()
jeu.mainloop()


