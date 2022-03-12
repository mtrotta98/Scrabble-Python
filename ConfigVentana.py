import PySimpleGUI as sg
from datetime import date
import json
import os


def abrirArch (nombreArch, puntos):
    datos = []
    try:
        archivo = open(nombreArch, "r")
        datos = json.load(archivo)
        datos.append({'Nombre': puntos[0], 'Puntaje': puntos[1], 'Fecha': "{}/{}/{}".format(puntos[2], puntos[3], puntos[4])})
        archivo = open(nombreArch, "w")
        archivo.write(json.dumps(datos))
        archivo.close()
    except:
        archivo = open(nombreArch, "w")
        try:
            datos.append({'Nombre': puntos[0], 'Puntaje': puntos[1], 'Fecha': "{}/{}/{}".format(puntos[2], puntos[3], puntos[4])})
            json.dump(datos, archivo)
        except:
            print('error al llenar el archivo ')
        archivo.close()

def layoutPrin():
    layoutPrincipal = [
            [sg.Button('Jugar', key='jugar', pad=((130, 0), 35), size=(25,1))],
            [sg.Button('Configurar', key='config', pad=((130, 0), 35), size=(25,1))],
            [sg.Button('Estadisticas', key='ranking', pad=((130, 0), 35), size=(25,1))],
            [sg.Button('Salir', key='quit', pad=((130, 0), 35), size=(25,1))],
    ]
    return layoutPrincipal

def layoutConfig():
    layoutconfig = [
                [sg.Text('Seleccione el nivel de dificultad:', font='Helvetica', background_color=('#A72D2D'))],
                [sg.InputCombo(('Facil', 'Normal', 'Dificil'), size=(25,1), key='nivel')],
                [sg.Text('Seleccione el tiempo por ronda:', font='Helvetica', background_color=('#A72D2D'))],
                [sg.InputCombo(('20 seg(facil)', '15 seg(normal)', '10 seg(dificil)'), size=(20,1), key='tiempo')],
                [sg.Button('Aceptar', key='Ok', pad=(80,5))]
    ]
    return layoutconfig

def layoutNoConfig():
    layoutNoConfig = [
                    [sg.Text('Se ejecutara con la configuracion predeterminada', font='Helvetiva', background_color=('#A72D2D'))],
                    [sg.Ok(), sg.Cancel()]
    ]
    return layoutNoConfig

def layoutUsuario():
    layoutUs = [
               [sg.Text('Ingrese un nombre de usuario: ', background_color=('#A72D2D')), sg.InputText(key='usuario')],
               [sg.Button('Aceptar', pad=(100,10), key='ok')]
    ]
    return layoutUs

def layoutRanking(datos):
        layoutRank = []
        for i in range(len(datos)):
            try:
                botones = [sg.Text(text='Nombre: ', background_color=('#A72D2D')), sg.Text(text= datos[i]['Nombre'], background_color=('#A72D2D')), sg.Text(text= 'Puntaje: ', background_color=('#A72D2D')), sg.Text(text=datos[i]['Puntaje'], background_color=('#A72D2D')), sg.Text(text= 'Fecha: ', background_color=('#A72D2D')), sg.Text(text=datos[i]['Fecha'], background_color=('#A72D2D'))]
                layoutRank.append(botones)
                layoutRank.append([sg.Text('-'*140, background_color=('#A72D2D'))])
            except:
                print('No se registraron mas jugadores')
        return layoutRank

def layoutSelecTop():
    layoutTop = [
                [sg.Text('Seleccione el top que desea ver', background_color=('#A72D2D'))],
                [sg.Button('Facil', key='Facil'), sg.Button('Normal', key='Normal'), sg.Button('Dificil', key='Dificil')]
    ]
    return layoutTop

def ventanaConfig (config):
    try:
        windowConfig = sg.Window('Configuracion', size=(300,160), background_color=('#A72D2D')).Layout(layoutConfig())
        event, value = windowConfig.Read()
        if event == None:
            windowConfig.Close()
            return config
        if event == 'Ok':
            config = value
        windowConfig.Close()
        return config
    except:
        print('Error al abrir la ventana config')
        pass

def ventanaJugar (config, Scrabble):
    ''' Cierra las ventanas y abre una nueva ventana con el Scrabble '''
    if (len(config) == 0):
        try:

            windowNoConfig = sg.Window('Aviso', size=(450,100), background_color=('#A72D2D')).Layout(layoutNoConfig())
            event, value = windowNoConfig.Read()

            if (event == 'Ok'):
                #se entra sin configuracion al juego
                windowUs = sg.Window('Usuario', size=(350, 100), background_color=('#A72D2D')).Layout(layoutUsuario())
                event, value = windowUs.Read()
                if event == 'ok':
                    nombre = value['usuario']
                    windowUs.Close()
                    windowNoConfig.Close()#  ??? QUE ES ESTO
                    return (nombre,Scrabble.main(), date.today().day, date.today().month, date.today().year) #SCRABBEL MAIN??????????????????????????
            elif(event == 'Cancel'):
                windowNoConfig.Close()
        except:
            print('Error al abrir la ventana JUGar')
            pass
    else:
        windowUs = sg.Window('Usuario', size=(350, 100), background_color=('#A72D2D')).Layout(layoutUsuario())
        event, value = windowUs.Read()
        if event == 'ok':
            nombre = value['usuario']
            windowUs.Close()
            return (nombre, Scrabble.main(config['nivel'], config['tiempo'].split(' ')[0]), date.today().day, date.today().month, date.today().year)

def ventanaRanking(datos):
    windowRank = sg.Window('Top10', size=(600,600), background_color=('#A72D2D')).Layout(layoutRanking(datos))
    event, value = windowRank.Read()


def ventanaSelecTop():
    windowTop = sg.Window('Seleccion', size=(300,100), background_color=('#A72D2D')).Layout(layoutSelecTop())
    while True:
        event, value = windowTop.Read()
        if (event == 'Facil'):
            windowTop.Close()
            return 'Facil'
        elif(event == 'Normal'):
            windowTop.Close()
            return 'Normal'
        else:
            windowTop.Close()
            return 'Dificil'
