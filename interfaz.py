import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import tiposDeAtaques as tda
import funcionesAuxiliares as fa
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
    global ventanaRoot
    global matrizTableroUsuario
    global matrizTableroBot
    global informacionBarcos
    global dicInstrucciones
    global dicPosicionesBarcos
    global dicPosicionesBarcosBot
    global disparoSeleccionado
    global posicionAfectada
    global ataquesDisponiblesUsuario
    global ataquesDisponiblesBot
    global estatusActualUsuario
    global estatusActualBot

    ventanaRoot.destroy()
    # ventanaRoot = tkinter.Tk()
    matrizTableroUsuario = [[0 for j in range(10)] for i in range(10)]
    matrizTableroBot = [[0 for j in range(10)] for i in range(10)]
    informacionBarcos = [
        ("", "Espacio sin tocar", "white"),
        ("1", "Portaviones", "blue", 5),
        ("2", "Acorazado", "yellow", 4),
        ("3", "Buque de Guerra", "magenta", 3),
        ("4", "Submarino", "cyan", 3),
        ("5", "Destructor", "grey", 2)
    ]
    dicInstrucciones = {"Horizontal": True, "Vertical": False, "Positivo": True, "Negativo": False, "Barco": "Portaviones"}
    dicPosicionesBarcos = {"Portaviones": [], "Acorazado": [], "Buque de Guerra": [], "Submarino": [], "Destructor": []}
    dicPosicionesBarcosBot = bot.posicionarBarcos()
    disparoSeleccionado = {"Disparo": "Unico"}
    posicionAfectada = []
    ataquesDisponiblesUsuario = {"Misil": 0, "Bomba": 0}
    ataquesDisponiblesBot = {"Misil": 0, "Bomba": 0}
    estatusActualUsuario = {}
    estatusActualBot = {
        "Posiciones": {"Portaviones": [], "Acorazado": [], "Buque de Guerra": [], "Submarino": [], "Destructor": []}
    }
    ventanaRoot = tkinter.Tk()
    ventanaRoot.title("BattleShip v1.0.0")
    # Insertar imagen background
    backgroundCanvas = Canvas(ventanaRoot, width=602, height=390)
    backgroundCanvas.grid(row=0, column=0)
    imagenBackground = ImageTk.PhotoImage(Image.open("background.jpg"))
    backgroundCanvas.create_image(0, 0, anchor=NW, image=imagenBackground)
    boton = Button(ventanaRoot, text="Jugar", command=lambda: cargarPantallaConfiguracion())
    boton.grid(row=0, column=0, sticky=NW)
    boton.config(font=("helvetica", 20, "underline italic"))
    ventanaRoot.mainloop()


def cargarPantallaConfiguracion():
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
    global ventanaRoot

    ventanaRoot.destroy()
    ventanaRoot = tkinter.Tk()
    ventanaRoot.title("BattleShip - Configuración")
    contenedorTablero = Frame(ventanaRoot)
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
    contenedorSimbologia = Frame(ventanaRoot)
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
    contenedorOpciones = Frame(ventanaRoot)
    contenedorOpciones.grid(row=1, column=1)
    etiquetaOpciones = Label(contenedorOpciones, text="Configurar tablero")
    etiquetaOpciones.grid(row=0, column=0, pady=(0, 15))
    etiquetaAgregar = Label(contenedorOpciones, text="Añadir")
    etiquetaAgregar.grid(row=1, column=0)
    # Crear menu despegable
    variableMenuDesple = StringVar()
    menuDesplegable = ttk.Combobox(contenedorOpciones, state="readonly", textvariable=variableMenuDesple)
    menuDesplegable["values"] = ["Portaviones", "Acorazado", "Buque de Guerra", "Submarino", "Destructor"]
    menuDesplegable.grid(row=1, column=1, padx=20)
    menuDesplegable.current(0)
    cambioTipoDeBarco = lambda evento: dicInstrucciones.update({"Barco": variableMenuDesple.get()})
    menuDesplegable.bind("<<ComboboxSelected>>", cambioTipoDeBarco)

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
        radioButton = Radiobutton(contenedorOpciones, text=text, variable=variable, value=valor,
        command=lambda direccion=text: configurarDirecciones(direccion))
        radioButton.grid(row=fila, column=columna, padx=20, pady=10)

    botonJugar = Button(ventanaRoot, text="Continuar", command=lambda: validarBarcosPosicionados())
    botonJugar.grid(row=1, column=0, sticky=SW)
    botonJugar.config(font=("helvetica", 12, "underline"))
    ventanaRoot.mainloop()


