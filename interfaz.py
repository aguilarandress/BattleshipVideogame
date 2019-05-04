import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from funcionValidacion import configurarTablero


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
    menuDesplegable.bind("<<ComboboxSelected>>", lambda cambioBarco: dicInstrucciones.update({"Barco": variableMenuDesple.get()}))

    horiVertiVariable = BooleanVar()
    negPosVariable = BooleanVar()
    horiVertiVariable.set(1)
    negPosVariable.set(1)

    # Texto, Variable, Valor, Fila, Columna
    radCondfiguracion = (
        ("Horizontal", horiVertiVariable, 1, 2, 0),
        ("Vertical", horiVertiVariable, 0, 2, 1),
        ("Positivo", negPosVariable, 1, 3, 0),
        ("Negativo", negPosVariable, 0, 3, 1)
    )

    # Creación de botones de radio para configuración
    for text, variable, valor, fila, columna in radCondfiguracion:
        radioButton = Radiobutton(contenedorOpciones, text=text, variable=variable, value=valor, \
        command=lambda direccion=text: configurarDirecciones(direccion))

        radioButton.grid(row=fila, column=columna, padx=20, pady=10)

    botonJugar = Button(root, text="Continuar", command=lambda: cargarPantallaJuego(root))
    botonJugar.grid(row=1, column=0, sticky=SW)
    botonJugar.config(font=("helvetica", 12, "underline"))

    root.mainloop()


def posicionarBarco(evento):
    global dicInstrucciones
    global informacionBarcos
    global matrizTableroUsuario

    barcoActual = dicInstrucciones["Barco"]

    # Obtener información del barco
    espacios = 0
    color = ""
    numeroBarco = ""
    for barco in informacionBarcos:
        if barco[1] == barcoActual:
            espacios = barco[3]
            color = barco[2]
            numeroBarco = barco[0]

    boton = evento.widget
    infoPosicion = boton.grid_info()

    posicionActual = (infoPosicion["row"], infoPosicion["column"])

    #TODO: Validar posicionamiento de los barcos

    if dicInstrucciones["Horizontal"]:
        if dicInstrucciones["Positivo"]:
            for i in range(espacios):
                matrizTableroUsuario[posicionActual[0]][posicionActual[1] + i].config(bg=color, text=numeroBarco)
        else:
            for i in range(espacios):
                matrizTableroUsuario[posicionActual[0]][posicionActual[1] - i].config(bg=color, text=numeroBarco)
    else:
        if dicInstrucciones["Positivo"]:
            for i in range(espacios):
                matrizTableroUsuario[posicionActual[0] - i][posicionActual[1]].config(bg=color, text=numeroBarco)
        else:
            for i in range(espacios):
                matrizTableroUsuario[posicionActual[0] + i][posicionActual[1]].config(bg=color, text=numeroBarco)


def configurarDirecciones(direccion):
    global dicInstrucciones

    dicInstrucciones[direccion] = True
    if direccion != "":
        if direccion == "Horizontal":
            dicInstrucciones["Vertical"] = False
        elif direccion == "Vertical":
            dicInstrucciones["Horizontal"] = False
        elif direccion == "Positivo":
            dicInstrucciones["Negativo"] = False
        else:
            dicInstrucciones["Positivo"] = False
    print(dicInstrucciones)


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
    ("1", "Portaviones", "blue", 5),
    ("2", "Acorazado", "yellow", 4),
    ("3", "Buque de Guerra", "magenta", 3),
    ("4", "Submarino", "cyan", 3),
    ("5", "Destructor", "grey", 2)
]
dicInstrucciones = {"Horizontal": True, "Vertical": False, "Positivo": True, "Negativo": False, "Barco": "Portaviones"}

# Inicio del juego
cargarPantallaInicio()