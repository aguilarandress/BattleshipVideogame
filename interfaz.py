import tkinter
from tkinter import *
from PIL import Image, ImageTk


def cargarPantallaInicio():
    root = tkinter.Tk()

    root.title("BattleShip v1.0.0")

    backgroundCanvas = Canvas(root, width=602, height=390)
    backgroundCanvas.grid(row=0, column=0)

    # Insertar imagen background
    imagenBackground = ImageTk.PhotoImage(Image.open("background.jpg"))
    backgroundCanvas.create_image(0, 0, anchor=NW, image=imagenBackground)

    boton = Button(root, text="Jugar", command=lambda: cargarPantallaConfiguracion(root))
    boton.grid(row=0, column=0, sticky=NW)
    boton.config(font=("helvetica", 20, "underline italic"))

    root.mainloop()


def cargarPantallaConfiguracion(ventanaActual):
    ventanaActual.destroy()

    root = tkinter.Tk()
    root.title("BattleShip - Configuración")

    root.mainloop()


cargarPantallaInicio()