def posicionarBarco(evento):
    """Posiciona el barco en el tablero del usuario

    Entradas:
        evento: Es un objeto que representa el evento de un click de un botón
        en la interfaz
    Precondiciones:
        No hay
    Salidas:
        No retorna nada
    Proceso:
        1. Se inicializan variables para la información del barco seleccionado
        2. Se obtiene la información del barco seleccionado con un ciclo for
        3. Se valida mediante un condicional si es válida la posición del barco
        4. Mediante se posiciona el barco dependiendo de la configuración actual
    """
    global dicInstrucciones
    global informacionBarcos
    global matrizTableroUsuario
    global dicPosicionesBarcos

    posicionBarco = []
    # Obtener información del barco
    informacionBarco = {"espacios": 0, "color": "", "numero": ""}
    barcoActual = dicInstrucciones["Barco"]
    for barco in informacionBarcos:
        if barco[1] == barcoActual:
            informacionBarco["espacios"] = barco[3]
            informacionBarco["color"] = barco[2]
            informacionBarco["numero"] = barco[0]
    boton = evento.widget
    infoPosicion = boton.grid_info()
    posicionActual = (infoPosicion["row"], infoPosicion["column"])

    if  validarPosicionEnMatriz(posicionActual, barcoActual):
        if dicInstrucciones["Horizontal"]:
            if dicInstrucciones["Positivo"]:
                for i in range(informacionBarco["espacios"]):
                    matrizTableroUsuario[posicionActual[0]][posicionActual[1] + i]\
                        .config(bg=informacionBarco["color"], text=informacionBarco["numero"])
                    posicionBarco += [[posicionActual[0]] + [posicionActual[1] + i]]
                dicPosicionesBarcos[barcoActual] = posicionBarco
            else:
                for i in range(informacionBarco["espacios"]):
                    matrizTableroUsuario[posicionActual[0]][posicionActual[1] - i]\
                        .config(bg=informacionBarco["color"], text=informacionBarco["numero"])
                    posicionBarco += [[posicionActual[0]] + [posicionActual[1] - i]]
                dicPosicionesBarcos[barcoActual] = posicionBarco
        else:
            if dicInstrucciones["Positivo"]:
                for i in range(informacionBarco["espacios"]):
                    matrizTableroUsuario[posicionActual[0] - i][posicionActual[1]]\
                        .config(bg=informacionBarco["color"], text=informacionBarco["numero"])
                    posicionBarco += [[posicionActual[0] - i] + [posicionActual[1]]]
                dicPosicionesBarcos[barcoActual] = posicionBarco
            else:
                for i in range(informacionBarco["espacios"]):
                    matrizTableroUsuario[posicionActual[0] + i][posicionActual[1]]\
                        .config(bg=informacionBarco["color"], text=informacionBarco["numero"])
                    posicionBarco += [[posicionActual[0] + i] + [posicionActual[1]]]
                dicPosicionesBarcos[barcoActual] = posicionBarco


def validarPosicionEnMatriz(posicion, barcoActual):
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
        if len(dicPosicionAnterior[barcoActual]) != 0 :
            for i in dicPosicionAnterior[barcoActual]:
                matrizTableroUsuario[i[0]][i[1]].config(bg="white", text="   ")
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
                return validarColisionDeBarcos(posicion)
            else:
                messagebox.showerror("ERROR", "El barco seleccionado no puede ser posicionado segun la configuracion"
                                    + "solicitada, seleccione una configuracion diferente")
                return infoBarcos["Posicion"]


