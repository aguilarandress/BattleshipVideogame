def formatearParesOrdenados(paresOrdenados):
    """Formatea como una hilera la lista de pares ordenados

    Entradas:
        paresOrdenados: es una lista de listas
    Precondiciones:
        paresOrdenados tiene sublistas con dos números enteros
    Salidas:
        Retorna una hilera con los pares ordenados formateados correctamente
    Proceso:
        1. Se inicializa una variable resultado
        2. Se ordenan los pares ordenados
        3. Con ciclo for se va agregando el par ordenado con formato de hilera
        y se retorna el resultado
    """
    resultado = ""
    paresOrdenados = ordenarParesOrdenados(paresOrdenados)
    for parOrdenado in paresOrdenados:
        resultado += "(" + str(parOrdenado[0]) + ", " + str(parOrdenado[1]) + "), "
    return resultado[:-2]


def ordenarParesOrdenados(paresOrdenados):
    """Ordena los pares ordenados de forma ascendiente

    Entradas:
        paresOrdenados: es una lista de listas
    Precondiciones:
        paresOrdenados tiene sublistas con dos números enteros
    Salidas:
        Retorna las coordenadas ordenadas correctamente
    Proceso:
        1. Se verifica con un condicional y una variable si los pares
        ordenados están ordenados por filas o columnas
        2. En una variable de resultado se agregan aquellos números
        enteros que deben ser ordenados
        3. Se ordena de manera ascendiente la variable resultado
        4. Con un ciclo for se va agregando la parte de fila o columna
        que haga falta y se retorna el resultado
    """
    ordenadoPor = ("columnas", paresOrdenados[0][0])
    if paresOrdenados[0][1] == paresOrdenados[1][1]:
        ordenadoPor = ("filas", paresOrdenados[0][1])
    resultado = []
    for i in paresOrdenados:
        if ordenadoPor[0] == "columnas":
            resultado.append(i[1])
        else:
            resultado.append(i[0])
    resultado.sort()
    for i in range(len(resultado)):
        parOrdenado = [resultado[i]]
        if ordenadoPor[0] == "columnas":
            parOrdenado = [ordenadoPor[1]] + parOrdenado
        else:
            parOrdenado.append(ordenadoPor[1])
        resultado[i] = parOrdenado
    return resultado

