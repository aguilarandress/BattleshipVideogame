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
    Proceso:
        1. Se inicializan variables que contienen el resultado, los espacios que
        necesita el tipo de barco y las posiciones ya utilizadas
        2. Se itera sobre cada tipo de barco con un ciclo for
        3. Se utiliza un ciclo while para repetir el proceso n veces en caso de que
        alguna coordenada ya haya sido utilizada
        4. Se selecciona aleatoriamente si el barco va a ir en dirección horizontal
        o vertical mediante una variable que contiene un 1 o 2 y un condicional
        5. Con un ciclo for se van creando las coordenadas del barco
        6. Si la coordenada existe se sale del ciclo for y se inicia de cero
        en el ciclo while
    """
    posicionesBarcos = {"Portaviones": [], "Acorazado": [], "Buque de Guerra": [], "Submarino": [], "Destructor": []}
    espaciosDeBarcos = {"Portaviones": 5, "Acorazado": 4, "Buque de Guerra": 3, "Submarino": 3, "Destructor": 2}
    posicionesUtilizadas = ()
    # Para cada tipo de barco se crea una combinación de coordenadas para su posicionamiento
    # si alguna coordenada ya fue utilizada, se vuelve a crear de cero el set de coordenadas
    for barco in posicionesBarcos:
        while True:
            # 1 significa dirección horizontal y 2 vertical
            direccion = randint(1, 2)
            posicionRepetida = False
            if direccion == 1:
                # Información de las coordenadas del barco
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
                # Información de las coordenadas del barco
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
