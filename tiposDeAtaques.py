import random


def disparoUnico(posicion, matrizTableroBot):
    """Ejecuta el disparo unico

    Entradas:
        posicion: es una lista
        matrizTableroBot: es una matriz
    Precondiciones:
        posicion es una lista de dos número enteros
        y matrizTableroBot es una matriz de botones
    Salidas:
        Retorna la posición afectada
    Proceso:
        1. La funcion cambia el color del boton seleccionado por el usuario por medio de la
        posicion obtenida como argumento
        2. retorna la posicion afectada para actualizar la variable global posicionAfectada
    """
    matrizTableroBot[posicion[0]][posicion[1]].config(bg="red")
    return [[posicion[0], posicion[1]]]


def disparoMisil(posicion, matrizTableroBot):
    """Ejecuta el disparo del misil

    Entradas:
        posicion: es una lista
        matrizTableroBot: es una matriz
    Precondiciones:
        posicion es una lista de dos número enteros
        y matrizTableroBot es una matriz de botones
    Salidas:
        Retorna la posición afectada
    Proceso:
        1. La funcion cambia el color del los botones desde la posicion seleccionada por el usuario
        dependiendo de los factores: horizontal, vertical, positivo y negativo. Dado de manera
        aleatoria por la libreria random
        2. Según la configuracion ejecuta una logica para evitar contadores fuera del rango de la matriz
        3. Según la configuracion dada por la libreria random se ejecuta una logica para 1 de los 4 posibles
        casos de configuracion
        4. Se cambia a color rojo las posiciones afectadas con iteracion que tiene el rango de los contadores
        anteriormente validados
        5. Finalmente se retorna las posiciones afectadas para actualizar la variable global
        posicionAfectada
    """
    # Posicionamiento de forma horizontal o no horizontal y  positivo o no positivo
    posicionamientoRandom = [True, True]
    casillaAfectada = []
    # Se configura la posicion de manera aleatoria del misil
    posicionamientoRandom[0] = random.choice([True, False])
    posicionamientoRandom[1] = random.choice([True, False])
    if posicionamientoRandom[0]:
        # Configuración igual a horizontal
        if posicionamientoRandom[1]:
            # Configuración igual a positivo
            # Posición seleccionada se le suma el largo de misil
            horiVertiFinal = posicion[1] + 3
            # Si el largo excede el rango de matriz se configura por defecto 10
            if horiVertiFinal > 9:
                horiVertiFinal = 10
            # Finalmente se iterea y se hacen los repectivos cambios
            # Se guardan y se retornan las posiciones afectadas
            for i in range(posicion[1], horiVertiFinal):
                matrizTableroBot[posicion[0]][i].config(bg="red")
                casillaAfectada.append([posicion[0], i])
            return casillaAfectada
        else:
            # Configuracion igual a negativo
            # Posicion seleccionada se le resta el largo de misil
            horiVertiInicio = posicion[1] - 3
            # Si el largo excede el rango de matriz se configura por defecto -1
            if horiVertiInicio < -1:
                horiVertiInicio = -1
            # Finalmente se iterea y se hacen los repectivos cambios
            # Se guardan y se retornan las posiciones afectadas
            for i in range(posicion[1], horiVertiInicio, -1):
                matrizTableroBot[posicion[0]][i].config(bg="red")
                casillaAfectada.append([posicion[0], i])
            return casillaAfectada
    else:
        # Configuracion igual a vertical
        if posicionamientoRandom[1]:
            # Configuracion igual a positivo
            # Posicion seleccionada se le resta el largo de misil
            horiVertiInicio = posicion[0] - 3
            # Si el largo excede el rango de matriz se configura por defecto -1
            if horiVertiInicio < -1:
                horiVertiInicio = -1
            # Finalmente se iterea y se hacen los repectivos cambios
            # Se guardan y se retornan las posiciones afectadas
            for i in range(posicion[0], horiVertiInicio, -1):
                matrizTableroBot[i][posicion[1]].config(bg="red")
                casillaAfectada.append([i, posicion[1]])
            return casillaAfectada
        else:
            # Configuracion igual a negativo
            # Posicion seleccionada se le suma el largo de misil
            horiVertiFinal = posicion[0] + 3
            # Si el largo excede el rango de matriz se configura por defecto 10
            if horiVertiFinal > 9:
                horiVertiFinal = 10
            # Finalmente se iterea y se hacen los repectivos cambios
            # Se guardan y se retornan las posiciones afectadas
            for i in range(posicion[0],horiVertiFinal):
                matrizTableroBot[i][posicion[1]].config(bg="red")
                casillaAfectada.append([i, posicion[1]])
            return casillaAfectada


