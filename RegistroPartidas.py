import PySimpleGUI as sg
from datetime import date
import pickle
import os
import ScrabbleAR

nombre_archivo_rankings = 'ranking_nuevo'

def guardar_score (dificultad, nombre, puntos):
    '''guardo score en archivo ingresado como parametro'''
    dia = date.today().day
    mes = date.today().month
    ano = date.today().year
    nuevo_record = {'Nombre': nombre, 'Puntaje': puntos, 'Fecha': "{}/{}/{}".format(dia, mes, ano)}
    print(nuevo_record)
    try:
        try:
            file=open(nombre_archivo_rankings, 'rb')
            data = pickle.load(file)
        except(FileNotFoundError):
            file= open(nombre_archivo_rankings,'w')
            data={}
        data[dificultad].append(nuevo_record)
        print(data)
    except (KeyError):
        print("No record yet")
        data[dificultad]= [nuevo_record]
    file.close()
    with open(nombre_archivo_rankings, 'wb') as file:
        pickle.dump(data, file)
        file.close()



def ingresar_usuario():
    '''muestro una ventana para ingresar nombre de usuario. si no se ingresa se toma como nombre "anonimo"'''
    layout_ingreso_usuario = [
               [sg.Text('Ingrese un nombre de usuario: ', background_color=('#2C2C2C'), text_color='#E1BF56'), sg.InputText(key='usuario', background_color='#545454', text_color='#E1BF56')],
               [sg.Button('Aceptar', pad=(100,10), key='ok', button_color=('white', '#E1BF56'))]
    ]
    nombre = 'Anonimo'
    windowUs = sg.Window('Usuario', size=(350, 100), background_color='#2C2C2C').Layout(layout_ingreso_usuario)
    event, value = windowUs.Read()
    while True:
        if event == 'ok':
            nombre = value['usuario']
            windowUs.Close()
            break
        elif event == None:
            break
    return nombre

def mostrar_ranking(nivel):
    '''Muestro ranking '''
    diccionario_dificultad_según_boton = {'mejores_puestos_dif_facil': 'dificultad_facil',
                                          'mejores_puestos_dif_media': 'dificultad_media',
                                          'mejores_puestos_dif_maxima' : 'dificultad_maxima'
                                          }
    try:
        with open(nombre_archivo_rankings, 'rb') as f:
            datos = pickle.load(f)
            f.close()
        try:
            dificultad = diccionario_dificultad_según_boton[nivel]
            datos_a_imprimir = datos[dificultad]
            datos_a_imprimir = list(map( lambda x : list([x['Nombre'],x['Puntaje'], x['Fecha']]), datos_a_imprimir ))
            datos_a_imprimir = sorted(datos_a_imprimir,key= lambda x : x[1], reverse = True)
            for linea in datos_a_imprimir[:10]:
                print('Nombre: {}    Puntaje: {}    Fecha: {}'.format(linea[0],linea[1],linea[2]))
        except KeyError:
            print('No hay jugadores record en esta dificultad')
    except (FileNotFoundError, IOError):
        print("No record yet")


def ventana_Ganador(puntaje_jugador, puntaje_maquina, atril, atril_pc, puntaje_letras, nombre, nivel):
    '''organiza la ventana que muestra el ganador'''
    letter_atril = { 'size' : (3, 2), 'pad' : (0,0), 'button_color' : ('white', '#C8C652')}
    puntaje_letras_jugador = []
    puntaje_letras_pc = []
    for i in range(7):
        try:

            puntaje_letras_jugador.append(puntaje_letras[atril.get_espacio_fichas()[i].get_letra()])

            puntaje_letras_pc.append(puntaje_letras[atril_pc.get_espacio_fichas()[i].get_letra()])
        except KeyError:
            continue
    puntaje_final_jugador = puntaje_jugador - sum(puntaje_letras_jugador)
    puntaje_final_Pc = puntaje_maquina - sum(puntaje_letras_pc)
    guardar_score(nivel, nombre, puntaje_final_jugador)

    if (puntaje_final_jugador < puntaje_final_Pc):
        imagen = '/imagenes/perder.png'
    elif(puntaje_final_jugador > puntaje_final_Pc):
        imagen = '/imagenes/ganaste.png'
    else:
        imagen = '/imagenes/empataron.png'

    columna1_PC = [[sg.Button(button_text= atril_pc.get_espacio_fichas()[i].get_letra(), **letter_atril) for i in range(7)]]
    columna2_PC = [[sg.Text('Puntaje Final Pc', key='puntaje_pc', background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12))],
                   [sg.Text(puntaje_final_Pc, key='puntaje_final_pc', background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12))]]

    columna1_jugador = [[sg.Button(button_text= atril.get_espacio_fichas()[i].get_letra(), **letter_atril) for i in range(7)]]
    columna2_jugador = [[sg.Text('Puntaje Final Jugador', key='Puntaje_jugador', background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12))],
                        [sg.Text(puntaje_final_jugador, key='puntaje_final_jugador', background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12))]]

    layout = []
    layout.append([sg.Text('Atril PC', background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12))])
    layout.append([sg.Column(columna1_PC, background_color='#2C2C2C'), sg.Column(columna2_PC, background_color='#2C2C2C')])
    layout.append([sg.Image((os.getcwd()+imagen), size=(400,300), background_color='#2C2C2C')])
    layout.append([sg.Text('Atril Jugador', background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12))])
    layout.append([sg.Column(columna1_jugador, background_color='#2C2C2C'), sg.Column(columna2_jugador, background_color='#2C2C2C')])
    layout.append([sg.Button(key='quit', button_text='Salir', button_color=('white', '#E1BF56')), sg.Button(key='volver', button_text='Volver', button_color=('white', '#E1BF56'))])
    return layout


def muestra_Ganador(puntaje_jugador, puntaje_maquina, atril, atril_pc, puntajes_letras, nivel, nombre):
    '''imprime en una ventana quien fue el ganador y pone un menu para volver al juego'''
    windowTop = sg.Window('Final', background_color='#2C2C2C').Layout(ventana_Ganador(puntaje_jugador, puntaje_maquina, atril, atril_pc, puntajes_letras, nombre, nivel))
    while True:
        event, value = windowTop.Read()
        if (event == 'quit'):
            windowTop.Close()
            break

        elif event== 'volver':
            windowTop.Close()
            ScrabbleAR.main()
            break
