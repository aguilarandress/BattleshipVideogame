import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
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
    global dicPosicionesBarcos

    barcoActual = dicInstrucciones["Barco"]
    posicionBarco =[]
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

    if  validacioPosEnMatriz(posicionActual, str(barcoActual)):
        if dicInstrucciones["Horizontal"]:
            if dicInstrucciones["Positivo"]:
                for i in range(espacios):
                    matrizTableroUsuario[posicionActual[0]][posicionActual[1] + i].config(bg=color, text=numeroBarco)
                    posicionBarco += [[posicionActual[0]] + [posicionActual[1] + i]]
                dicPosicionesBarcos[str(barcoActual)] = posicionBarco
            else:
                for i in range(espacios):
                    matrizTableroUsuario[posicionActual[0]][posicionActual[1] - i].config(bg=color, text=numeroBarco)
                    posicionBarco += [[posicionActual[0]] + [posicionActual[1] - i]]
                dicPosicionesBarcos[str(barcoActual)] = posicionBarco
        else:
            if dicInstrucciones["Positivo"]:
                for i in range(espacios):
                    matrizTableroUsuario[posicionActual[0] - i][posicionActual[1]].config(bg=color, text=numeroBarco)
                    posicionBarco += [[posicionActual[0] - i] + [posicionActual[1]]]
                dicPosicionesBarcos[str(barcoActual)] = posicionBarco
            else:
                for i in range(espacios):
                    matrizTableroUsuario[posicionActual[0] + i][posicionActual[1]].config(bg=color, text=numeroBarco)
                    posicionBarco += [[posicionActual[0] + i] + [posicionActual[1]]]
                dicPosicionesBarcos[str(barcoActual)] = posicionBarco
    print(dicPosicionesBarcos)


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


def validacioPosEnMatriz(posicion, barcoActual):
    global dicPosicionesBarcos
    global dicInstrucciones

    diccionario = dicInstrucciones
    dicPosicionAnterior = dicPosicionesBarcos
    infoBarcos = {"Posicion" : False}
    # Configuracion para validacion de barcos seun su tipo se condiciona su posicion minima o maxima
    posConfigValidacion = (
        ("Portaviones", 3, 6),
        ("Acorazado", 2, 7),
        ("Buque de Guerra", 1, 8),
        ("Submarino", 1, 8),
        ("Destructor", 0, 9)
    )

    for barco, posMin, posMax in posConfigValidacion:
        if len(dicPosicionAnterior[barcoActual])!= 0 :
            for i in dicPosicionAnterior[barcoActual]:
                matrizTableroUsuario[i[0]][i[1]].config(bg="grey92", text="   ")

        if diccionario["Barco"] == barco :
            if diccionario["Positivo"]:
                if  diccionario["Vertical"] and posMin < posicion[0] :
                    infoBarcos["Posicion"] = True
                    infoBarcos[barco] = barco

                if  diccionario["Horizontal"] and posMax > posicion[1] :
                    infoBarcos["Posicion"] = True
                    infoBarcos[barco] = barco

            if diccionario["Negativo"]:
                if  diccionario["Vertical"] and posMax > posicion[0] :
                    infoBarcos["Posicion"] = True
                    infoBarcos[barco] = barco

                if  diccionario["Horizontal"] and posMin < posicion[1] :
                    infoBarcos["Posicion"] = True
                    infoBarcos[barco] = barco
            if infoBarcos["Posicion"]:
                print("Posicion en Matriz: ", infoBarcos["Posicion"])
                return validacionBarcos(posicion)
            else:
                messagebox.showerror("ERROR", "El barco deleccionado no puede ser posicionado segun la configuracion"
                                    + "solicitada, seleccione una configuracion diferente")
                return infoBarcos["Posicion"]


def validacionBarcos(posicion):
    def validacionBarcos_PosicionFutura(posicionActual):
        global informacionBarcos
        global matrizTableroUsuario

        barcoActual = dicInstrucciones["Barco"]
        posicionFutura = []

        # Obtener información del barco
        largo = 0
        for barco in informacionBarcos:
            if barco[1] == barcoActual:
                largo = barco[3]

        if dicInstrucciones["Horizontal"]:
            if dicInstrucciones["Positivo"]:
                for i in range(largo):
                    posicionFutura += [[posicionActual[0]] + [posicionActual[1] + i]]
                return posicionFutura
            else:
                for i in range(largo):
                    posicionFutura += [[posicionActual[0]] + [posicionActual[1] - i]]
                return posicionFutura
        else:
            if dicInstrucciones["Positivo"]:
                for i in range(largo):
                    posicionFutura += [[posicionActual[0] - i ] + [posicionActual[1]]]
                return posicionFutura
            else:
                for i in range(largo):
                    posicionFutura += [[posicionActual[0] + i] + [posicionActual[1]]]
                return posicionFutura


    posicionFutura = validacionBarcos_PosicionFutura(posicion)
    print(posicionFutura)
    for llave in dicPosicionesBarcos:
        for contador in range(len(posicionFutura)):
            if posicionFutura[contador] in dicPosicionesBarcos[llave] and llave != dicInstrucciones["Barco"]:
                messagebox.showerror("ERROR",
                                     "El barco deleccionado no puede ser posicionado segun la posicion solicitada" \
                                     + ", seleccione una posicion diferente")
                return False

    return True


