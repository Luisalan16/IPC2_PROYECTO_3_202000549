import xml.etree.ElementTree as ET
from flask import json
import re

class Configuracion:
    def __init__(self) -> None:
        self.configuraciones = []
        self.mensajes = []
        self.hashtags_ = []
        self.menciones = []
        self.feelings = []
        self.simbolos = "@(_?-+:[0-9]"

    def setConfiguracion(self, palabras_positivas, palabras_negativas):
        set = Sentimiento(palabras_positivas, palabras_negativas)
        self.configuraciones.append(set)

    def reiniciarDiccionario(self):
        root = ET.Element('Diccionario')
        PalabrasBonitas = ET.SubElement(root, 'PalabrasBonitas')
        PalabrasFeas = ET.SubElement(root, 'PalabrasFeas')
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write('controllers/Diccionario.xml', encoding='utf-8')

    def resetearBaseDeDatos(self):
        self.configuraciones = []
        self.mensajes = []
        self.hashtags_ = []
        self.menciones = []
        self.feelings = []
    
    
    def setMensajes(self, date, text):
        s = re.compile(r'(\d{2})/(\d{2})/(\d{4})')
        date = s.search(date)
        mensaje = Mensaje(date.group(), text)
        self.mensajes.append(mensaje)
    
    def setHashtags(self, hashtags, date):
        set = Hashtag(hashtags, date)
        self.hashtags_.append(set)

    def setMenciones(self, user, date):
        set = Mencion(user, date)
        self.menciones.append(set)
    

    def getConfiguracion(self):
        positivo = []
        negativo = []
        for i in self.configuraciones:
            sentimiento_positivo = i.good_feelings,
            sentimiento_negativo = i.bad_feelings
            positivo.append(sentimiento_positivo)
            negativo.append(sentimiento_negativo)
        return positivo, negativo


    def getMensajes(self):
        fechas = []
        msjs = []
        for i in self.mensajes:
            fecha = i.date
            texto = i.text
            fechas.append(fecha)
            msjs.append(texto)
        return fechas, msjs
    
    def getUsers(self):
        fechas = []
        usuarios = []
        for i in self.menciones:
            usuario = i.user
            fecha = i.date
            fechas.append(fecha)
            usuarios.append(usuario)
        return fechas, usuarios
    
    def getTags(self):
        fechas = []
        tags = []
        for i in self.hashtags_:
            tag = i.hashtags
            fecha = i.date
            
            fechas.append(fecha)
            tags.append(tag)
        return fechas, tags


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
                'sentimientos_buenos': i.palabras_positivas,
                'sentimientos_malos': i.palabras_negativas,
                'fecha': i.date
            }
            json.append(feel)
        return json
    
    
    

# Para las consultas
class Hashtag:
    def __init__(self, hashtags, date) -> None:
        self.hashtags = hashtags
        self.date = date
        self.mensajes = []

class Mencion:
    def __init__(self, user, date) -> None:
        self.user = user 
        self.date = date
        self.mensajes = []

class Sentimiento:
    def __init__(self, good_feelings,bad_feelings) -> None:
        self.good_feelings = good_feelings
        self.bad_feelings = bad_feelings
        self.mensajes = []

# -----------------------------------------------------------------------------------------------------

class Mensaje:
    def __init__(self, date, text):
        self.date = date
        self.text = text

    
    
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