def validarColisionDeBarcos(posicion):
    """Valida la colision de barcos en su configuracion

    Entradas:
        posicion
    Precondiciones:
        No hay
    Salidas:
        Verdadero si se puede colocar el barco y false si no se puede colocar porque sucede
        una colision
    Proceso:
        1.Primero se utiliza una subfuncion o funcion auxiliar para saber la posicion futura
        que tendra el barco seleccionado
        2.Luego se itera en las posiciones de los barco excepto el barco seleccionado y si en
        alguna posicion hay coincidencia muestra un mensaje al usuario para informarle
    """
    def revisarPosicionFutura(posicionActual):
        global informacionBarcos
        global matrizTableroUsuario

        barcoActual = dicInstrucciones["Barco"]
        posicionFutura = []

        # Obtener información del barco, su largo, o sea la cantidad de espacios que utilizara
        largo = 0
        for barco in informacionBarcos:
            if barco[1] == barcoActual:
                largo = barco[3]

        if dicInstrucciones["Horizontal"]:
            if dicInstrucciones["Positivo"]:
                #Se obtiene la posicion futura en horizontal positivo
                for i in range(largo):
                    posicionFutura += [[posicionActual[0]] + [posicionActual[1] + i]]
                return posicionFutura
            else:
                # Se obtiene la posicion futura en horizontal negativo
                for i in range(largo):
                    posicionFutura += [[posicionActual[0]] + [posicionActual[1] - i]]
                return posicionFutura
        else:
            if dicInstrucciones["Positivo"]:
                # Se obtiene la posicion futura en vertical positivo
                for i in range(largo):
                    posicionFutura += [[posicionActual[0] - i ] + [posicionActual[1]]]
                return posicionFutura
            else:
                # Se obtiene la posicion futura en vertical negativo
                for i in range(largo):
                    posicionFutura += [[posicionActual[0] + i] + [posicionActual[1]]]
                return posicionFutura


    posicionFutura = revisarPosicionFutura(posicion)
    # Se itera en las posiciones de todos los barcos y en la posicion futura obtenida para saber si hay colision
    for llave in dicPosicionesBarcos:
        for contador in range(len(posicionFutura)):
            if posicionFutura[contador] in dicPosicionesBarcos[llave] and llave != dicInstrucciones["Barco"]:
                messagebox.showerror("ERROR",
                                     "El barco seleccionado no puede ser posicionado segun la posicion solicitada" \
                                     + ", seleccione una posicion diferente")
                return False
    return True


def validarBarcosPosicionados():
    """Valida si todos los barcos están posicionados en la interfaz

    Entradas:
        ventanaActual: La ventana actual que se está ejecutando
    Precondiciones:
        No hay
    Salidas:
        No retorna nada
    Proceso:
        1. Se itera sobre el diccionario de barcos
        2. Se verifica si el barco está posicionado
        3. Si lo está, se carga la pantalla de juego, de lo
        contrario se muestra un error
    """
    global dicPosicionesBarcos
    global ventanaRoot
    for i in dicPosicionesBarcos:
        if not dicPosicionesBarcos[i]:
            return messagebox.showerror("ERROR", "Debe configurar su tablero completamente para avanzar")
    cargarPantallaJuego()


def configurarDirecciones(direccion):
    """Configura las direcciones de configuración del barco que se va a
    posicionar

    Entradas:
        direccion: Es una hilera
    Precondiciones:
        direccion representa algún tipo de dirección el la configuración
    Salidas:
        No retorna nada
    Proceso:
        1. En el diccionario de instrucciones global se configura la
        dirección al valor True
        2. Con un condicional se verifica que no sea ""
        3. Dependiendo de su tipo de dirección, se configura su dirección
        opuesta como False
    """
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


