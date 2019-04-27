import tkinter
from tkinter import *
from PIL import Image, ImageTk


def cargarPantallaInicio():
    """Carga la pantalla de inicio del juego

    Entradas:
        No recibe
    Precondiciones:
        No hay
    Salidas:
        No retorna nada
    Proceso:
        1. Se inicializa la variable "root" y se configura la ventana
        2. Se configura un objeto Canvas para las dimensiones de la imagen
        3. Se obtiene la imagen en un objeto manipulable para Tkinter
        4. La imagen se inserta en el Canvas
        5. El boton "Jugar" es creado, luego se configura y se inserta
        en la ventana
    """
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
    """Carga la pantalla de configuración del juego

    Entradas:
        ventanaActual: un objeto que representa la ventana que se
        está corriendo
    Precondicones:
        ventanaActual tiene que ser una ventana que se esté
        ejecutando
    Salidas:
        No retorna nada
    Proceso:
        1. Se destruye la ventana actual y se crea una nueva
        2. Se crea un contenedor para el tablero
        3. Una matriz 10x10 es creada con "list comprehensions"
        4. Con un ciclo for anidado se crea la matriz de botones en
        el tablero
        5. Se inserta un boton de continuar
        6. Se inicia el "mainloop" de la ventana
    """
    global matrizTableroUsuario

    ventanaActual.destroy()

    root = tkinter.Tk()
    root.title("BattleShip - Configuración")

    contenedorTablero = Frame(root)
    contenedorTablero.grid(row=0, column=0)

    # Crear matriz para tablero de juego
    matrizTableroUsuario = [[str(i) + str(j) for j in range(10)] for i in range(10)]

    # Insertar matriz en el tablero
    for fila in range(len(matrizTableroUsuario)):
        for columna in range(len(matrizTableroUsuario[fila])):
            boton = Button(contenedorTablero, text="   ")

            matrizTableroUsuario[fila][columna] = boton
            boton.grid(row=fila, column=columna)

            boton.bind("<Button-1>", eventoClick)

    print(matrizTableroUsuario)

    # TODO: Insertar el resto de la interfaz en la pantalla de juego

    botonJugar = Button(root, text="Continuar", command=lambda: cargarPantallaJuego(root))
    botonJugar.grid(row= 1, column=0)

    root.mainloop()


def eventoClick(event):
    boton = event.widget
    infoPosicion = boton.grid_info()

    print(infoPosicion["row"], infoPosicion["column"])


def cargarPantallaJuego(ventanaActual):
    ventanaActual.destroy()

    root = tkinter.Tk()
    root.title("BattleShip - Pantalla de Juego")

    #TODO: Insertar el resto de la pantalla de juego

    boton = Button(root, text="Continuar", command=lambda: cargarPantallaFinJuego(root))
    boton.grid(row=0, column=0)

    root.mainloop()


def cargarPantallaFinJuego(ventanaActual):
    ventanaActual.destroy()

    root = tkinter.Tk()
    root.title("Fin de juego")

    backgroundCanvas = Canvas(root, width=602, height=390)
    backgroundCanvas.grid(row=0, column=0)

    # Insertar imagen background
    imagenBackground = ImageTk.PhotoImage(Image.open("background.jpg"))
    backgroundCanvas.create_image(0, 0, anchor=NW, image=imagenBackground)

    boton = Button(root, text="Salir", command=lambda: root.destroy())
    boton.grid(row=0, column=0, sticky=NW)
    boton.config(font=("helvetica", 20, "underline italic"))

    root.mainloop()


matrizTableroUsuario = []
cargarPantallaInicio()