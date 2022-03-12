import Casilla
import Fichas
import PySimpleGUI as sg
from pattern.es import *
from pattern.web import Wiktionary


class Tablero:

    def __init__(self, filas=15, columnas=15):

        self.set_filas(filas)
        self.set_columnas(columnas)
        self.set_coorUsadas()
        self.set_coordenadasActivas()
        self.set_matriz([[Casilla.Casilla() for x in range(columnas)] for y in range(filas)])
        for i in range(filas):
            for j in range(columnas):
                self.get_matriz()[i][j] = Casilla.Casilla(i,j)


#------------------------------Comienzo getters y setters-----------------------

    def set_filas(self, filas):
        self.__filas= filas

    def get_filas(self):
        return self.__filas

    def set_columnas(self, columnas):
        self.__columnas= columnas

    def get_columnas(self):
        return self.__columnas

    def set_matriz(self, matriz):
        self.__matriz= matriz

    def get_matriz(self):
        return self.__matriz

    def set_coorUsadas(self, listCoorUsadas=[]):
        self.__coorUsadas = listCoorUsadas

    def get_coorUsadas(self):
        return self.__coorUsadas

    def set_coordenadasActivas(self, coorAct=[]):
        self.__coordenadas_activas = coorAct

    def get_coordenadasActivas(self):
        return self.__coordenadas_activas