def cargarPantallaJuego():
    """Cargar la pantalla de juego

     Entradas:
         No hay
     Precondiciones:
         No hay
     Salidas:
         No hay
     Proceso:
         1. Se llaman las variables globales requeridas
         2. Se carga la musica de fondo
         3. Se crea la ventana de juego
         4. Los contenedores del enemigo y del usuario
         5. Se cargan las matrices de tablero
         6. En los contenedores de estatus se colocan los estatus del enemigo y usuario
         7. Se hace el disparo con la funcionValidar tipo de ataque y de esta forma se
         van llamando a las demas funciones
    """
    global ventanaRoot
    global matrizTableroBot
    global matrizTableroUsuario
    global informacionBarcos
    global disparoSeleccionado
    global estatusActualBot
    global estatusActualUsuario
    # Cargar música
    pygame.init()
    pygame.mixer.music.load("musica.mp3")
    pygame.mixer.music.play()

    ventanaRoot.destroy()
    ventanaRoot = tkinter.Tk()
    ventanaRoot.title("BattleShip - Pantalla de Juego")

    etiquetaTurno = Label(ventanaRoot, text="Su Turno", font=("helvetica", 18, "underline italic"))
    etiquetaTurno.grid(row=0, column=0, sticky=W)

    contenedorTableros = Frame(ventanaRoot)
    contenedorTableros.grid(row=1, column=0, pady=30, sticky=N)

    contenedorEnemigo = Frame(contenedorTableros)
    contenedorEnemigo.grid(row=0, column=0)
    etiquetaTableroEnemigo = Label(contenedorEnemigo, text="Tablero Enemigo")
    etiquetaTableroEnemigo.grid(row=0, column=0, sticky=NW)

    contenedorTableroEnemigo = Frame(contenedorEnemigo)
    contenedorTableroEnemigo.grid(row=1, column=1, sticky=NW)
    # Crear tablero enemigo
    for fila in range(len(matrizTableroBot)):
        for columna in range(len(matrizTableroBot[fila])):
            boton = Button(contenedorTableroEnemigo, text="   ", padx=6, pady=4)
            matrizTableroBot[fila][columna] = boton
            boton.grid(row=fila, column=columna, padx=5, pady=5)
            boton.config(bg="white")
            boton.bind("<Button-1>", validarTipoDeAtaque)
    contenedorEstatusEnemigo = Frame(contenedorEnemigo)
    contenedorEstatusEnemigo.grid(row=2, column=0, columnspan=2, sticky=SW)
    etiquetaEstatusEnemigo = Label(contenedorEstatusEnemigo, text="Estatus Enemigo", justify=LEFT)
    etiquetaEstatusEnemigo.grid(row=0, column=0, sticky=W)
    estatusEnemigo = {
        "Portaviones": ("Posición Desconocida", "En pie", 5),
        "Acorazado": ("Posición Desconocida", "En pie", 4),
        "Buque de Guerra": ("Posición Desconocida", "En pie", 3),
        "Submarino": ("Posición Desconocida", "En pie", 3),
        "Destructor": ("Posición Desconocida", "En pie", 2)
    }

    contador = 1
    for barco in estatusEnemigo:
        texto = StringVar()
        textoContenido = barco + ": " + estatusEnemigo[barco][0] + ", " + estatusEnemigo[barco][1]
        texto.set(textoContenido)
        etiquetaEstatus = Label(contenedorEstatusEnemigo, textvariable=texto, justify=LEFT)
        etiquetaEstatus.grid(row=contador, column=0, sticky=SW)
        contador += 1
        estatusActualBot[barco] = [etiquetaEstatus ,estatusEnemigo[barco][2]]

    contenedorUsuario = Frame(contenedorTableros)
    contenedorUsuario.grid(row=0, column=1, sticky=W)
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
    # Configurar tablero con los barcos del usuario
    for barco in dicPosicionesBarcos:
        for tipoDeBarco in informacionBarcos:
            if barco == tipoDeBarco[1]:
                for posicion in dicPosicionesBarcos[barco]:
                    matrizTableroUsuario[posicion[0]][posicion[1]].config(text=tipoDeBarco[0], bg=tipoDeBarco[2])
    contenedorEstatusUsuario = Frame(contenedorUsuario)
    contenedorEstatusUsuario.grid(row=2, column=0, columnspan=2, sticky=SW)
    etiquetaEstatusUsuario = Label(contenedorEstatusUsuario, text="Mi Estatus", justify=LEFT)
    etiquetaEstatusUsuario.grid(row=0, column=0, sticky=W)

    estatusUsuario = {
        "Portaviones": ("Sin daño", 5),
        "Acorazado": ("Sin daño", 4),
        "Buque de Guerra": ("Sin daño", 3),
        "Submarino": ("Sin daño", 3),
        "Destructor": ("Sin daño", 2)
    }

    contador = 1
    for barco in estatusUsuario:
        texto = StringVar()
        textoContenido = barco + ": " + estatusUsuario[barco][0]
        texto.set(textoContenido)
        etiquetaEstatus = Label(contenedorEstatusUsuario, textvariable=texto, justify=LEFT)
        etiquetaEstatus.grid(row=contador, column=0, sticky=W)
        contador += 1
        estatusActualUsuario[barco] = [etiquetaEstatus, estatusUsuario[barco][1]]

    contenedorSimbologiaOpciones = Frame(ventanaRoot)
    contenedorSimbologiaOpciones.grid(row=1, column=1)

    contenedorSimbologia = Frame(contenedorSimbologiaOpciones)
    contenedorSimbologia.grid(row=0, column=0, sticky=N)
    etiquetaSimbologia = Label(contenedorSimbologia, text="Simbologia", justify=LEFT)
    etiquetaSimbologia.grid(row=0, column=0)
    simbologia = [
        (1, "Espacio Sin Tocar", "white","  "),
        (2, "Disparo Acertado", "green","  "),
        (3, "Disparo Fallido", "red","  "),
        (4, "Portaviones Sin Daño", "blue","1"),
        (5, "Portaviones Con Daño", "red","1"),
        (6, "Acorazado Sin Daño", "yellow","2"),
        (7, "Acorazado Con Daño", "red","2"),
        (8, "Buque de Guerra Sin Daño", "magenta","3"),
        (9, "Buque de Guerra con Daño", "red","3"),
        (10, "Submarino Sin Daño", "cyan","4"),
        (11, "Submarino con Daño", "red","4"),
        (12, "Destructor Sin Daño", "grey","5"),
        (13, "Destructor con Daño", "red","5")
    ]
    for fila in simbologia:
        boton = Button(contenedorSimbologia, text=fila[3], padx=4, pady=4)
        boton.config(bg=fila[2])
        boton.grid(row=fila[0], column=0, padx=10, pady=5)
        etiqueta = Label(contenedorSimbologia, text=fila[1], justify=LEFT)
        etiqueta.grid(row=fila[0], column=1, padx=10, sticky=W)

    contenedorOpciones = Frame(contenedorSimbologiaOpciones)
    contenedorOpciones.grid(row=1, column=0, sticky=NW)

    variableDisparo = BooleanVar()
    variableDisparo.set(0)
    etiquetaAccionesDisponible = Label(contenedorOpciones, text="Acciones Disponibles")
    etiquetaAccionesDisponible.grid(row=0,column=0, pady=5, sticky=W)
    disparos= ["Unico", "Misil", "Bomba"]
    for i in range(3):
        disparoBoton = Radiobutton(contenedorOpciones, text="Disparo " + disparos[i], variable=variableDisparo,
                                   value=i, command=lambda disp=disparos[i]: actualizarDisparo(disp))
        disparoBoton.grid(row=i+1, column=0, pady=3, sticky=W)
    botonAbandonar = Button(contenedorOpciones, text="Abandonar", command=lambda: ventanaRoot.destroy())
    botonAbandonar.grid(row=4, column=0, pady=5)
    ventanaRoot.mainloop()


