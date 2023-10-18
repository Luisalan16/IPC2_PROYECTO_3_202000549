from flask import Flask
from routes.routes import mensajes_app

app = Flask(__name__)
app.register_blueprint(mensajes_app)