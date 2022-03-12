



def crear_bolsa_de_fichas (fichas):
    bolsa_de_fichas = []
    try:
        for key, value in fichas.items():
            for cantidad in range(value[0]):
                bolsa_de_fichas.append(key[0])
                bolsa_de_fichas.append(key[1])
    except(IndexError):
        for key in fichas.keys():
            for cantidad in range(fichas[key][0]):
                bolsa_de_fichas.append(key)

    return bolsa_de_fichas

def crear_diccionario_de_puntos(fichas):
    diccionario_de_puntos = dict()
    try:
        for key, value in fichas.items():
            diccionario_de_puntos[key[0]] = value[1]
            diccionario_de_puntos[key[1]] = value[1]

    except IndexError:
        for key in fichas.items():
            diccionario_de_puntos[key] = value[1]
            diccionario_de_puntos[key] = value[1]

    return diccionario_de_puntos

def crear_diccionario():
    lista_diccionario = []
    with open('diccionarios/diccionario.txt', 'r', encoding="cp437", errors='ignore') as file:
        for line in file:
            line = line.rstrip('\n')
            lista_diccionario.append(line)
    return lista_diccionario