def validarTipoDeAtaque(evento):
    """Valida la recarga de los ataques

    Entradas:
        Evento
    Precondiciones:
        No hay
    Salidas:
        No hay
    Proceso:
        1.se llaman la variable global requerida
        2.se valida el tipo de ataque seleccionado
        3.si el ataque es el de bomba se valida si tiene igual o mas de 5 turnos desde la ultima vez
          utilizado este ataque se resetea su contador y se le suma uno al ataque de misil
        4.si el ataque es el de misil se valida si tiene igual o mas de 3 turnos desde la ultima vez, se llama la
         funcion ataqueEnemigo y se le envia evento
          utilizado este ataque se resetea su contador y se le suma uno al ataque de bomba, se llama la funcion
          ataqueEnemigo y se le envia evento
        5 .si el ataque es el ataque unico se le suma un 1 a los contadores de misil, bomba, se llama la funcion
          ataqueEnemigo y se le envia evento
        6. si no cumplen las validaciones se le hace saber al usuario la cantidad de turnos que debe esperar
        y cuantos lleva hasta ese momento
    """
    global ataquesDisponiblesUsuario

    if disparoSeleccionado["Disparo"] == "Bomba":
        if ataquesDisponiblesUsuario["Bomba"] == 5:
            ataquesDisponiblesUsuario["Bomba"] = 0
            ataqueAlEnemigo(evento)
            if ataquesDisponiblesUsuario["Misil"] < 3:
                ataquesDisponiblesUsuario["Misil"] += 1
        else:
            messagebox.showinfo("Recarga", "La bomba tiene un tiempo de recarga de 5 turnos y lleva " + \
                                str(ataquesDisponiblesUsuario["Bomba"]))
    elif disparoSeleccionado["Disparo"] == "Misil":
        if ataquesDisponiblesUsuario["Misil"] == 3:
            ataquesDisponiblesUsuario["Misil"] = 0
            ataqueAlEnemigo(evento)
            if ataquesDisponiblesUsuario["Bomba"] < 5:
                ataquesDisponiblesUsuario["Bomba"] += 1
        else:
            messagebox.showinfo("Recarga", "El misil tiene un tiempo de recarga de 3 turnos y lleva " + \
                                str(ataquesDisponiblesUsuario["Misil"]))
    elif disparoSeleccionado["Disparo"] == "Unico":
        ataqueAlEnemigo(evento)
        if ataquesDisponiblesUsuario["Bomba"] < 5:
            ataquesDisponiblesUsuario["Bomba"] += 1
        if ataquesDisponiblesUsuario["Misil"] < 3:
            ataquesDisponiblesUsuario["Misil"] += 1


