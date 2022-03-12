import os
import PySimpleGUI as sg
import Tablero
import Atril
import Fichas
import time
import Jugar
import ScrabbleAR

import RegistroPartidas
from pickle import load



def main(nivel_palabras, config_fichas, nivel = 'Facil', tiempo_ronda = 30, tiempo_partida = 320,cargarJuego=False):

    if(cargarJuego):
        with open("partida_guardada", "rb") as f: #antes de entrar se fija que exista
            diccionario2 = load(f)
        tablero = diccionario2['tablero']
        atril = diccionario2['atril_jugador']
        atril_pc =diccionario2['atril_computadora']


        jugar = diccionario2['juego']
        letras_de_atril = 7
        tiempo_ini = jugar.get_hora()
        puntaje_total= jugar.get_puntaje_jugador()

        #moodif
        lista_de_palabras = diccionario2['juego'].get_lista_palabras()
        #ver lo del tiempo
        tiempo_max = tiempo_ronda * 100  # tiempo maximo de turno
        tiempo_comienzo_juego = int(round(time.time() * 100))
        tiempo_fin_juego = tiempo_partida * 100  # Este es el tiempo total de partida
        palabras_permitidas= jugar.get_nivel()
        jugar.mostrar_dificultad(nivel, nivel_palabras) #???
        nombre=jugar.get_nombre()
    else:
        nombre = RegistroPartidas.ingresar_usuario()
        filas = 15
        columnas = 15
        puntaje_total=0

        letras_de_atril = 7
        tablero = Tablero.Tablero(filas,columnas)
        atril = Atril.Atril(letras_de_atril)
        atril_pc = Atril.Atril_PC(letras_de_atril)
        palabras_permitidas = nivel_palabras
        diccionario = Fichas.crear_diccionario()


        jugar = Jugar.Jugar()
        letras_de_atril = 7

        print(jugar.get_turno())
        tiempo_max = tiempo_ronda * 100  # tiempo maximo de turno
        tiempo_comienzo_juego = int(round(time.time() * 100))
        tiempo_fin_juego = tiempo_partida * 100  # Este es el tiempo total de partida
        lista_de_palabras = []
        tiempo_ini=0
        jugar.mostrar_dificultad(nivel, nivel_palabras)

    fichas_jugador = Fichas.crear_bolsa_de_fichas(config_fichas)
    fichas_compu = Fichas.crear_bolsa_de_fichas(config_fichas)

    start_time = int(round(time.time() * 100))
    tiempo_computadora = 0  # inicializo el tiempo actual en 0
    puntajes_letras = Fichas.crear_diccionario_de_puntos(config_fichas)
    diccionario = Fichas.crear_diccionario()
    continuar= atril.agregar_letras(fichas_jugador) #si no hay suficientes fichas  devuelve false

    if(continuar):

        atril_pc.agregar_letras(fichas_compu)
    else:
        sg.popup("upsss, no hay suficientes letras, prueba agregar mas", background_color='#2C2C2C', text_color='#E1BF56', button_color=('white', '#E1BF56'), font=('Helvetica', 12))
        ScrabbleAR.main()



    current_time = 0
    imagen = '/imagenes/scrabble.png'

    # ------ Column Definition ------ #
    column1 = tablero.crear_tablero(nivel)
    column2=[[sg.Text('Fin del juego:', background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12))],
             [sg.Text('', size=(8, 2), font=('Helvetica', 20), justification='center', key='timer_juego', background_color='#2C2C2C', text_color=('#E1BF56'))],
             [sg.Button(button_text='Finalizar Juego',key=('fin_juego'), button_color=('white', '#E1BF56'))],
             [sg.Text('Ultimas Palabras ingresadas', background_color='#2C2C2C', text_color=('#E1BF56'), font=('Helvetica', 12))],
             [sg.Listbox(values=(lista_de_palabras), size=(30, 6),key='lista', background_color='#545454', text_color=('#E1BF56'))],
             [sg.Button(button_text='Posponer partida', key=('Posponer'), button_color=('white', '#E1BF56'))],
             ]
    # ------ Menu Definition ------ #
    menu_def = [['Menu', ['Ver modo']],
                 ]
    letter_atril = { 'size' : (3, 2), 'pad' : (0,0), 'button_color' : ('white', '#C8C652')}
    #-----------------------LAYOUT VENTANA-----------------------------------
    layout= []
    layout.append([sg.Menu(menu_def, tearoff=True)])
    atril_PC = [[sg.Button(key=('Atril_PC', i), button_text='?', **letter_atril) for i in range(letras_de_atril)]]
    imagen = [[sg.Text(' '*10, background_color='#2C2C2C'), sg.Image((os.getcwd()+imagen), size=(370, 40), background_color='#2C2C2C')]]
    layout.append([sg.Column(atril_PC, background_color='#2C2C2C'), sg.Column(imagen, background_color='#2C2C2C')])
    PC = [sg.Text('', size=(8, 1), font=('Helvetica', 20), justification='center', key='tempo_compu', background_color='#2C2C2C', text_color=('#E1BF56')), sg.Text('Puntaje computadora: ', font='Helvetica', background_color='#2C2C2C', text_color=('#E1BF56')), sg.Text(atril_pc.get_puntaje(), key='puntPC', font='Helvetica', background_color='#2C2C2C', text_color=('#E1BF56' ),size=(20, 1) )]
    layout.append(PC)
    layout.append([sg.Column(column1, background_color='#2C2C2C'), sg.Column(column2, background_color='#2C2C2C')])
    layout.append([sg.Text('Seleccione una letra de abajo', auto_size_text=True, font='Helvetica', background_color='#2C2C2C', text_color=('#E1BF56'))])
    layout.append([sg.Button(key=('Atril_jugador', i) , button_text= atril.get_espacio_fichas()[i].get_letra(), **letter_atril) for i in range(letras_de_atril)])
    botones = [sg.Button(key='vali', button_text='Validar', button_color=('white', '#E1BF56'), font='Helvetica'),sg.Button(button_text='Cambiar letras',key ="cambiar_letras", button_color=('white', '#E1BF56'), font='Helvetica'), sg.Button(button_text='devolver', key='devolver_al_atril', button_color=('white', '#E1BF56'), font='Helvetica'), sg.Text('Puntaje total: ', font='Helvetica', background_color='#2C2C2C', text_color=('#E1BF56')), sg.Text(puntaje_total, key='punt', font='Helvetica', background_color='#2C2C2C', text_color=('#E1BF56'),size=(20,1))]
    layout.append([sg.Checkbox("", key=('Checkbox', i), size=(2, 2), background_color='#2C2C2C', text_color='#E1BF56')for i in range(letras_de_atril)])
    layout.append(botones)
    layout.append([sg.Text('', size=(8, 1), font=('Helvetica', 20), justification='center', key='timer_jugador', background_color='#2C2C2C', text_color=('#E1BF56'))]) #Temporizador

    window = sg.Window('Scrabble', background_color='#2C2C2C').Layout(layout)
    
    if (cargarJuego):
        tablero.cargar_tablero(window)

    while continuar:
        event, values = window.Read(timeout=0)
        if int(round(time.time() * 100))-tiempo_comienzo_juego> tiempo_fin_juego or event== 'fin_juego' or atril.get_terminar_juego() or atril_pc.get_terminar_juego():  # el juego terminó
            atril.devolver_fallo(window,tablero)
            window.Close()
            #guardo el puntaje y datos del usuario
            if(atril.get_terminar_juego()):
                sg.popup('se terminaron los cambios de atril, se termina el juego ', background_color='#2C2C2C', text_color='#E1BF56', button_color=('white', '#E1BF56'), font=('Helvetica', 12))
            #muestro una ventana con el ganador, opcion retornar al menu
            RegistroPartidas.muestra_Ganador(puntaje_total, atril_pc.get_puntaje(), atril, atril_pc, puntajes_letras, nivel, nombre)

            break
        elif event== 'Posponer':
            jugar.cargar_datos(puntaje_total,atril_pc.get_puntaje(),fichas_jugador, fichas_compu, lista_de_palabras,nivel_palabras,tiempo_transcurrido,nombre)
            jugar.guardar_partida(tablero,atril,atril_pc,jugar)
            sg.Popup("SE GUARDO LA PARTIDA", background_color='#2C2C2C', text_color='#E1BF56', button_color=('white', '#E1BF56'), font=('Helvetica', 12))
            window.Close()
        else:
            # turno de la computadora

            if jugar.get_turno()=='computadora':
                start_time=int(round(time.time()*100)) # momento en el que empiezo a contar
                window.Read(timeout=0)
                current_time= 0 #tiempo transcurrido
                tiempo_computadora = int(round(time.time()*100))-current_time - start_time
                window.Element('tempo_compu').Update('{:02d}:{:02d}.{:02d}'.format((tiempo_computadora // 100) // 60,(tiempo_computadora // 100) % 60, tiempo_computadora % 100))

                #Juega la computadora
                palabra_armada = atril_pc.jugar_turno(tablero, diccionario, window, fichas_compu, puntajes_letras, palabras_permitidas)
                if(palabra_armada != ' ' and palabra_armada != ''):
                    lista_de_palabras.append(palabra_armada)
                    window.Element('lista').Update(values=lista_de_palabras)
                #actualizo los relojes
                tiempo_computadora = int(round(time.time()))-current_time - start_time
                window.Element('tempo_compu').Update('{:02d}:{:02d}.{:02d}'.format((tiempo_computadora // 100) // 60,(tiempo_computadora // 100) % 60, tiempo_computadora % 100))

                #-------actualizo reloj total
                tiempo_transcurrido = int(round(time.time() * 100)) - tiempo_comienzo_juego
                window.Element('timer_juego').Update('{:02d}:{:02d}.{:02d}'.format((tiempo_transcurrido // 100) // 60,(tiempo_transcurrido// 100) % 60, tiempo_transcurrido % 100))


                if (tiempo_computadora > tiempo_max):
                    print('terminoeltiempo')
                jugar.cambiar_turno()

                tiempo_computadora = int(round(time.time()*100))-current_time - start_time
                window.Element('tempo_compu').Update('{:02d}:{:02d}.{:02d}'.format((tiempo_computadora // 100) // 60,(tiempo_computadora // 100) % 60, tiempo_computadora % 100))

            #turno del jugador
            elif jugar.get_turno()=='jugador':
                #se termino el tiempo del jugador
                if (current_time> tiempo_max):
                    sg.Popup('Termino el tiempo', background_color='#2C2C2C', text_color='#E1BF56', button_color=('white', '#E1BF56'), font=('Helvetica', 12))
                    print('terminoeltiempo jugador') # insertat
                    atril.devolver_fallo(window,tablero)
                    jugar.cambiar_turno()
                    continue    #no sacar el continue, lo que hace es volver al while sin pasar por lo que esta abajo

                # no se termino el tiempo del jugador
                
                if event == 'devolver_al_atril':
                    atril.devolver_fallo(window, tablero)

                if event in atril.listado_botones():
                    atril.click(tablero, event)
                elif event in tablero.listado_botones():
                    tablero.click(atril, event, window)

                elif event == "cambiar_letras":
                    atril.devolver_fallo(window,tablero)
                    if (atril.get_cambios_atril()>0):
                        atril.cambiar_letras(fichas_jugador,window,tablero,values,fichas_jugador,jugar)
                    else:
                        sg.Popup('no hay mas cambios de atril', background_color='#2C2C2C', text_color='#E1BF56', button_color=('white', '#E1BF56'), font=('Helvetica', 12))
                elif event in atril.listado_botones():
                    atril.click(tablero, event)

                elif event == 'vali':
                    puntaje_total = tablero.click_validar(atril, tablero, window, diccionario, puntaje_total, fichas_jugador, puntajes_letras, jugar, palabras_permitidas, lista_de_palabras)
                elif event=='Ver modo':
                    restantes=  tiempo_fin_juego - tiempo_transcurrido
                    jugar.mostrar_modos(nivel, nivel_palabras,tiempo_max,tiempo_fin_juego,restantes)
                    pass #todo: agregar texto al menu
                elif event == None:
                    break;
                current_time = int(round(time.time() * 100)) - (
                    tiempo_computadora) - start_time  # tiempo actual - tiempo de la computadora - el momento en que empezo
                tiempo_transcurrido=int(round(time.time() * 100))+tiempo_ini -tiempo_comienzo_juego
                window.Element('timer_juego').Update('{:02d}:{:02d}.{:02d}'.format((tiempo_transcurrido// 100) // 60, (tiempo_transcurrido // 100) % 60,
                                                  tiempo_transcurrido % 100))  # muestro el contador
                window.Element('timer_jugador').Update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60, (current_time // 100) % 60, current_time % 100)) #muestro el contador


    window.Close()
    print('llega ??')
    #RegistroPartidas.guardar_score(nivel, nombre, puntaje_total)

if __name__ == '__main__':
    main()
