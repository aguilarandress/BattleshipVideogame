
from tkinter import messagebox
def disparoUnico(posicion, matrizTableroBot):

    matrizTableroBot[posicion[0]][posicion[1]].config(bg="red")
    messagebox.showinfo("Disparo Unico", "Disparo unico en " + str(posicion))


def disparoMisil(posicion,matrizTableroBot):
    matrizTableroBot[posicion[0]][posicion[1]].config(bg="red")
    messagebox.showinfo("Disparo Misil", "Disparo Misil en " + str(posicion))


def disparoBomba(posicion,matrizTableroBot):
    matrizTableroBot[posicion[0]][posicion[1]].config(bg="red")
    messagebox.showinfo("Disparo Bomba", "Disparo Bomba en " + str(posicion))
