
class Casilla:


    def __init__(self, fila=-1, columna =-1, multiplicador=1):
        self.set_id(fila,columna)
        self.set_activo(False) # Indica si la casilla está en juego, completandose la palabra.
        self.set_habilitado(True) # Indica si el espacio puede ser usado o no.
        self.set_definitivo(False) # Evita la modificación de la casilla definitivamente
        self.set_letra('') # Letra almacenada temporal o definitivamente en la casilla.
        self.set_multiplicador_de_puntos(multiplicador) # Multiplica los puntos de la letra al ocupar la casilla.
        self.set_imagen_fondo('') #String de la dirección de la imagen de fondo.
        self.set_premio(' ')
        self.set_color('white')
        self.set_tiene_letra(False)


#--------------------GETTERS Y SETTERS
    def set_color(self, color):
        self.__color= color

    def get_color(self):
        return self.__color

    def set_tiene_letra(self, tiene_letra):
        self.__tiene_letra = tiene_letra

    def get_tiene_letra(self):
        return self.__tiene_letra


    def set_premio(self, premio):
        self.__premio= premio
    def get_premio(self):
        return self.__premio


#id
    def set_id(self,fila,columna):
        self.__ID= (fila,columna)
    def get_id(self):
        return self.__ID
#activo
    def get_activo(self):
        return self.__activo
    def set_activo(self, value):
        self.__activo = value
#habilitado
    def set_habilitado(self, habilitado):
        self.__habilitado= habilitado
    def get_habilitado(self):
        return self.__habilitado

#__definitivo

    def set_definitivo(self, definitivo):
        self.__definitivo = definitivo
    def get_definitivo(self):
        return self.__definitivo
#letra

    def set_letra(self, letra):
        self.__letra= letra
    def get_letra(self):
        return self.__letra
#__multiplicador_de_puntos

    def set_multiplicador_de_puntos(self,multiplicador):
        self.__multiplicador_de_puntos=multiplicador
    def get_multiplicador_de_puntos(self):
        return self.__multiplicador_de_puntos

#__imagen_fondo

    def set_imagen_fondo(self, imagen):
        self.__imagen_fondo= imagen
    def get_imagen_fondo(self):
        return self.__imagen_fondo

#------------------------------------------------------------------

