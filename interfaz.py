import tkinter
from tkinter import *
from tkinter import ttk
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
    global informacionBarcos
    global dicInstrucciones
    ventanaActual.destroy()

    root = tkinter.Tk()
    root.title("BattleShip - Configuración")

    contenedorTablero = Frame(root)
    contenedorTablero.grid(row=0, column=0, padx=10, pady=10)

    # Insertar matriz de botones en el tablero
    for fila in range(len(matrizTableroUsuario)):
        for columna in range(len(matrizTableroUsuario[fila])):
            boton = Button(contenedorTablero, text="   ", padx=6, pady=4)

            matrizTableroUsuario[fila][columna] = boton
            boton.grid(row=fila, column=columna, padx=5, pady=5)

            boton.bind("<Button-1>", posicionarBarco)

    # Crear simbologia
    contenedorSimbologia = Frame(root)
    contenedorSimbologia.grid(row=0, column=1)

    etiquetaSimbologia = Label(contenedorSimbologia, text="Simbología", anchor=W)
    etiquetaSimbologia.grid(row=0, column=0, pady=10)

    # Insertar tabla de simbologia con botones con colores y sus etiquetas
    for i in range(len(informacionBarcos)):
        boton = Button(contenedorSimbologia, text=informacionBarcos[i][0], padx=5, pady=5 )
        if informacionBarcos[i][1] == "Espacio sin tocar":
            boton.config(padx=13, pady=13)
        else:
            boton.config(bg=informacionBarcos[i][2], font=("helvetica", 15, "bold"))

        boton.grid(row=i + 1, column=0, sticky=W, pady=5)

        etiqueta = Label(contenedorSimbologia, text=informacionBarcos[i][1], padx=30)
        etiqueta.grid(row=i + 1, column=1, pady=5)

    # Crear tabla de opciones
    contenedorOpciones = Frame(root)
    contenedorOpciones.grid(row=1, column=1)

    etiquetaOpciones = Label(contenedorOpciones, text="Configurar tablero")
    etiquetaOpciones.grid(row=0, column=0, pady=(0, 15))

    etiquetaAgregar = Label(contenedorOpciones, text="Añadir")
    etiquetaAgregar.grid(row=1, column=0)

    # Crear menu despegable
    variableMenuDesple = StringVar()
    menuDesplegable = ttk.Combobox(contenedorOpciones, state="readonly", textvariable=variableMenuDesple )
    menuDesplegable["values"] = ["Portaviones", "Acorazado", "Buque de Guerra", "Submarino", "Destructor"]
    menuDesplegable.grid(row=1, column=1, padx=20)
    menuDesplegable.current(0)
    menuDesplegable.bind("<<ComboboxSelected>>",lambda cambioBarco: dicInstrucciones.update({"Barco": variableMenuDesple.get()}) )

    horiVertiVariable = BooleanVar()
    negPosVariable = BooleanVar()
    horiVertiVariable.set(0)
    negPosVariable.set(0)

    # Texto, Variable, Valor, Fila, Columna
    radCondfiguracion = (
        ("Horizontal", horiVertiVariable, 1, 2, 0),
        ("Vertical", horiVertiVariable, 2, 2, 1),
        ("Positivo", negPosVariable, 3, 3, 0),
        ("Negativo", negPosVariable, 4, 3, 1)
    )

    # Creación de botones de radio para configuración
    radBotones = []
    for text, variable, valor, fila, columna in radCondfiguracion:
        radioButton = Radiobutton(contenedorOpciones, text=text, variable=variable, value=valor, \
        command=lambda text=text, variable=variable: configuracionTablero(text, variable.get()))

        radioButton.grid(row=fila, column=columna, padx=20, pady=10)
        radBotones.append(radioButton)

    botonJugar = Button(root, text="Continuar", command=lambda: cargarPantallaJuego(root))
    botonJugar.grid(row=1, column=0, sticky=SW)
    botonJugar.config(font=("helvetica", 12, "underline"))

    root.mainloop()


def posicionarBarco(evento):
    global dicInstrucciones
    boton = evento.widget
    infoPosicion = boton.grid_info()

    print(infoPosicion["row"], infoPosicion["column"])
    print(dicInstrucciones)

def configuracionTablero(pos="", valor=False):
    global dicInstrucciones

    if pos != "" and valor != False:
        dicInstrucciones[pos] = valor
        if pos == "Horizontal":
            dicInstrucciones["Vertical"] = False
        elif pos == "Vertical":
            dicInstrucciones["Horizontal"] = False
        elif pos == "Positivo":
            dicInstrucciones["Negativo"] = False
        else:
            dicInstrucciones["Positivo"] = False


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


# Variables globales
matrizTableroUsuario = [[str(i) + str(j) for j in range(10)] for i in range(10)]
informacionBarcos = [
    ("", "Espacio sin tocar", ""),
    ("1", "Portaviones", "blue"),
    ("2", "Acorazado", "yellow"),
    ("3", "Buque de Guerra", "magenta"),
    ("4", "Submarino", "cyan"),
    ("5", "Destructor", "grey")
]
dicInstrucciones = {"Horizontal": False, "Vertical": False, "Positivo": False, "Negativo": False, "Barco": "Portaviones"}
# Inicio del juego
cargarPantallaInicio()