def cargarPantallaJuego(ventanaActual):
    global matrizTableroBot
    global matrizTableroUsuario
    global informacionBarcos

    ventanaActual.destroy()

    root = tkinter.Tk()
    root.title("BattleShip - Pantalla de Juego")

    etiquetaTurno = Label(root, text="Su Turno", font=("helvetica", 18, "underline italic"))
    etiquetaTurno.grid(row=0, column=0, sticky=NW)

    contenedorEnemigo = Frame(root)
    contenedorEnemigo.grid(row=1, column=0, pady=(50, 0))
    etiquetaTableroEnemigo = Label(contenedorEnemigo, text="Tablero Enemigo")
    etiquetaTableroEnemigo.grid(row=0, column=0, sticky=NW)
    contenedorTableroEnemigo = Frame(contenedorEnemigo)
    contenedorTableroEnemigo.grid(row=1, column=1)

    # Crear tablero enemigo
    for fila in range(len(matrizTableroBot)):
        for columna in range(len(matrizTableroBot[fila])):
            boton = Button(contenedorTableroEnemigo, text="   ", padx=6, pady=4)

            matrizTableroBot[fila][columna] = boton
            boton.grid(row=fila, column=columna, padx=5, pady=5)

    contenedorEstatusEnemigo = Frame(contenedorEnemigo)
    contenedorEstatusEnemigo.grid(row=2, column=0)
    etiquetaEstatusEnemigo = Label(contenedorEstatusEnemigo, text="Estatus Enemigo", justify=LEFT)
    etiquetaEstatusEnemigo.grid(row=0, column=0, sticky=W)

    estatusEnemigo = {
        "Portaviones": ("Posición Desconocida", "En pie"),
        "Acorazado": ("Posición Desconocida", "En pie"),
        "Buque de Guerra": ("Posición Desconocida", "En pie"),
        "Submarino": ("Posición Desconocida", "En pie"),
        "Destructor": ("Posición Desconocida", "En pie")
    }

    contador = 1
    for barco in estatusEnemigo:
        texto = barco + ": " + estatusEnemigo[barco][0] + ", " + estatusEnemigo[barco][1]
        etiquetaEstatus = Label(contenedorEstatusEnemigo, text=texto, justify=LEFT)
        etiquetaEstatus.grid(row=contador, column=0, sticky=W)
        contador += 1

    contenedorUsuario = Frame(root)
    contenedorUsuario.grid(row=1, column=1, pady=(50, 0), padx=20)
    etiquetaTableroUsuario = Label(contenedorUsuario, text="Mi Tablero")
    etiquetaTableroUsuario.grid(row=0, column=0, sticky=NW)
    contenedorTableroUsuario = Frame(contenedorUsuario)
    contenedorTableroUsuario.grid(row=1, column=1)

    # Insertar matriz de botones en el tablero
    for fila in range(len(matrizTableroUsuario)):
        for columna in range(len(matrizTableroUsuario[fila])):
            boton = Button(contenedorTableroUsuario, text="   ", padx=6, pady=4)
            boton.grid(row=fila, column=columna, padx=5, pady=5)
            matrizTableroUsuario[fila][columna] = boton

    for barco in dicPosicionesBarcos:
        for tipoDeBarco in informacionBarcos:
            if barco == tipoDeBarco[1]:
                for posicion in dicPosicionesBarcos[barco]:
                    matrizTableroUsuario[posicion[0]][posicion[1]].config(text=tipoDeBarco[0], bg=tipoDeBarco[2])

    contenedorEstatusUsuario = Frame(contenedorUsuario)
    contenedorEstatusUsuario.grid(row=2, column=0)
    etiquetaEstatusUsuario = Label(contenedorEstatusUsuario, text="Mi Estatus", justify=LEFT)
    etiquetaEstatusUsuario.grid(row=0, column=0, sticky=W)

    estatusUsuario = {
        "Portaviones": "Sin daño",
        "Acorazado": "Sin daño",
        "Buque de Guerra": "Sin daño",
        "Submarino": "Sin daño",
        "Destructor": "Sin daño"
    }

    contador = 1
    for barco in estatusUsuario:
        texto = barco + ": " + estatusUsuario[barco]
        etiquetaEstatus = Label(contenedorEstatusUsuario, text=texto, justify=LEFT)
        etiquetaEstatus.grid(row=contador, column=0, sticky=W)
        contador += 1

    # TODO: Insertar el resto de la pantalla de juego

    # boton = Button(root, text="Continuar", command=lambda: cargarPantallaFinJuego(root))
    # boton.grid(row=0, column=0)

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
matrizTableroBot = [[str(i) + str(j) for j in range(10)] for i in range(10)]
informacionBarcos = [
    ("", "Espacio sin tocar", ""),
    ("1", "Portaviones", "blue", 5),
    ("2", "Acorazado", "yellow", 4),
    ("3", "Buque de Guerra", "magenta", 3),
    ("4", "Submarino", "cyan", 3),
    ("5", "Destructor", "grey", 2)
]
dicInstrucciones = {"Horizontal": True, "Vertical": False, "Positivo": True, "Negativo": False, "Barco": "Portaviones"}
dicPosicionesBarcos = {"Portaviones": [], "Acorazado": [],"Buque de Guerra": [], "Submarino": [], "Destructor": []}
# Inicio del juego
cargarPantallaInicio()