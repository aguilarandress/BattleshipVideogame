

def disparoUnico(posicion, matrizTableroBot):

    matrizTableroBot[posicion[0]][posicion[1]].config(bg="red")



def disparoMisil(posicion,matrizTableroBot):
    matrizTableroBot[posicion[0]][posicion[1]].config(bg="red")


def disparoBomba(posicion,matrizTableroBot):

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



