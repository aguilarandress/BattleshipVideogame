from random import randint


def posicionarBarcos():
    """Crea las posiciones de los barcos del bot contrincante de manera aleatoria

    Entradas:
        No hay
    Precondiciones:
        No hay
    Salidas:
        Retorna un diccionario con valores que contienen pares ordenados para
        las posiciones de cada barco
    """
    posicionesBarcos = {"Portaviones": [], "Acorazado": [], "Buque de Guerra": [], "Submarino": [], "Destructor": []}
    espaciosDeBarcos = {"Portaviones": 5, "Acorazado": 4, "Buque de Guerra": 3, "Submarino": 3, "Destructor": 2}
    posicionesUtilizadas = ()
    for barco in posicionesBarcos:
        while True:
            direccion = randint(1, 2)
            posicionRepetida = False
            if direccion == 1:
                espaciosDelBarco = espaciosDeBarcos[barco]
                fila = randint(0, 9)
                contador = randint(0, 9 - espaciosDelBarco)
                for i in range(espaciosDelBarco):
                    coordenada = [fila, contador]
                    if coordenada in posicionesUtilizadas:
                        posicionesBarcos[barco] = []
                        posicionRepetida = True
                        break
                    posicionesBarcos[barco].append(coordenada)
                    contador += 1
                    posicionesUtilizadas += (coordenada,)
                if posicionRepetida:
                    continue
                break
            else:
                espaciosDelBarco = espaciosDeBarcos[barco]
                columna = randint(0, 9)
                contador = randint(0, 9 - espaciosDelBarco)
                for i in range(espaciosDelBarco):
                    coordenada = [contador, columna]
                    if coordenada in posicionesUtilizadas:
                        posicionesBarcos[barco] = []
                        posicionRepetida = True
                        break
                    posicionesBarcos[barco].append(coordenada)
                    contador += 1
                    posicionesUtilizadas += (coordenada,)
                if posicionRepetida:
                    continue
                break
    return posicionesBarcos


# TODO: Implementar ataques del bot
