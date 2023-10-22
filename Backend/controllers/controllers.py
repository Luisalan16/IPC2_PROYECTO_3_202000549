import xml.etree.ElementTree as ET
import os

class Configuracion:
    def __init__(self) -> None:
        self.palabras_positivas = []
        self.palabras_negativas = []
        self.mensajes = []
        self.hashtags_ = []
        self.menciones = []
        self.feelings = []
        self.simbolos = "@(_?-+:[0-9]"

    def setPalabrasBonitas(self, palabras_positivas):
        set = Sentimiento_positivo(palabras_positivas)
        self.palabras_positivas.append(set)
    
    def setPalabrasBonitas(self, palabras_negativas):
        set = Sentimiento_negativo(palabras_negativas)
        self.palabras_negativas.append(set)
    
    def setMensajes(self, date, text):
        mensaje = Mensaje(date, text)
        self.mensajes.append(mensaje)

    # Método para consultar datos
    def consultarData(self):
        json = []
        for i in self.hashtags_:
            hashtag = {
                'Datos':'Hashtags',
                'hashtag': i.hashtags,
                'fecha': i.date
            }
            json.append(hashtag)
        for i in self.menciones:
            mencion = {
                'Datos':'Menciones de usuarios',
                'usuario': i.user,
                'fecha': i.date
            }
            json.append(mencion)
        for i in self.feelings:
            feel = {
                'Datos':'Sentimientos de usuarios',
                'sentimientos_buenos': i.good_feelings,
                'sentimientos_malos': i.bad_feelings,
                'fecha': i.date
            }
            json.append(feel)
    
    def getMensajes(self):
        json = []
        for i in self.mensajes:
            mensaje = {
                'fecha': i.date,
                'texto': i.text
            }
            json.append(mensaje)


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
    
class Sentimiento_positivo:
    def __init__(self, palabras_positivas):
        self.palabras_positivas = palabras_positivas
       
class Sentimiento_negativo:
    def __init__(self, palabras_negativas):
        self.palabras_positivas = palabras_negativas

    """ @classmethod
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

        return cls(config['palabras_positivas'], config['palabras_negativas']) """