def ataqueAlEnemigo(evento):
    """Valida el tipo ataque hacia el enemigo

    Entradas:
        evento, el cual se utilizara como posicion inicial del ataque
    Precondiciones:
        No hay
    Salidas:
        No hay
    Proceso:
        1. Se llaman las variables globales requeridas
        2. Obtener la grid.info del evento y convertirla en una posicion de lista
        3. Validar sobre cual tipo de ataque se solicita y de estar recargado o bien sea el disparo
           unico se llama la funcion correspondiente del archivo tiposDeAtaques referenciada como tda
        4. Se guardan las posiciones afectadas en la variable global posicionAfectada
        5. Se llama la fincion validacionAtaqueAcertado
    """
    global disparoSeleccionado
    global matrizTableroBot
    global posicionAfectada
    global ataquesDisponiblesBot

    boton = evento.widget
    infoPosicion = boton.grid_info()
    posicionActual = [infoPosicion["row"], infoPosicion["column"]]

    if disparoSeleccionado["Disparo"] == "Bomba":
        posicionAfectada += tda.disparoBomba(posicionActual, matrizTableroBot)
    elif disparoSeleccionado["Disparo"] == "Misil":
        posicionAfectada += tda.disparoMisil(posicionActual, matrizTableroBot)
    elif disparoSeleccionado["Disparo"] == "Unico":
        posicionAfectada += tda.disparoUnico(posicionActual, matrizTableroBot)
    validarAtaqueAcertado()
    posicionAtacada = bot.atacarUsuario(matrizTableroUsuario, ataquesDisponiblesBot)
    validarAtaqueAcertadoBot(posicionAtacada)
    revisarGanador()


