from flask import  request, jsonify, Blueprint
from controllers.controllers import *
# creo mi app
mensajes_app = Blueprint("mensajes_app", __name__)

@mensajes_app.route('/home', methods=['GET'])
def home():
    return 'hola'

@mensajes_app.route('/cargar_mensajes', methods=['GET'])
def cargar_mensajes():
    mensajes = Mensaje

