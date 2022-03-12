
import PySimpleGUI as sg
import VentanasBackEnd
import ProgramaPrincipal
import random
import os
def main():
    ancho_total = 120
    menu_def = [['Menu', ['Configuracion avanzada ']],
                ]
    layout_ventana_principal = [
        [sg.Menu(menu_def, tearoff=True)],
        [sg.Button('Jugar', key='jugar', pad=((0, 0), 10), size=(ancho_total + 8, 1), button_color=('white', '#E1BF56'))],
        [sg.Button('Cargar partida guardada', key='cargar', pad=((0, 0), 10), size=(ancho_total + 8, 1), button_color=('white', '#E1BF56'))],

        [sg.Text('Seleccione nivel de dificultad: ', background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12))],
        [sg.Button('Facil', key='dificultad_facil', pad=((0, 0), 10), size=(round(ancho_total /3), 1), button_color=('white', '#E1BF56')),
         sg.Button('Media', key='dificultad_media', pad=((0, 0), 10), size=(round(ancho_total /3), 1), button_color=('white', '#E1BF56')),
         sg.Button('Máxima', key='dificultad_maxima', pad=((0, 0), 10), size=(round(ancho_total /3), 1), button_color=('white', '#E1BF56'))],

        [sg.Text('Seleccione el tiempo por turno: ', background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12))],
        [sg.Button('30 seg', key='tiempo_turno_30_seg', pad=((0, 0), 10), size=(round(ancho_total /3), 1), button_color=('white', '#E1BF56')),
         sg.Button('60 seg', key='tiempo_turno_60_seg', pad=((0, 0), 10), size=(round(ancho_total /3), 1), button_color=('white', '#E1BF56')),
         sg.Button('90 seg', key='tiempo_turno_90_seg', pad=((0, 0), 10), size=(round(ancho_total /3), 1), button_color=('white', '#E1BF56'))],

        [sg.Text('Seleccione el tiempo de partida: ', background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12))],
        [sg.Button('5 min', key='tiempo_partida_5_min', pad=((0,0), 10), size=(round(ancho_total / 3), 1), button_color=('white', '#E1BF56')),
         sg.Button('10 min', key='tiempo_partida_10_min', pad=((0,0), 10), size=(round(ancho_total / 3), 1), button_color=('white', '#E1BF56')),
         sg.Button('15 min', key='tiempo_partida_15_min', pad=((0,0), 10), size=(round(ancho_total / 3), 1), button_color=('white', '#E1BF56'))],

        [sg.Text('Ver records por dificultad ', background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12))],
        [sg.Button('Mejores Puestos - Dificultad Facil', key='mejores_puestos_dif_facil', pad=((0, 0), 10), size=(round(ancho_total / 3), 1), button_color=('white', '#E1BF56')),
         sg.Button('Mejores Puestos - Dificultad Media', key='mejores_puestos_dif_media', pad=((0, 0), 10), size=(round(ancho_total / 3), 1), button_color=('white', '#E1BF56')),
         sg.Button('Mejores Puestos - Dificultad Máximo', key='mejores_puestos_dif_maxima', pad=((0, 0), 10), size=(round(ancho_total / 3), 1), button_color=('white', '#E1BF56'))],

        [sg.Output(size=(ancho_total +80, 5), key='-OUTPUT-', background_color='#545454', text_color='#E1BF56')],
        [sg.Button('Salir', key='quit', pad=((0, 0), 35), size=(ancho_total + 8, 1), button_color=('white', '#E1BF56'))],
    ]

    tipo_palabras = ['NN', 'JJ', 'VB']
    fichas_facil = {('A', 'E'): (11, 1), ('O', 'S'): (8, 1), ('I', 'U'): (6, 1), ('N', 'L'): (5, 1), ('R', 'T'): (4, 1), ('C', 'D'): (4, 2), ('M', 'B'): (3, 3), ('G', 'P'): (2, 3), ('F', 'H'): (2, 4), ('V', 'Q'): (2, 4), ('Y', 'K'): (1, 4), ('Ñ', 'W'): (1, 6), ('X', 'Z'): (1, 10)}
    fichas_media = {('A', 'E'): (15, 3), ('O', 'S'): (12, 3), ('I', 'U'): (10, 3), ('N', 'L'): (9, 3), ('R', 'T'): (8, 3), ('C', 'D'): (8, 4), ('M', 'B'): (7, 5), ('G', 'P'): (6, 5), ('F', 'H'): (6, 6), ('V', 'Q'): (6, 6), ('Y', 'K'): (5, 6), ('Ñ', 'W'): (5, 8), ('X', 'Z'): (5, 12)}
    fichas_maxima = {('A', 'E'): (17, 5), ('O', 'S'): (14, 5), ('I', 'U'): (12, 5), ('N', 'L'): (11, 5), ('R', 'T'): (10, 5), ('C', 'D'): (10, 6), ('M', 'B'): (9, 7), ('G', 'P'): (8, 7), ('F', 'H'): (8, 8), ('V', 'Q'): (8, 8), ('Y', 'K'): (7, 8), ('Ñ', 'W'): (7, 10), ('X', 'Z'): (5, 14)}
    botones_dificultad = {'dificultad_facil': [['NN', 'JJ', 'VB'], fichas_facil], 'dificultad_media': [['NN', 'VB'], fichas_media], 'dificultad_maxima': [[random.choice(tipo_palabras)], fichas_maxima]}
    botones_tiempo_partida = ['tiempo_partida_5_min', 'tiempo_partida_10_min', 'tiempo_partida_15_min']
    botones_tiempo_turno = ['tiempo_turno_30_seg', 'tiempo_turno_60_seg', 'tiempo_turno_90_seg']
    botones_mejores_puestos = ['mejores_puestos_dif_facil', 'mejores_puestos_dif_media', 'mejores_puestos_dif_maxima']

    configuracion_partida = ['dificultad_facil', 90, ['NN', 'JJ', 'VB'], 320, fichas_facil]
    window_principal = sg.Window('Scrabble', size=(ancho_total * 8, 650), background_color='#2C2C2C').Layout(layout_ventana_principal)

    diccionario_mejores_puestos = {'juan' : 90}

    jugar = False
    diccionario= False

    while True:
        event, value = window_principal.Read()
        if event in (None, 'quit'):
            window_principal.Close()
            break
        if event== 'Configuracion avanzada ':
            diccionario=VentanasBackEnd.ventanaConfig()


        elif event in botones_dificultad:
            VentanasBackEnd.click_dificultad(window_principal, event, botones_dificultad, configuracion_partida, fichas_facil, fichas_media, fichas_maxima)

        elif event in botones_tiempo_turno:
            VentanasBackEnd.click_tiempo_turno(window_principal, event, botones_tiempo_turno, configuracion_partida)

        elif event in botones_tiempo_partida:
            VentanasBackEnd.click_tiempo_partida(window_principal, event, botones_tiempo_partida, configuracion_partida)

        elif event in botones_mejores_puestos:
            window_principal.FindElement('-OUTPUT-').Update('')
            VentanasBackEnd.click_mejores_puestos(window_principal, event, botones_mejores_puestos)

        elif event in 'jugar':
            window_principal.Close()
            if (diccionario!= False):
                ProgramaPrincipal.main(configuracion_partida[2], diccionario, configuracion_partida[0], configuracion_partida[1], configuracion_partida[3])
                break
            else:
                ProgramaPrincipal.main(configuracion_partida[2], configuracion_partida[4], configuracion_partida[0],
                                       configuracion_partida[1], configuracion_partida[3])

            break
        elif event in 'cargar':

            try:
                window_principal.Close()
                ProgramaPrincipal.main(configuracion_partida[2], configuracion_partida[4],
                                       configuracion_partida[0], configuracion_partida[1], configuracion_partida[3],cargarJuego=True)
                window_principal.Close()
                break
            except(FileExistsError,FileNotFoundError):
                sg.popup('no hay ninguna partida guardada :(', background_color='#2C2C2C', text_color='#E1BF56', button_color=('white', '#E1BF56'), font=('Helvetica', 12))
                main()
                break


if __name__ == '__main__':
    main()