def revisarGanador():
    """Valida si hay un ganador

    Entradas:
        No hay
    Precondiciones:
        No hay
    Salidas:
        No hay
    Proceso:
        1. Se llaman las variables globales requeridas
        2. se crea un conjunto para guardar los barcos que hayan sidos destruidos totalmente
        3. Se itera y se guardan en el conjunto los barcos hundidos
        4. si hay un total de 5 barcos se da un ganador
    """
    global ventanaRoot
    global dicPosicionesBarcos
    global dicPosicionesBarcosBot

    flotaDestruida = set()
    # Revisar flota del usuario
    for barco in dicPosicionesBarcos:
        if not dicPosicionesBarcos[barco]:
            flotaDestruida.add(barco)
    if len(flotaDestruida) == 5:
        cargarPantallaFinJuego(False)
    flotaDestruida.clear()
    # Revisar flota del bot
    for barco in dicPosicionesBarcosBot:
        if not dicPosicionesBarcosBot[barco]:
            flotaDestruida.add(barco)
    if len(flotaDestruida) == 5:
        cargarPantallaFinJuego(True)


def validarAtaqueAcertado():
    """Valida los ataques realizados por la funcion ataqueAlEnemigo

    Entradas:
        No hay
    Precondiciones:
        No hay
    Salidas:
        No hay
    Proceso:
        1. Se llaman la variables globales requeridas
        2. Se itera en el diccionario de posiciones de los barcos del bot
        3. Se itera en la lista de listas donde se encuentran las posiciones afectadas por
        algun tipo de ataque
        4. Se valida si hay un barco del bot en una posicion afectada y si es asi se cambia
        su color a verde
        5. Si la posicion se ve afectada se borra y se guarda en el estatus actual del bot para se
        presentadas luego
    """
    global posicionAfectada
    global dicPosicionesBarcosBot
    global matrizTableroBot
    global estatusActualBot

    for i in dicPosicionesBarcosBot:
        for j in posicionAfectada:
            if j in dicPosicionesBarcosBot[i]:
                matrizTableroBot[j[0]][j[1]].config(bg="green")
                dicPosicionesBarcosBot[i].remove(j)
                estatusActualBot["Posiciones"][i] += [j]
                actualizarEstatusBot(i)
            else:
                if j in estatusActualBot["Posiciones"][i]:
                    matrizTableroBot[j[0]][j[1]].config(bg="green")
    posicionAfectada = []


def validarAtaqueAcertadoBot(posicionDisparada):
    """Valida los ataques realizados por la funcion ataqueAlEnemigo

    Entradas:
        Posicion del disparo
    Precondiciones:
        No hay
    Salidas:
        No hay
    Proceso:
        1.Se llaman la variables globales requeridas
        2.Se itera en el diccionario de posiciones de los barcos del bot
        3.se itera en la lista de listas donde se encuentran las posiciones afectadas por
          algun tipo de ataque
        4.Se valida si hay un barco del bot en una posicion afectada y si es asi se cambia
         su color a verde
        5.La posicion afectada se borra del dic de posiciones para evitar validaciones repetidas
    """
    global dicPosicionesBarcos
    global matrizTableroUsuario

    for i in dicPosicionesBarcos:
        for j in posicionDisparada:
            if j in dicPosicionesBarcos[i]:
                dicPosicionesBarcos[i].remove(j)
                actualizarEstatusUsuario(i)


def actualizarDisparo(tipoDisparo):
    """Valida el tipo ataque hacia el enemigo

    Entradas:
        tipo de disparo
    Precondiciones:
        No hay
    Salidas:
        No hay
    Proceso:
        1. Se llaman las variables globales requeridas
        2. Se actualiza disparo selccionado por el disparo recibido
    """
    global disparoSeleccionado
    disparoSeleccionado["Disparo"] = tipoDisparo


