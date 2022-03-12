import Casilla as cas
import random
from random import randint
import Fichas
import PySimpleGUI as sg
import itertools
from pattern import *
from pattern.es import *

def random_letter(lista_letras ):
    letra= chr(randint(65, 90))
    if letra in (lista_letras):
        lista_letras.remove(letra)
        return letra

class Atril():




    def __init__(self, columnas, tipo_atril = 'Atril_jugador'):
        self.__casilla_seleccionada  = None
        self.set_columnas(columnas)
        self.set_terminar_juego(False)
        self.set_puntaje(000)
        self.set_espacio_fichas( [cas.Casilla() for x in range(columnas)])
        for i in range(columnas):
            self.get_espacio_fichas()[i] =(cas.Casilla(tipo_atril, i))
        self.set_cambios_atril(9) # Cantidad de cambios está dada por la cantidad de fichas para cambiar en la bolsa
        self.set_esta_vacio(True)


    #----------- getters y setters-------------------------
    def set_terminar_juego(self, var):
        self.__terminar_juego = var
    def get_terminar_juego(self):
        return self.__terminar_juego

    # cambios_atril

    def set_cambios_atril(self, cantidad):
        self.__cambios_atril= cantidad
    def get_cambios_atril(self):
        return self.__cambios_atril
    def decrement_cambios_atril(self):
        self.set_cambios_atril(self.get_cambios_atril()-1)

    #__espacio_fichas
    def set_espacio_fichas(self, arreglo):
        self.__espacio_fichas= arreglo
    def get_espacio_fichas(self):
        return self.__espacio_fichas

    #__casilla_seleccionada
    def set_casilla_seleccionada(self, casilla):
        self.__casilla_seleccionada = casilla
    def get_casilla_seleccionada(self):
        return self.__casilla_seleccionada

    #__columnas
    def set_columnas(self,columnas):
        self.__columnas= columnas
    def get_columnas(self):
        return self.__columnas

    #__esta_vacio
    def set_esta_vacio(self,validez):
        self.__esta_vacio= validez
    def esta_vacio(self):
        return self.__esta_vacio

    def set_puntaje (self,puntaje):
        self.__puntaje=puntaje

    def get_puntaje(self):
        return self.__puntaje


#_____________________________________________Comienzo de  otros metodos ____________

    def agregar_letras(self, bolsa):

        '''agrego letras al atril'''
        if(len(bolsa)>7):
            for i in self.get_espacio_fichas():
                if not i.get_tiene_letra():
                    letra= bolsa.pop(randint(0, len(bolsa)-1))
                    i.set_letra(letra)
                    i.set_tiene_letra(True)
            return  True
        else:
            self.set_terminar_juego(True)
            sg.Popup('upss no hay mas letras ', background_color='#2C2C2C', text_color='#E1BF56', button_color=('white', '#E1BF56'), font=('Helvetica', 12))
            return False


    def cambiar_letras(self, lista_letras,window,tablero,checkbox,bolsa,juego):
        ''' cambio las letras del atril por nuevas letras'''
        #self.devolver_fallo(window,tablero) #devuelve las letras que estan en uso  al atril
        if len(bolsa)>7:

            for i in range(7):
                if self.get_espacio_fichas()[i].get_tiene_letra() and checkbox[('Checkbox', i)]:
                    bolsa.append(self.get_espacio_fichas()[i].get_letra())
                    letra = bolsa.pop(randint(0, len(bolsa) - 1))
                    self.get_espacio_fichas()[i].set_letra(letra)

            self.decrement_cambios_atril() #solo hay 3 cambios de atril, decremento en 1
            self.refrescar_atril(window)

            juego.cambiar_turno()
        else:
            self.set_terminar_juego(True)
            sg.popup('no hay mas letras', background_color='#2C2C2C', text_color='#E1BF56', button_color=('white', '#E1BF56'), font=('Helvetica', 12))
            return False





    def refrescar_atril(self, window, atril ='Atril_jugador'):
        '''actualizo el atril del jugador '''
        letras = (self.get_espacio_fichas())
        if atril== 'Atril_PC':
            for i in range(len(letras)):
                window.Element((atril, i)).Update(text='?')
        else:
            for i in range(len(letras)):
                window.Element((atril,i)).Update(text=letras[i].get_letra())

    def devolver_fallo(self, window, tablero): #no hace falta mandar la lista de coordenadas si te mandas el tablero -agus
        '''Este metodo devuelve las letras al atril'''
        letra_devolver = []
        letras = self.get_espacio_fichas()
        for coor in tablero.enlistar_coordenadas_activas(): #actualiza los botones usados en el tablero y se guarda las letras para devolver al atril
            if (tablero.get_matriz()[coor[0]][coor[1]].get_definitivo() == False): #ahora solo devuelve las letras que no son definitivas
                letra_devolver.append(tablero.get_matriz()[coor[0]][coor[1]].get_letra())
                tablero.get_matriz()[coor[0]][coor[1]].set_letra(' ')
                tablero.get_matriz()[coor[0]][coor[1]].set_activo(False)
                window.Element(coor).Update(tablero.get_matriz()[coor[0]][coor[1]].get_premio(), button_color=(('white', tablero.get_matriz()[coor[0]][coor[1]].get_color())))

        for i in range(len(letras)):
            if letras[i].get_letra() == ' ':
                if (len(letra_devolver) > 0):
                    letras[i].set_letra(letra_devolver[0])
                    window.Element(('Atril_jugador', i)).Update(letras[i].get_letra())
                    letras[i].set_tiene_letra(True)
                    letra_devolver.pop(0)
        tablero.desbloquear_tablero()


    def listado_botones(self):
        ''' retorna una lista con las teclas del atril'''
        listado =[]
        for i in range(self.get_columnas()):
            listado.append(self.get_espacio_fichas()[i].get_id())
        return listado

    def click(self, casilla, coordenadas):
        self.set_casilla_seleccionada(self.get_espacio_fichas()[coordenadas[1]])
        refresh = self.get_casilla_seleccionada().get_letra()
        return refresh

