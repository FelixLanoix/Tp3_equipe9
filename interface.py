import tkinter as tk 
import numpy as np
LARGEUR, HAUTEUR = 900, 500

jeu = tk.Tk()

jeu.title("billard")

canvas = tk.Canvas(jeu, width= LARGEUR, height= HAUTEUR)
canvas.pack()

canvas.create_rectangle(LARGEUR - 850, HAUTEUR - 450, LARGEUR - 50, HAUTEUR - 50, fill="#561010", outline="")
canvas.create_rectangle(LARGEUR - 820, HAUTEUR - 420, LARGEUR - 80, HAUTEUR - 80, fill="#268844", outline="")

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
pos_initiale = canvas.coords(balle_blanche)
historique = []
compteur = 0 
friction = 0.01
epsilon = 0.05
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
    global vx, vy, historique, compteur
    

    x1, y1, x2, y2 = canvas.coords(balle_blanche)

    if x1 <= 80 or x2 >= 820:
        vx = -vx
    if y1 <= 80  or y2 >= 420:
        vy = -vy
    
    vx = vx * (1 - friction)
    vy = vy * (1 - friction)

    
    if np.linalg.norm([vx, vy]) <= epsilon:
        vx = 0
        vy = 0


    canvas.move(balle_blanche, vx, vy)
    jeu.after(16, deplacer)
    historique.append([x1, y1, x2, y2])
    compteur+= 1
     
def reset():
    global vx, vy

    vx = 0
    vy = 0

    canvas.coords(balle_blanche, *pos_initiale)

def retour_arriere():
    global vx, vy, historique, compteur
    
    
    if compteur > 10:
        compteur-=10
        canvas.coords(balle_blanche, *historique[compteur])
    else:
        raise Exception ("impossible de revenir en arrière") 
    vx = 0
    vy = 0 


bouton1 = tk.Button(jeu, text= "lancer",command= lancer)
bouton1.pack()

bouton2 = tk.Button(jeu, text= "reset", command= reset)
bouton2.pack()

bouton3 = tk.Button(jeu, text= "<--", command= retour_arriere)
bouton3.pack()

deplacer()
jeu.mainloop()


