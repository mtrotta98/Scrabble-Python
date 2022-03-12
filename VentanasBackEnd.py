import RegistroPartidas
import PySimpleGUI as sg

def click_dificultad(window, evento, botones_dificultad, configuracion_partida, fichas_facil, fichas_media, fichas_maxima):
    ''' selecciona un boton de dificultad '''

    for boton in botones_dificultad.keys():
        if evento == boton:
            configuracion_partida[0] = evento
            configuracion_partida[2] = botones_dificultad[evento][0]
            configuracion_partida[4] = botones_dificultad[evento][1]
            window.Element(boton).Update(button_color=('white', 'black'))
        else:
            window.Element(boton).Update(button_color=('#FFFFFF', '#545454'))


def click_tiempo_turno(window, evento, botones_tiempo_turno, configuracion_partida):
    ''' Selecciona  un tiempo de juego '''
    diccionario_tiempo_turnos = {'tiempo_turno_30_seg': 30, 'tiempo_turno_60_seg': 60, 'tiempo_turno_90_seg': 90}
    for boton in botones_tiempo_turno:
        if evento == boton:
            configuracion_partida[1] = diccionario_tiempo_turnos[evento]
            window.Element(boton).Update(button_color=('white', 'black'))
        else:
            window.Element(boton).Update(button_color=('#FFFFFF', '#545454'))


def click_tiempo_partida(window, evento, botones_tiempo_partida, configuracion_partida):
    '''Selecciona un tiempo de partida'''
    diccionario_tiempo_partida = {'tiempo_partida_5_min': 320, 'tiempo_partida_10_min': 620, 'tiempo_partida_15_min': 920}
    for boton in botones_tiempo_partida:
        if evento == boton:
            configuracion_partida[3] = diccionario_tiempo_partida[evento]
            window.Element(boton).Update(button_color=('white', 'black'))
        else:
            window.Element(boton).Update(button_color=('#FFFFFF', '#545454'))


def click_mejores_puestos(window, evento, botones_mejores_puestos):
    ''' muestra los mejores puestos'''
    for boton in botones_mejores_puestos:
        if evento == boton:
            RegistroPartidas.mostrar_ranking(boton)
            window.Element(boton).Update(button_color=('white', 'black'))


        else:
            window.Element(boton).Update(button_color=('#FFFFFF', '#545454'))


def ventanaConfig():
    ABC = 'ABCDEFGHIJKLMN'
    columna1 = []
    for letra in ABC:
        lista = [sg.Text(letra + ':', background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12)), sg.InputText('Cantidad', key=(letra, 1), size=(5, 5), background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12)),
                 sg.InputText('Valor', key=(letra, 2), size=(5, 5), background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12))]
        columna1.append(lista)

    columna2 = []
    ABC2 = 'OPQRSTUVWXYZ'
    for letra in ABC2:
        lista = [sg.Text(letra + ':', background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12)), sg.InputText('Cantidad', key=(letra, 1), size=(5, 5), background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12)),
                 sg.InputText('Valor', key=(letra, 2), size=(5, 5), background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12))]
        columna2.append(lista)

    layout = [[sg.Column(columna1, background_color='#2C2C2C'), sg.Column(columna2, background_color='#2C2C2C')],
              [sg.Button(button_text='ACEPTAR', key=('ACEPTAR'), button_color=('white', '#E1BF56')),
               sg.Button(button_text='CANCELAR', key=('CANCELAR'), button_color=('white', '#E1BF56'))
               ]
              ]

    window = sg.Window('Scrabble', background_color='#2C2C2C').Layout(layout)
    diccionario = {}

    while True:
        event, values = window.Read(timeout=0)

        if event == 'ACEPTAR':
            abc=ABC+ABC2
            for letra in abc:

                try:
                    valor1 = int(values[letra, 1])
                except ValueError:
                    valor1 = 0

                try:
                    valor2 = int(values[letra, 2])
                except ValueError:
                    valor2 = 0

                diccionario[letra] = (valor1, valor2)
            window.close()
            return diccionario
        elif event == "CANCELAR":
            window.close()
            return False