def cargarPantallaFinJuego(usuarioGana):
    """Pantalla de fin de juego

    Entradas:
        Si el usuario es ganador en valor booleano
    Precondiciones:
        No hay
    Salidas:
        No hay
    Proceso:
        1.Se llaman las variables globales requeridas
        2.Se destruye la ventana anterior
        3.Se carga la ventana con la imagen, boton de salir y volver al inicio
        4.Si el usuario es le ganador se muestra un label con la palabra ganador de lo contrario
        se muestra perdedor
    """
    global ventanaRoot
    ventanaRoot.destroy()
    ventanaRoot = tkinter.Tk()
    ventanaRoot.title("Fin de juego")

    backgroundCanvas = Canvas(ventanaRoot, width=602, height=390)
    backgroundCanvas.grid(row=0, column=0)
    # Insertar imagen background
    imagenBackground = ImageTk.PhotoImage(Image.open("background.jpg"))
    backgroundCanvas.create_image(0, 0, anchor=NW, image=imagenBackground)

    botonSalir = Button(ventanaRoot, text="Salir", command=lambda: ventanaRoot.destroy())
    botonSalir.grid(row=0, column=0, sticky=SE)
    botonSalir.config(font=("helvetica", 20, "underline italic"))
    botonVolverInicio = Button(ventanaRoot, text="Volver al Inicio", command=lambda: cargarPantallaInicio())
    botonVolverInicio.grid(row=0, column=0, sticky=NW)
    botonVolverInicio.config(font=("helvetica", 20, "underline italic"))

    if usuarioGana:
        etiquetaGanador = Label(ventanaRoot, text="Ganador", anchor=W)
        etiquetaGanador.config(font=("helvetica", 35, "underline italic"))
        etiquetaGanador.grid(row=0, column=0, pady=10)
    else:
        etiquetaGanador = Label(ventanaRoot, text="Perdedor", anchor=W)
        etiquetaGanador.config(font=("helvetica", 35, "underline italic"))
        etiquetaGanador.grid(row=0, column=0, pady=10)

    ventanaRoot.mainloop()


def actualizarEstatusBot(barco):
    """Cambia el estatus de los barcos

    Entradas:
        barco
    Precondiciones:
        No hay
    Salidas:
        No hay
    Proceso:
        1. Se llaman las variables globales requeridas
        2. Si el barco afectado aun tiene posiciones se le resta una
        3. Si el barco afectado se queda sin posiciones se cambia su estatus a hundido
        """
    global estatusActualBot
    if estatusActualBot[barco][1] > 1:
        estatusActualBot[barco][1] -= 1
    else:
        texto = StringVar()
        coordenadasBarco = fa.formatearParesOrdenados(estatusActualBot["Posiciones"][barco])
        texto.set(barco + ": Ubicacion: " + coordenadasBarco + ", hundido")
        estatusActualBot[barco][0].config(textvariable=texto)


def actualizarEstatusUsuario(barco):
    """Cambia el estatus de los barcos

     Entradas:
         barco
     Precondiciones:
         No hay
     Salidas:
         No hay
     Proceso:
         1. Se llaman las variables globales requeridas
         2. Si el barco afectado aun tiene posiciones se le resta una
         3. Si el barco afectado se queda sin posiciones se cambia su estatus a hundido
    """
    global dicPosicionesBarcos
    global estatusActualUsuario
    if estatusActualUsuario[barco][1] > 1:
        estatusActualUsuario[barco][1] -= 1
        texto = StringVar()
        texto.set(barco + ", dañado")
        estatusActualUsuario[barco][0].config(textvariable=texto)
    else:
        texto = StringVar()
        texto.set(barco + ", hundido")
        estatusActualUsuario[barco][0].config(textvariable=texto)


# Variables globales
ventanaRoot = tkinter.Tk()
matrizTableroUsuario = []
matrizTableroBot = []
informacionBarcos = []
dicInstrucciones = {}
dicPosicionesBarcos = {}
dicPosicionesBarcosBot = {}
disparoSeleccionado = {}
posicionAfectada = []
ataquesDisponiblesUsuario = {}
ataquesDisponiblesBot = {}
estatusActualUsuario = {}
estatusActualBot = {}
# Inicio del juego
cargarPantallaInicio()