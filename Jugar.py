import random
import PySimpleGUI as sg
from pickle import dump, dumps, load, loads
class Jugar :


    def __init__(self):
        self.set_turno(self.seleccionar_turno())


    # _____________________Setters y GETTERS

    def set_intentos(self, intento):
        self.__intentos= intento
    def get_intentos(self, intentos):
        return self.__intentos

    def set_turno(self, turno):
        self.__turno= turno
    def get_turno(self):
        return self.__turno

    def set_hora(self, hora):
        self.__hora= hora
    def get_hora(self):
        return self.__hora

    def set_puntaje_computadora(self, puntaje):
        self.__puntaje_computadora= puntaje
    def get_puntaje_computadora(self):
        return self.__puntaje_computadora

    def set_puntaje_jugador(self, puntaje):
        self.__puntaje_jugador= puntaje

    def get_puntaje_jugador(self):
        return self.__puntaje_jugador

    def set_bolsa_jugador(self, bolsa):
        self.__bolsa_jugador= bolsa
    def get_bolsa_jugador(self):
        return self.__bolsa_jugador

    def set_bolsa_compu(self, bolsa):
        self.__bolsa_compu = bolsa
    def get_bolsa_compu(self):
        return self.__bolsa_compu

    def set_lista_palabras(self, lista):
        self.__lista_palabras=lista
    def get_lista_palabras(self):
        return self.__lista_palabras

    def set_nivel(self,nivel):
        self.__nivel=nivel
    def get_nivel(self):
        return self.__nivel

    def set_nombre(self,nombre):
        self.__nombre= nombre
    def get_nombre(self):
        return self.__nombre


    def cambiar_turno(self):
        if(self.get_turno()== 'computadora'):
            self.set_turno('jugador')
        else:
            self.set_turno('computadora')
    def seleccionar_turno(self):

        turno=random.choice(['computadora','jugador'])
        return turno

    def mostrar_dificultad(self, dificultad, tipo ):

        if dificultad=='dificultad_maxima':
            diccionario= dict(NN='sustantivos', JJ='adjetivos', VB='verbos')
            text= 'Usted eligio la dificultad maxima.\n  Debe jugar con ' + diccionario[tipo[0]]
            sg.Popup(text)

    def mostrar_modos(self, dificultad, tipo, minutos_partida, minutos_ronda,restantes):

        '''muestra modo de juego'''
        diccionario_dificultad={}
        diccionario_dificultad= {'dificultad_media':' MEDIA', 'dificultad_facil':'FACIL', 'dificultad_maxima':'MAXIMA'}
        diccionario = dict(NN='SUSTANTIVOS', JJ='ADJETIVOS', VB='VERBOS ')
        string =' '
        for texto in tipo:
            string= string +diccionario[texto] +' '


        texto=(''' DIFICULTAD:'''+diccionario_dificultad[dificultad]+'''


    ----------USTED PUEDE INGRESAR----------
            '''+string+'''
    MINUTOS DE PARTIDA:'''+ str(minutos_partida)+'''

    MINUTOS DE RONDA :'''+ str(minutos_ronda) +'''

     RESTAN:'''+ str(restantes)+ 'min')
        sg.Popup(texto, title='Modo de juego', background_color='#2C2C2C', text_color='#E1BF56', button_color=('white', '#E1BF56'), font=('Helvetica', 12))
    def guardar_partida(self,tablero, atril_jugador,atril_computadora,juego):

        diccionario=dict(tablero=tablero,atril_jugador=atril_jugador,atril_computadora=atril_computadora,juego=juego)

        with open("partida_guardada", "wb") as f:
            dump(diccionario, f)

    def devolver_diccionario(self):
        with open("partida_guardada", "rb") as f:
            diccionario=load(f)
        return diccionario

    def cargar_datos(self,puntaje_jugador, puntaje_compu,bolsa_jugador, bolsa_compu, lista_palabras, nivel,hora,nombre):
        self.set_bolsa_compu(bolsa_compu)
        self.set_bolsa_jugador(bolsa_jugador)
        self.set_puntaje_computadora(puntaje_compu)
        self.set_lista_palabras(lista_palabras)
        self.set_puntaje_jugador(puntaje_jugador)
        self.set_nivel(nivel)
        self.set_hora(hora)
        self.set_nombre(nombre)
