from flask import  request, jsonify, Blueprint
from controllers.controllers import *
import datetime
from xml.etree import ElementTree as ET
from datetime import timezone
from fpdf import FPDF

# creo mi app
mensajes_app = Blueprint("mensajes_app", __name__)
config = Configuracion()
@mensajes_app.route('/home', methods=['GET'])
def home():
    return 'hola'

@mensajes_app.route('/cargar_mensajes', methods=['GET'])
def cargar_mensajes():
    mensajes = Mensaje

@mensajes_app.route('/agregarMensajes', methods=['POST'])
def agregarMensajes():
    contMensajes = 0
    try:
        xml = request.data.decode('utf-8')
        root = ET.fromstring(xml)
        mensajes = root.findall('MENSAJE')

        for mensaje in mensajes:
            fecha = mensaje.find('FECHA').text
            texto = mensaje.find('TEXTO').text
            
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
    """ try:
        xml = request.data.decode('utf-8')
        archivo = ET.XML(xml)
        for mensaje in archivo:
            config.setMensajes(mensaje('FECHA').text, mensaje('TEXTO').text)
            contMensajes +=1
        return jsonify({
            'archivo':'Cargado con éxito',
            'mensajes agregados':contMensajes
        })
    except Exception as e:
        print("Error", str(e))
        return jsonify({
            'archivo': 'Error'
        }) """
