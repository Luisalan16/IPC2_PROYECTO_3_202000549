import xml.etree.ElementTree as ET
import os

class Gestor:
    def __init__(self) -> None:
        self.palabras = []
        self.hashtags = []
        self.menciones = []
        self.feelings = []
        self.simbolos = "@(_?-+:[0-9]"

    def setPalabrasBonitas(self, palabras_positivas,palabras_negativas):
        set = Configuracion(palabras_positivas, palabras_negativas)
        self.palabras.append(set)

    def setHashtags(self, hashtags, date):
        set = Hashtag(hashtags, date)
        self.hashtags.append(set)

    def setMenciones(self, user, date):
        set = Mencion(user, date)
        self.menciones.append(set)

# Para las consultas
class Hashtag:
    def __init__(self, hashtags, date) -> None:
        self.hastags = hashtags
        self.date = date
        self.mensajes = []

class Mencion:
    def __init__(self, user, date) -> None:
        self.user = user 
        self.date = date
        self.mensajes = []

class Sentimiento:
    def __init__(self, good_feelings,bad_feelings, date) -> None:
        self.good_feelings = good_feelings
        self.bad_feelings = bad_feelings
        self.date = date
        self.mensajes = []

# -----------------------------------------------------------------------------------------------------

class Mensaje:
    def __init__(self, date, text):
        self.date = date
        self.text = text

    def cargar_mensajes(valor, ruta):
        mensajes = []
        if os.path.exists(ruta):
            tree = ET.parse(ruta)
            root = tree.getroot()
            for mensaje in root.findall('MENSAJE'):
                text = mensaje.find('TEXTO').text
                date = mensaje.find('FECHA').text
                mensajes.append(valor(date, text))
        return mensajes
    
class Configuracion:
    def __init__(self, palabras_positivas, palabras_negativas):
        self.palabras_positivas = palabras_positivas
        self.palabras_negativas = palabras_negativas

    @classmethod
    def load_config(cls, file_path):
        config = {
            'palabras_positivas': set(),
            'palabras_negativas': set()
        }
        if os.path.exists(file_path):
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Procesar las palabras positivas
            palabras_positivas = root.find('sentimientos_positivos')
            if palabras_positivas is not None:
                for palabra in palabras_positivas:
                    config['palabras_positivas'].add(palabra.text)
            
            # Procesar las palabras negativas
            palabras_negativas = root.find('sentimientos_negativos')
            if palabras_negativas is not None:
                for palabra in palabras_negativas:
                    config['palabras_negativas'].add(palabra.text)

        return cls(config['palabras_positivas'], config['palabras_negativas'])