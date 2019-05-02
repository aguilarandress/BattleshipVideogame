#funciones de validaciones

def configurarTablero(diccionario, posicion):
    listaOpciones = []
    contador = 0
    infoBarcos = {"Posicion" : False}
    #Configuracion para validacion de barcos seun su tipo se condiciona su posicion minima o maxima
    posConfigValidacion = (
        ("Portaviones", 3, 6),
        ("Acorazado", 2, 7),
        ("Buque de Guerra", 1, 8),
        ("Submarino", 1, 8),
        ("Destructor", 0, 9)
    )
    for i in diccionario:
        if diccionario[i]:
            contador +=1
            listaOpciones.append(i)

    for barco, posMin, posMax in posConfigValidacion:
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
        #TODO insertar cambio en la matriz dependiendo el tipo de barco...usar informacionBarcos
        print("Validacion Correcta")