class Atril_PC(Atril):
    def __init__(self, columnas, puntaje=0):
        super().__init__(columnas, 'Atril_PC')
        self._puntaje = 0
        self._posicion = ''

    def set_puntaje(self, puntaje):
        self._puntaje= puntaje
    def get_puntaje(self):
        return self._puntaje
    def set_posicion(self, posicion):
        self._posicion = posicion
    def get_posicion(self):
        return self._posicion

    def formar_palabra(self, letras_desordenadas, lista_diccionario, palabras_permitidas= ('NN', 'JJ', 'VB' )):
        retorno = ' '
        print("formar palabras ", letras_desordenadas)
        letras_desordenadas = letras_desordenadas.lower()
        lista_intentos = set()
        for i in range(3, 7):
            lista_intentos.update((map("".join, itertools.permutations(letras_desordenadas, i))))
        print(lista_intentos)
        for intento in lista_intentos:
            if intento in lexicon:
                if parse(intento).split('/')[1] in palabras_permitidas: #puede ser que no toma el parse??
                    print("está en parse")
                    if intento in lista_diccionario:
                        print("Esta en el diccionario")
                        return intento

        return retorno

    def buscar_espacio(self, tablero, casillas_requeridas):
        for posibilidades in range(3):
            posicion = random.choice(['vertical', 'horizontal'])
            i = random.randint(0, tablero.get_filas())
            j = random.randint(0, tablero.get_columnas())
            count = 0
            if (posicion == 'vertical'):
                if (casillas_requeridas > tablero.get_filas() - j):
                    break
                for k in range(casillas_requeridas):
                    try:
                        if not tablero.get_matriz()[i][j+k].get_activo() and not tablero.get_matriz()[i][j+k].get_definitivo():
                            count = count + 1
                    except IndexError:
                        print('hay algun error de indexacion') #todo: ver por que salta error
                if count == casillas_requeridas:
                    self.set_posicion(posicion)
                    return (i,j)
            else:
                if (casillas_requeridas > tablero.get_columnas() - i):
                    break
                for k in range(casillas_requeridas):
                    try:
                        if not tablero.get_matriz()[i + k][j].get_activo() and not tablero.get_matriz()[i + k][j].get_definitivo():
                            count = count + 1
                    except IndexError:
                        print('Error de indexacion')
                if count == casillas_requeridas:
                    self.set_posicion(posicion)
                    return(i, j)
        return False

    def orden_coordenadas_atril(self, palabra_armada):
        lista_coordenadas_de_palabra_en_atril = []
        for i in palabra_armada:
            for j in range(len(self.get_espacio_fichas())):
                if self.get_espacio_fichas()[j].get_letra().lower() == i and self.get_espacio_fichas()[j].get_tiene_letra() :
                    print("encontró la cordenada", i, self.get_espacio_fichas()[j].get_letra().lower() )
                    self.get_espacio_fichas()[j].set_tiene_letra(False)
                    lista_coordenadas_de_palabra_en_atril.append(self.get_espacio_fichas()[j].get_id())
                    break
        return lista_coordenadas_de_palabra_en_atril

    def colocar_en_tablero(self,tablero,  lista_coordenadas, coordenada_inicial,ventana):
        ''' coloca una a una las letras en el tablero '''
        coordenadas_tablero = []
        for i in range(len(lista_coordenadas)):
            letra_a_colocar = self.get_espacio_fichas()[lista_coordenadas[i][1]].get_letra()
            if (self.get_posicion() == 'vertical'):
                tablero.get_matriz()[coordenada_inicial[0]][coordenada_inicial[1] + i].set_letra(letra_a_colocar)
                tablero.get_matriz()[coordenada_inicial[0]][coordenada_inicial[1] + i].set_definitivo(True)
                tablero.get_matriz()[coordenada_inicial[0]][coordenada_inicial[1] + i].set_tiene_letra(True)
                coordenadas_tablero.append(tablero.get_matriz()[coordenada_inicial[0]][coordenada_inicial[1] + i].get_id())
                ventana.Element((coordenada_inicial[0],coordenada_inicial[1] + i) ).Update(letra_a_colocar, button_color=('white', '#C8C652'))
            else:
                tablero.get_matriz()[coordenada_inicial[0] + i][coordenada_inicial[1]].set_letra(letra_a_colocar)
                tablero.get_matriz()[coordenada_inicial[0] + i][coordenada_inicial[1]].set_definitivo(True)
                tablero.get_matriz()[coordenada_inicial[0] + i][coordenada_inicial[1]].set_tiene_letra(True)
                coordenadas_tablero.append(tablero.get_matriz()[coordenada_inicial[0] + i][coordenada_inicial[1]].get_id())
                ventana.Element((coordenada_inicial[0] + i, coordenada_inicial[1])).Update(letra_a_colocar, button_color=('white', '#C8C652'))
            self.get_espacio_fichas()[lista_coordenadas[i][1]].set_letra("")
            self.get_espacio_fichas()[lista_coordenadas[i][1]].set_tiene_letra(False)
        return coordenadas_tablero

    def calcular_puntajePC(self, puntajes_letras, botones, tablero):
        total = 0
        aumentos = []
        for pos in botones:
            if (tablero.get_matriz()[pos[0]][pos[1]].get_letra() in puntajes_letras):
                total = total + puntajes_letras[tablero.get_matriz()[pos[0]][pos[1]].get_letra()]
        for pos in botones:
            if (tablero.get_matriz()[pos[0]][pos[1]].get_premio() == "3P"):
                total = total * 3
            elif(tablero.get_matriz()[pos[0]][pos[1]].get_premio() == "3L"):
                total = total + 3
            elif(tablero.get_matriz()[pos[0]][pos[1]].get_premio() == "2P"):
                total = total * 2
            elif(tablero.get_matriz()[pos[0]][pos[1]].get_premio() == "2L"):
                total = total + 2
            elif(tablero.get_matriz()[pos[0]][pos[1]].get_premio() == "2R"):
                total = total - 2
        return total

    def mezclar_letras(self):
        lista_letras = []
        for j in range(len(self.get_espacio_fichas())):
            lista_letras.append(self.get_espacio_fichas()[j].get_letra())
        random.shuffle(lista_letras)
        for j in range(len(self.get_espacio_fichas())):
            self.get_espacio_fichas()[j].set_letra(lista_letras[0])
            lista_letras.pop(0)

    def jugar_turno(self,tablero, lista_diccionario,ventana,bolsa, puntajes_letras, palabras_permitidas = ('NN', 'JJ', 'VB' )):
        '''juega el turno de la computadora, si encuentra una palabra la pone en el tablero . pasa turno  '''

        lista_letras = ""
        for boton in self.listado_botones():
            lista_letras = lista_letras + self.get_espacio_fichas()[boton[1]].get_letra()
        palabra_armada = self.formar_palabra( lista_letras, lista_diccionario, palabras_permitidas)
        if (palabra_armada != " ") and len(palabra_armada)>2:
            coordenada_inicial = False
            for i in range (3):
                coordenada_inicial = self.buscar_espacio(tablero, len(palabra_armada)) #ver si es boole
                if coordenada_inicial == True:
                    return ' '
            if(coordenada_inicial!= False):
                print(palabra_armada)
                lista_coordenadas = self.orden_coordenadas_atril(palabra_armada)
                coordenadas_tablero = self.colocar_en_tablero(tablero, lista_coordenadas, coordenada_inicial,ventana)
                self._puntaje = self._puntaje + self.calcular_puntajePC(puntajes_letras, coordenadas_tablero, tablero)
                ventana.Element('puntPC').Update(self._puntaje)
                self.agregar_letras(bolsa)
            else:

                print('no se encontro una coordenada adecuada ')
                return ''

        else:
            self.cambiar_todas_letras(ventana,bolsa)
            return ' '
        self.refrescar_atril(ventana, 'Atril_PC')
        return palabra_armada


    def cambiar_todas_letras(self,window,bolsa):
        '''la PC cambia todas las letras del atril'''
        if len(bolsa)<7:
            self.set_terminar_juego(True)
            sg.popup('La pc se quedo sin letras ')
            return False

        else:
            for i in range(7):
                bolsa.append(self.get_espacio_fichas()[i].get_letra())
                if(len(bolsa)>1):
                    self.get_espacio_fichas()[i].set_letra(bolsa.pop(randint(0, len(bolsa)-1)))
                else:
                    self.set_terminar_juego(True)
            self.decrement_cambios_atril() #solo hay 3 cambios de atril, decremento en 1
        self.refrescar_atril(window, 'Atril_PC')
