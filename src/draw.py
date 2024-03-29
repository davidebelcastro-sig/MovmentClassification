import turtle
import time
import os

def conta_volte(i, lista, el):
    cont = 0
    while i < len(lista) and lista[i].strip() == el:
        cont += 1
        i += 1
    return cont

   
def disegna_camminata(t, distanza):
    distanza = distanza * 30
    t.forward(distanza)

def disegna_giro_dx(t, angolo=90):
    t.right(angolo)

def disegna_giro_sx(t, angolo=90):
    t.left(angolo)


t = turtle.Turtle()
t.speed(1)
#create dir camminata odierna
now = time.strftime("%d-%m-%Y-%H-%M-%S")
if not os.path.exists("attivita/"+ now):
    os.makedirs("attivita/"+ now)
fl = open("attivita/attivita.txt","r")
lista = fl.readlines()
fl.close()
k = 0
lunghezza_lista = len(lista)
piano = 0
while k < lunghezza_lista:
    lista[k] = lista[k].strip()
    if lista[k] == "dx":
        disegna_giro_dx(t)
        k += 1
    elif lista[k] == "sx":
        disegna_giro_sx(t)
        k += 1
    else:
        cont = conta_volte(k, lista, lista[k])
        if cont > 1:
            if lista[k] == "camminata":
                disegna_camminata(t,cont)
            else:
                t.screen.getcanvas().postscript(file="attivita/"+now+"/disegno"+str(piano)+".eps")
                if lista[k] == "salire":
                    piano += 1
                else:
                    piano -= 1
                turtle.resetscreen()
        k += cont


t.screen.getcanvas().postscript(file="attivita/"+now+"/disegno"+str(piano)+".eps")



