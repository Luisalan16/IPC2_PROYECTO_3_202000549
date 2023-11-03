from flask import  request, jsonify, Blueprint
from controllers.controllers import *
import datetime
from xml.etree import ElementTree as ET
from datetime import timezone
from fpdf import FPDF
from unidecode import unidecode
import re
import json
# creo mi app
mensajes_app = Blueprint("mensajes_app", __name__)
config = Configuracion()
@mensajes_app.route('/home', methods=['GET'])
def home():
    return 'hola'


@mensajes_app.route('/agregarMensajes', methods=['POST'])
def agregarMensajes():
    contMensajes = 0
    try:
        xml = request.data.decode('utf-8')
        root = ET.XML(xml)
       

        for mensaje in root.findall('MENSAJE'):
            fecha = mensaje.find('FECHA').text
            texto = mensaje.find('TEXTO').text

            # Limpiar texto: eliminar acentos y convertir a minúsculas
            texto = unidecode(texto).lower()

            hashtags_encontrados = re.findall(r'#\w+', texto)
            menciones_encontradas = re.findall(r'@\w+', texto)
            fecha = unidecode(fecha).lower()

            for hashtag in hashtags_encontrados:
                config.setHashtags(hashtag, fecha)
            for user in menciones_encontradas:
                config.setMenciones(user, fecha)

            config.setMensajes(fecha, texto)
            
            contMensajes += 1

        return jsonify({
            'respuesta': 'Mensajes procesados con éxito',
            'mensajes agregados': contMensajes
        })
        
    except Exception as e:
        print("Error:", str(e))
        return jsonify({
            'respuesta': 'Error en la solicitud'
        })


""" @mensajes_app.route('/verHashtags', methods=['GET'])
def verHashtags():
    tags = config.getTags()
    return jsonify(tags),200 """

@mensajes_app.route('/consultarDatos', methods=['GET'])
def verMensajes():
    msj = config.getMensajes()
    tags = config.getTags()
    users = config.getUsers()
    
    return jsonify(msj, tags, users),200

""" CONSULTAS DE LA API """
@mensajes_app.route('/verMensajes', methods=['GET'])
def getMensajes():
    fechas, mensajes = config.getMensajes()
    data = {'fechas': fechas, 'mensajes': mensajes}
    return jsonify(data), 200

@mensajes_app.route('/verHashtags', methods = ['GET'])
def getTags():
    fechas, tags = config.getTags()
    data = {'fechas': fechas, 'tags': tags}
    return jsonify(data), 200

@mensajes_app.route('/verUsuarios', methods = ['GET'])
def getUsuarios():
    fechas, usuarios = config.getUsers()
    data = {'fechas': fechas, 'usuarios': usuarios}
    return jsonify(data), 200

@mensajes_app.route('/verPalabras', methods = ['GET'])
def getSentimientos():
    buenos, malas = config.getConfiguracion()
    data = {'buenos': buenos, 'malas': malas}
    return jsonify(data), 200

""" @mensajes_app.route('/verMensajes', methods = ['GET'])
def getMensajes():
    mensajes = config.getMensajes()
    print(mensajes)
    return jsonify(mensajes),200 """

@mensajes_app.route('/verConfiguracion', methods = ['GET'])
def verConfiguracion():
    configuracion = config.getConfiguracion()
    return jsonify(configuracion),200

@mensajes_app.route('/verDatos', methods=['GET'])
def getConsulta():
    data = config.consultarData()
    return jsonify(data),200

@mensajes_app.route('/agregarConfiguracion', methods = ['POST'])
def agregarConfiguracion():
    contPalabras = 0  
    try:
        xml = request.data.decode('utf-8')
        root = ET.fromstring(xml)

        sentimientos_positivos = root.find('sentimientos_positivos')
        sentimientos_negativos = root.find('sentimientos_negativos')

        palabras_positivas = []
        palabras_negativas = []

        if sentimientos_positivos is not None:
            palabras_positivas = [unidecode(palabra.text).lower() for palabra in sentimientos_positivos.findall('palabra')]

        if sentimientos_negativos is not None:
            palabras_negativas = [unidecode(palabra.text).lower() for palabra in sentimientos_negativos.findall('palabra')]

        config.setConfiguracion(palabras_positivas, palabras_negativas)
       

        return jsonify({
            'respuesta': 'Palabras procesadas con éxito',
            'palabras agregadas': len(palabras_positivas) + len(palabras_negativas),
            'Mensajes con sentimiento positivo': len(palabras_positivas),
            'Mensajes con sentimiento negativo': len(palabras_negativas)
        })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({
            'respuesta': 'Error en la solicitud'
        })

@mensajes_app.route('/resetearDatos', methods = ['POST'])
def resetearDatos():
    config.resetearBaseDeDatos()
    return jsonify({
        'respuesta': 'Base de datos restablecida con éxito'
    })

    """ try:
        config.configuraciones = []
        config.menciones = []
        config.mensajes = []
        config.hashtags_ = []
        config.feelings = []
        return jsonify({
            'respuesta': 'Datos reseteados con éxito',
        })
    except Exception as e:
        print("Error:", str(e))
        return jsonify({
            'respuesta': 'Error al resetear los datos'
        }) """

""" @mensajes_app.route('/cargaArchivo', methods = ['POST'])
def cargaArchivo():
    resultado = Lectura()
    return(resultado)
 """




