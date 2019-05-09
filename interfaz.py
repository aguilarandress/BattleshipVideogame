import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import tiposDeAtaques as tDA
import botContrincante as bot


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
            boton.config(bg="white")
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

    botonJugar = Button(root, text="Continuar", command=lambda: validacionCargarPantallaDeJuego(root))
    botonJugar.grid(row=1, column=0, sticky=SW)
    botonJugar.config(font=("helvetica", 12, "underline"))

    root.mainloop()


def validacionCargarPantallaDeJuego(ventana):
    global dicPosicionesBarcos
    for i in dicPosicionesBarcos:
        if not dicPosicionesBarcos[i]:
            return messagebox.showerror("ERROR", "Debe configurar su tablero completamente para avanzar")
    cargarPantallaJuego(ventana)


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
    global disparoSeleccionado

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
            boton = Button(contenedorTableroEnemigo, text="   ", padx=6, pady=4 )

            matrizTableroBot[fila][columna] = boton
            boton.grid(row=fila, column=columna, padx=5, pady=5)
            boton.config(bg="white")
            boton.bind("<Button-1>",ataqueAlEnemigo)

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
            boton.config(bg="white")
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

    contenedorSimbologiaOpciones = Frame(root)
    contenedorSimbologiaOpciones.grid(row=1, column=2, sticky=W)

    contenedorSimbologia = Frame(contenedorSimbologiaOpciones)
    contenedorSimbologia.grid(row=0, column=0, sticky=N)
    etiquetaSimbologia= Label(contenedorSimbologia, text="Simbologia")
    etiquetaSimbologia.grid(row=0, column=0, sticky=NW)
    simbologia = [
        (1,"Espacio Sin Tocar", "white","  "),
        (2,"Disparo Acertado", "green","  "),
        (3,"Disparo Fallido", "red","  "),
        (4,"Portaviones Sin Daño", "blue","1"),
        (5,"Portaviones Con Daño", "red","1"),
        (6,"Acorazado Sin Daño", "yellow","2"),
        (7,"Acorazado Con Daño", "yellow","2"),
        (8,"Buque de Guerra Sin Daño", "pink","3"),
        (9,"Buque de Guerra con Daño", "red","3"),
        (10,"Submarino Sin Daño", "cyan","4"),
        (11,"Submarino con Daño", "red","4"),
        (12,"Destructor Sin Daño", "grey","5"),
        (13,"Destructor con Daño", "red","5")
    ]
    for fila in simbologia:
        boton = Button(contenedorSimbologia,text=fila[3], padx=4, pady=4 )
        boton.config(bg=fila[2])
        boton.grid(row=fila[0], column=0, padx=10, pady=5)

        etiqueta = Label(contenedorSimbologia, text=fila[1] , justify= LEFT)
        etiqueta.grid(row=fila[0], column=1, padx=10, sticky=W)

    contenedorOpciones = Frame(contenedorSimbologiaOpciones)
    contenedorOpciones.grid(row=1, column=0, sticky=NW)

    variableDisparo = BooleanVar()
    variableDisparo.set(0)
    etiquetaAccionesDisponible = Label(contenedorOpciones, text="Acciones Disponibles")
    etiquetaAccionesDisponible.grid(row=0,column=0, pady=15, sticky=W)
    disparos= [
        ("Unico",),
        ("Misil",),
        ("Bomba",)
    ]
    for i in range(3):
        disparoBoton = Radiobutton(contenedorOpciones, text= "Disparo " + disparos[i][0], variable=variableDisparo, value=i,\
                    command=lambda disp = disparos[i][0] : actualizarDisparo(disp))
        disparoBoton.grid(row=i+1, column=0, pady=15, sticky=W)


    # boton = Button(root, text="Continuar", command=lambda: cargarPantallaFinJuego(root))
    # boton.grid(row=0, column=0)

    root.mainloop()


def actualizarDisparo(tipoDisparo):
    global disparoSeleccionado
    disparoSeleccionado["Disparo"] = tipoDisparo


def ataqueAlEnemigo(evento):
    global disparoSeleccionado
    global matrizTableroBot
    boton = evento.widget
    infoPosicion = boton.grid_info()

    posicionActual = [infoPosicion["row"], infoPosicion["column"]]

    if disparoSeleccionado["Disparo"] == "Bomba":
        tDA.disparoBomba(posicionActual, matrizTableroBot)
    elif disparoSeleccionado["Disparo"] == "Misil":
        tDA.disparoMisil(posicionActual, matrizTableroBot)
    elif disparoSeleccionado["Disparo"] == "Unico":
        tDA.disparoUnico(posicionActual, matrizTableroBot)
    else:
        messagebox.showinfo("a")


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
    ("", "Espacio sin tocar", "white"),
    ("1", "Portaviones", "blue", 5),
    ("2", "Acorazado", "yellow", 4),
    ("3", "Buque de Guerra", "magenta", 3),
    ("4", "Submarino", "cyan", 3),
    ("5", "Destructor", "grey", 2)
]
dicInstrucciones = {"Horizontal": True, "Vertical": False, "Positivo": True, "Negativo": False, "Barco": "Portaviones"}
dicPosicionesBarcos = {"Portaviones": [], "Acorazado": [],"Buque de Guerra": [], "Submarino": [], "Destructor": []}
disparoSeleccionado = {"Disparo": "Unico"}
# Inicio del juego
cargarPantallaInicio()