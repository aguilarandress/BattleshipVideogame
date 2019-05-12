import random
def disparoUnico(posicion, matrizTableroBot):
    """Ejecuta el disparo unico

        Entradas:
            posicion y tablero del bot
        Precondiciones:
            No hay
        Salidas:
            la posicion afectada
        Proceso:
            1.La funcion cambia el color del boton seleccionado por el usuario por medio de la
            posicion obtenida como argumento
            2.retorna la posicion afectada para actualizar la variable global posicionAfectada
        """
    matrizTableroBot[posicion[0]][posicion[1]].config(bg="red")
    return [[posicion[0], posicion[1]]]

def disparoMisil(posicion,matrizTableroBot):
    """Ejecuta el disparo del misil

        Entradas:
            posicion y tablero del bot
        Precondiciones:
            No hay
        Salidas:
            la posicion afectada
        Proceso:
            1.La funcion cambia el color del los botones desde la posicion seleccionada por el usuario
              dependiendo de los factores: horizontal, vertical, positivo y negativo. Dado de manera
              aleatoria por la libreria random
            2.Segun la configuracion ejecuta una logica para evitar contadores fuera del rango de la matriz
            3.Segun la configuracion dada por la libreria random se ejecuta una logica para 1 de los 4 posibles
              casos de configuracion
            4.Se cambia a color rojo las posiciones afectadas con iteracion que tiene el rango de los contadores
              anteriormente validados
            5.finalmente se retorna las posiciones afectadas para actualizar la variable global
             posicionAfectada
        """
    # posicionamiento de forma horizontal o no horizontal y  positivo o no negativo
    posicionamientoRandom = [True, True]
    casillaAfectada = []
    posicionamientoRandom[0] = random.choice([True, False])
    posicionamientoRandom[1] = random.choice([True, False])
    if posicionamientoRandom[0]:
        if posicionamientoRandom[1]:
            horiVertiFinal = posicion[1] + 3
            if horiVertiFinal > 9:
                horiVertiFinal = 10
            for i in range(posicion[1],horiVertiFinal):
                matrizTableroBot[posicion[0]][i].config(bg="red")
                casillaAfectada.append([posicion[0],i])
            return casillaAfectada
        else:
            horiVertiInicio = posicion[1] - 3
            if horiVertiInicio < -1:
                horiVertiInicio = -1
            for i in range(posicion[1], horiVertiInicio, -1):
                matrizTableroBot[posicion[0]][i].config(bg="red")
                casillaAfectada.append([posicion[0],i])
            return casillaAfectada
    else:
        if posicionamientoRandom[1]:
            horiVertiInicio = posicion[0] - 3
            if horiVertiInicio < -1:
                horiVertiInicio = -1
            for i in range(posicion[0], horiVertiInicio, -1):
                matrizTableroBot[i][posicion[1]].config(bg="red")
                casillaAfectada.append([i,posicion[1]])
            return casillaAfectada
        else:
            horiVertiFinal = posicion[0] + 3
            if horiVertiFinal > 9:
                horiVertiFinal = 10
            for i in range(posicion[0],horiVertiFinal):
                matrizTableroBot[i][posicion[1]].config(bg="red")
                casillaAfectada.append([i,posicion[1]])
            return casillaAfectada

def disparoBomba(posicion,matrizTableroBot):
    """Ejecuta el disparo de la bomba

        Entradas:
            posicion y tablero del bot
        Precondiciones:
            No hay
        Salidas:
            la posicion afectada
        Proceso:
            1.La funcion cambia el color del los botones desde la posicion seleccionada por el usuario
              dependiendo de la posicion solicitada puesto que es una zona de 3x3
            2.Segun la posicion se valida con una logica para evitar contadores fuera del rango de la matriz
            3.Se itera segun los rangos para los contadores ya validados y se va cambiando su color a rojo
            3.finalmente se retorna las posiciones afectadas para actualizar la variable global
             posicionAfectada
        """
    casillaAfectada = []
    # rango de boma; inicioFila, incicioCol, finFila, finCol
    zonaDeAtaque = [0, 0, 2, 2]
    if posicion[0] == 0:
        zonaDeAtaque[0] = 0
        zonaDeAtaque[2] = 1
        if posicion[1] == 0:
            zonaDeAtaque[1] = posicion[1]
            zonaDeAtaque[3] = posicion[1] + 1
        elif posicion[1] == 9:
            zonaDeAtaque[1] = posicion[1] - 1
            zonaDeAtaque[3] = posicion[1]
        else:
            zonaDeAtaque[1] = posicion[1] - 1
            zonaDeAtaque[3] = posicion[1] + 1
    elif posicion[0] == 9:
        zonaDeAtaque[0] = 8
        zonaDeAtaque[2] = 9
        if posicion[1] == 0:
            zonaDeAtaque[1] = posicion[1]
            zonaDeAtaque[3] = posicion[1] + 1
        elif posicion[1] == 9:
            zonaDeAtaque[1] = posicion[1] - 1
            zonaDeAtaque[3] = posicion[1]
        else:
            zonaDeAtaque[1] = posicion[1] - 1
            zonaDeAtaque[3] = posicion[1] + 1
    else:
        zonaDeAtaque[0] = posicion[0] - 1
        zonaDeAtaque[2] = posicion[0] + 1
        if posicion[1] == 0:
            zonaDeAtaque[1] = posicion[1]
            zonaDeAtaque[3] = posicion[1] + 1
        elif posicion[1] == 9:
            zonaDeAtaque[1] = posicion[1] - 1
            zonaDeAtaque[3] = posicion[1]
        else:
            zonaDeAtaque[1] = posicion[1] - 1
            zonaDeAtaque[3] = posicion[1] + 1

    for fila in range(zonaDeAtaque[0], zonaDeAtaque[2] + 1):
        for col in range(zonaDeAtaque[1], zonaDeAtaque[3] + 1):
            matrizTableroBot[fila][col].config(bg="red")
            casillaAfectada += [[fila,col]]
    return casillaAfectada