#---------------------comienzo otros metodos-----------------------------------

    def imprimir(self):
        ''' imprime el tablero'''
        for i in range(self.get_filas()):
            for j in range(self.get_columnas()):
                print(self.get_matriz()[i][j])

    def listado_botones(self):
        ''' devuelve una lista con el id de los botones'''
        listado =[]
        for i in range(self.get_filas()):
            for j in range(self.get_columnas()):
                listado.append(self.get_matriz()[i][j].get_id())
        return listado

    def click(self, atril, coordenadas, ventana):
        ''' selecciona una casilla del tablero'''
        if atril.get_casilla_seleccionada() is not None:
                if self.get_matriz()[coordenadas[0]][coordenadas[1]].get_habilitado() and not self.get_matriz()[coordenadas[0]][coordenadas[1]].get_definitivo():
                    self.actualizar_letra_tablero(atril, coordenadas)
                    atril.get_casilla_seleccionada().set_letra(' ')
                    atril.get_casilla_seleccionada().set_tiene_letra(False)
                    ventana.Element(atril.get_casilla_seleccionada().get_id()).Update(' ')
                    atril.set_casilla_seleccionada(None)
                    ventana.Element(coordenadas).Update(self.get_matriz()[coordenadas[0]][coordenadas[1]].get_letra(), button_color=('white', '#C8C652'))
                    print(self.get_matriz()[coordenadas[0]][coordenadas[1]].get_letra())

    def actualizar_letra_tablero(self, atril, coordenadas):
        ''' pone la letra del atril en el tablero'''
        self.get_matriz()[coordenadas[0]][coordenadas[1]].set_letra(atril.get_casilla_seleccionada().get_letra())
        self.get_matriz()[coordenadas[0]][coordenadas[1]].set_activo(True)
        self.bloquear_tablero()

    def enlistar_coordenadas_activas(self):
        ''' retorna una lista con las coordenadas activas'''
        coordenadas_activas = []
        for i in range(self.get_filas()):
            for j in range(self.get_columnas()):
                self.get_matriz()[i][j].set_habilitado(False)
                if self.get_matriz()[i][j].get_activo():
                    coordenadas_activas.append(self.get_matriz()[i][j].get_id())
        return coordenadas_activas

    def bloquear_tablero(self):
        ''' bloqueo tablero, solo habilito en cruz'''
        coordenadas_activas = self.enlistar_coordenadas_activas()
        adyacente_arriba = (0, -1)
        adyacente_abajo = (0, +1)
        adyacente_izquierda = (-1, 0)
        adyacente_derecha = (+1, 0)

        adyacentes_todas = (adyacente_arriba, adyacente_abajo, adyacente_izquierda, adyacente_derecha)

        if len(coordenadas_activas) == 1:
            for i in adyacentes_todas:
                try:
                    fila_a_desbloquear = coordenadas_activas[0][0]+i[1]
                    columna_a_desbloquear =coordenadas_activas[0][1]+i[0]
                    if fila_a_desbloquear >= 0 and columna_a_desbloquear >= 0:
                        self.get_matriz()[fila_a_desbloquear][columna_a_desbloquear].set_habilitado(True)
                except IndexError:
                    print("Casilla a desbloquear fuera de rango, se ignora")  # Borrar
                    pass

        if len(coordenadas_activas) > 1:
            coordenada_max = max(coordenadas_activas)
            coordenada_min = min(coordenadas_activas)
            horizontal = False
            if coordenada_max[0] != coordenada_min[0]:
                horizontal = True
            if horizontal:
                coordenada_adyacente_izquierda = (coordenada_min[0]-1, coordenada_min[1])
                coordenada_adyacente_derecha = (coordenada_max[0]+1, coordenada_max[1])
                coordenadas_a_desbloquear = [coordenada_adyacente_izquierda, coordenada_adyacente_derecha]
            else:
                coordenada_adyacente_arriba = (coordenada_min[0], coordenada_min[1]-1)
                coordenada_adyacente_abajo = (coordenada_max[0], coordenada_max[1]+1)
                coordenadas_a_desbloquear = [coordenada_adyacente_arriba, coordenada_adyacente_abajo]

            for i in coordenadas_a_desbloquear:
                try:
                    self.get_matriz()[i[0]][i[1]].set_habilitado(True)
                except IndexError:
                    print("Casilla a desbloquear fuera de rango, se ignora")  # borrar
                    pass

    def calcular_puntaje(self, lista, puntaje_letras): #todo creo que no está biennn. Cualquier cosa modificar  agusss
        ''' calcula el puntaje '''
        total = 0
        aumentos = []
        for coor in lista:
            if self.get_matriz()[coor[0]][coor[1]].get_letra() in puntaje_letras.keys():
                total = total + puntaje_letras[self.get_matriz()[coor[0]][coor[1]].get_letra()]
                if (self.get_matriz()[coor[0]][coor[1]].get_premio() != ' '):
                    aumentos.append(self.get_matriz()[coor[0]][coor[1]].get_premio())
        print("puntaje: ", total)
        print(len(aumentos))
        for tipo in aumentos:
            if (tipo == "3P"):
                total = total * 3
            elif(tipo == "3L"):
                total = total + 3
            elif (tipo == "2P"):
                total = total * 2
            elif (tipo == "2L"):
                total = total + 2
            elif (tipo == "2R"):
                total = total - 2
        return total

    def desactivar_coordenadas_activas(self, lista_coordenadas_activas):

        for coor in lista_coordenadas_activas:
            self.get_matriz()[coor[0]][coor[1]].set_activo(False)

    def set_palabra_definitiva(self, lista_coors):
        for coor in lista_coors:
            #eliminar_letra(lista_letras) #hay que hacerlo!!
            self.get_matriz()[coor[0]][coor[1]].set_definitivo(True)



    #METODO VALIDAR PALABRA VIEJO_____________________________________________________
    def validar_pal(self):
        lista_coordenadas_activas = self.enlistar_coordenadas_activas()
        puntaje = self.calcular_puntaje(lista_coordenadas_activas)
        w = Wiktionary(language="es")
        palabra_separada = []
        for coor in lista_coordenadas_activas:
            palabra_separada.append(self.get_matriz()[coor[0]][coor[1]].get_letra())
        palabra = ''.join(palabra_separada)
        analisis = parse(palabra.lower()).split('/')
        if analisis[1] == "JJ" or analisis[1] == "VB":
            self.set_palabra_definitiva(lista_coordenadas_activas)           # la palabra es definitiva
            return (True, puntaje)
        elif (analisis[1] == "NN"):
            article=w.search(palabra.lower())
            if article is not None:
                self.set_palabra_definitiva(lista_coordenadas_activas)
                # la palabra es definitiva
                self.desactivar_coordenadas_activas(lista_coordenadas_activas)
                return (True, puntaje)
            else:

                return (False, 0)
        else:
            return (False, 0)
    #__________________________________________________________________________

    def desbloquear_tablero(self):
        '''desbloquea el tablero menos los botones activos'''
        for i in range(self.get_filas()):
            for j in range(self.get_columnas()):
                if self.get_matriz()[i][j].get_activo():
                    self.get_matriz()[i][j].set_definitivo(True)
                self.get_matriz()[i][j].set_activo(False)
                self.get_matriz()[i][j].set_habilitado(True)

    def validar_palabra(self, palabra, diccionario, palabras_permitidas):
        '''valido una palabra retorno true o false '''
        palabra_valida = False
        print(palabra in diccionario)
        if palabra in diccionario and len (palabra)>2:
            if parse(palabra).split('/')[1] in palabras_permitidas:
                palabra_valida = True
        return palabra_valida

    def click_validar(self, atril, tablero, window, diccionario, puntaje, bolsa , puntaje_letras, juego, palabras_permitidas=('NN', 'JJ', 'VB'), lista_palabras_usadas=[]):
        ''' valido una palabra, si es correcta devuelvo true y calculo el puntaje. paso el turno'''
        coordenadas_activas = tablero.enlistar_coordenadas_activas()
        palabra_en_lista = []
        for coordenada in coordenadas_activas:
            palabra_en_lista.append(self.get_matriz()[coordenada[0]][coordenada[1]].get_letra())

        palabra = ''.join(palabra_en_lista).lower()

        palabra_valida = self.validar_palabra(palabra, diccionario, palabras_permitidas)
        print(palabra_valida)
        if palabra_valida :
           # Fichas.borrar_de_bolsa(palabra,bolsa ) # al final las saco de la bolsa cuando las pongo en el atril
            #calculo el puntaje

            puntaje = puntaje + self.calcular_puntaje(coordenadas_activas, puntaje_letras)
            #agrego letras en el atril
            atril.agregar_letras(bolsa)
            atril.refrescar_atril(window)
            #desbloqueo el tablero (queda bloqueado cuando pongo una letra)
            tablero.desbloquear_tablero()
            #actualizo el puntaje
            window.Element('punt').Update(puntaje)
            #actualizo la lista de palabras usadas
            lista_palabras_usadas.append(palabra)
            window.Element('lista').Update(values=lista_palabras_usadas)

        else:
            #no fue valida la palabra
            #devuelvo las letras al atril
            atril.devolver_fallo(window, tablero)
        #desbloqueo tablero
        tablero.desbloquear_tablero()
        #cambio de turno
        juego.cambiar_turno()
        return puntaje



    def modificar_premios(self,lista, tipo,clave, color):
        ''' segun las tuplas en la lista seteo premios y modifico el aspecto del boton '''
        for valor in lista:
            try:
                self.get_matriz()[valor[0]][valor[1]].set_premio(tipo) # si es palabra x2, letrax2, letrax3
                self.get_matriz()[valor[0]][valor[1]].set_color(color)
            except KeyError:
                continue #por si me equivoque agregando tuplas

    def tablero_comun(self):
        ''' Armo lo que va a ser el tablero comun, modifico en la casilla el nombre, color y valor'''
        self.set_columnas(15)
        self.set_filas(15)
        lista_3p = []
        lista_2p = []
        lista_3l = []
        lista_2l = []
        for i in range(0, 15, 2):
            if ((i-1) != 7) and (i > 0):
                lista_2l.append(((i-1), (i-1)))
            lista_3p.append((i, i))
            lista_3p.append((((self.get_columnas()-1)-i), ((self.get_filas()-1)-i)))
            if (i < 7):
                lista_3p.append((i, 7))
            elif(i > 7):
                lista_2l.append((i, 7))
        self.modificar_premios(lista_3p,'3P','3P','#33FF71') #verde
        self.modificar_premios(lista_2l,'2L','2L','#33D4FF') #naranja
        for i in range(0, 15, 2):
            if ((i-1) != 7) and (i > 0):
                lista_2p.append((((i-1), (self.get_columnas()-1)-i+1)))
            lista_3l.append(((i, (self.get_columnas()-1)-i)))
            lista_3l.append((((self.get_filas()-1)-i), i))
            if (i < 7):
                lista_3l.append((7, i))
            elif(i > 7):
                lista_2p.append((7, i))
        self.modificar_premios(lista_3l,'3L','3L','#334CFF') #azul
        self.modificar_premios(lista_2p,'2P','2P','#FFC133')#celeste

    def modificaciones_principiante(self):

        lista_2r = []
        self.tablero_comun()
        for i in range(6, 9, 2):
            lista_2r.append((i, 5))
            lista_2r.append((5, i))
            lista_2r.append((i, 9))
            lista_2r.append((9, i))
        self.modificar_premios(lista_2r,'2R','2R','#C83C26')

    def modificaciones_intermedio(self):
        lista_2r = []
        self.tablero_comun()
        for i in range(4, 11, 3):
            lista_2r.append((i, 3))
            lista_2r.append((3, i))
            lista_2r.append((i, 11))
            lista_2r.append((11, i))
        self.modificar_premios(lista_2r,'2R','2R','#C83C26')

    def modificaciones_experto(self):
        lista_2r = []
        self.tablero_comun()
        for i in range(2, 13, 2):
            lista_2r.append((i, 1))
            lista_2r.append((1, i))
            lista_2r.append((i, 13))
            lista_2r.append((13, i))
        self.modificar_premios(lista_2r,'2R','2R','#C83C26')

    def crear_tablero(self, nivel='dificultad_facil'):
        '''creo un tablero segun la dificultad elegida'''
        if nivel== 'dificultad_facil':
            self.modificaciones_principiante()
        elif nivel== 'dificultad_media':
            self.modificaciones_intermedio()
        elif nivel=="dificultad_maxima":
            self.modificaciones_experto()
       # else:
        #    self.modificaciones_usuario()
        for x in range( self.get_filas()):
            for y in range(self.get_columnas()):
                try:
                    if (self.get_matriz()[x][y].get_color() == 'white') and (self.get_matriz()[x][y].get_premi() == ' '):
                        self.get_matriz()[x][y].set_color ('white', '#C8C652')
                        self.get_matriz()[x][y].set_premio(' ')
                except:
                    continue
        filas= self.get_filas()
        columnas= self.get_columnas()
        letter_tablero = { 'size' : (2,1), 'pad' : (0,0)} # ACA PODEMOS MODIFICAR EL TAMAN
        layout = [[sg.Button(key = (i, j),button_text= self.get_matriz()[i][j].get_premio(),button_color=('white',self.get_matriz()[i][j].get_color()),  **letter_tablero) for i in range(filas)] for j in range(columnas)]

        return layout
    def cargar_tablero(self,window):
        ''' hago un refresh del tablero actual '''
        for i in range(self.get_filas()):
            for j in range(self.get_columnas()):
                if(self.get_matriz()[i][j].get_letra()!=''  and self.get_matriz()[i][j].get_letra()!=' ' and (not self.get_matriz()[i][j].get_activo())):
                    window.Element((i,j)).Update(self.get_matriz()[i][j].get_letra(), button_color=('white', '#C8C652'))
                    window.Read(timeout=0)

                else:
                    try:
                        window.Element((i, j)).Update(self.get_matriz()[i][j].get_premio(),button_color=('white', self.get_matriz()[i][j].get_color()),)
                        window.read(timeout=0)
                    except():
                        sg.popup('un color no fue reconocido')