def disparoBomba(posicion, matrizTableroBot):
    """Ejecuta el disparo de la bomba

    Entradas:
        posicion: es una lista
        matrizTableroBot: es una matriz
    Precondiciones:
        posicion es una lista de dos número enteros
        y matrizTableroBot es una matriz de botones
    Salidas:
        Retorna la posición afectada
    Proceso:
        1. La función cambia el color del los botones desde la posicion seleccionada por el usuario
        dependiendo de la posicion solicitada puesto que es una zona de 3x3
        2. Según la posicion se valida con una logica para evitar contadores fuera del rango de la matriz
        3. Se itera segun los rangos para los contadores ya validados y se va cambiando su color a rojo
        4. Finalmente se retorna las posiciones afectadas para actualizar la variable global
         posicionAfectada
    """
    casillaAfectada = []
    # rango de bomba; inicioFila, incicioCol, finFila, finCol
    zonaDeAtaque = [0, 0, 2, 2]
    if posicion[0] == 0:
        # Posicion seleccionada en fila igual a cero
        # Se configura rango de inicio y fin de fila desde la posicion seleccionada hasta 1
        # Total 2 espacios a la derecha
        zonaDeAtaque[0] = 0
        zonaDeAtaque[2] = 1
        if posicion[1] == 0:
            # Posicion seleccionada en columa igual a cero
            # Se configura inicio y fin de columna desde la posicion 0 y posicion 0 mas 1 para el final
            # Total de rango en columnas es 2 a la derecha
            zonaDeAtaque[1] = posicion[1]
            zonaDeAtaque[3] = posicion[1] + 1
        elif posicion[1] == 9:
            # Posicion seleccionada en columna igual a 9 (fin de tablero)
            # Se configura inicio de columna en la posicion menos 1 y fin la posicion seleccionada o sea 9
            # Total de rango en columnas es 2 a la izquierda
            zonaDeAtaque[1] = posicion[1] - 1
            zonaDeAtaque[3] = posicion[1]
        else:
            # Posicion seleccionada en columna no esta en los bordes
            # Se configura inicio de columna uno menos de la posicion seleccionada y uno mas para el final
            # Total de rango en columnas es 3
            zonaDeAtaque[1] = posicion[1] - 1
            zonaDeAtaque[3] = posicion[1] + 1
    elif posicion[0] == 9:
        # Posicion seleccionada en fila igual a 9
        # Se configura rango de inicio de fila desde la posicion seleccionada menos 1 y fin igual a la 9
        # Total 2 espacios a la izquierda
        zonaDeAtaque[0] = 8
        zonaDeAtaque[2] = 9
        if posicion[1] == 0:
            # Posicion seleccionada en columa igual a cero
            # Se configura inicio y fin de columna desde la posicion 0 y posicion 0 mas 1 para el final
            # Total de rango en columnas es 2 a la derecha
            zonaDeAtaque[1] = posicion[1]
            zonaDeAtaque[3] = posicion[1] + 1
        elif posicion[1] == 9:
            # Posicion seleccionada en columna igual a 9 (fin de tablero)
            # Se configura inicio de columna en la posicion menos 1 y fin la posicion seleccionada o sea 9
            # Total de rango en columnas es 2 a la izquierda
            zonaDeAtaque[1] = posicion[1] - 1
            zonaDeAtaque[3] = posicion[1]
        else:
            # Posicion seleccionada en columna no esta en los bordes
            # Se configura inicio de columna uno menos de la posicion seleccionada y uno mas para el final
            # Total de rango en columnas es 3
            zonaDeAtaque[1] = posicion[1] - 1
            zonaDeAtaque[3] = posicion[1] + 1
    else:
        # Posicion seleccionada en filas no esta en los bordes
        # Se configura inicio de filas uno menos de la posicion seleccionada y uno mas para el final
        # Total de rango en filas es 3
        zonaDeAtaque[0] = posicion[0] - 1
        zonaDeAtaque[2] = posicion[0] + 1
        if posicion[1] == 0:
            # Posicion seleccionada en columa igual a cero
            # Se configura inicio y fin de columna desde la posicion 0 y posicion 0 mas 1 para el final
            # Total de rango en columnas es 2 a la derecha
            zonaDeAtaque[1] = posicion[1]
            zonaDeAtaque[3] = posicion[1] + 1
        elif posicion[1] == 9:
            # Posicion seleccionada en columna igual a 9 (fin de tablero)
            # Se configura inicio de columna en la posicion menos 1 y fin la posicion seleccionada o sea 9
            # Total de rango en columnas es 2 a la izquierda
            zonaDeAtaque[1] = posicion[1] - 1
            zonaDeAtaque[3] = posicion[1]
        else:
            # Posicion seleccionada en columna no esta en los bordes
            # Se configura inicio de columna uno menos de la posicion seleccionada y uno mas para el final
            # Total de rango en columnas es 3
            zonaDeAtaque[1] = posicion[1] - 1
            zonaDeAtaque[3] = posicion[1] + 1

    # Finalmente se itera y se hacen los cambios en el tablero segun el inicio y fin de fila y columna respectivamente
    # Se guarda las posiciones afectadas para retornar dichas posiciones
    for fila in range(zonaDeAtaque[0], zonaDeAtaque[2] + 1):
        for col in range(zonaDeAtaque[1], zonaDeAtaque[3] + 1):
            matrizTableroBot[fila][col].config(bg="red")
            casillaAfectada += [[fila, col]]
    return casillaAfectada

