from django.shortcuts import render, redirect
from .forms import *
from  django.http import HttpResponseRedirect
import requests

endpoint = 'http://127.0.0.1:5000/'


# Create your views here.
def PaginaInicio(request):
    return render(request, 'publicacion/index.html', {})

def Home(request):
    return render(request, 'publicacion/inicio.html', {})

def PaginaSubida(request):
    if request.method == 'POST':
        form = FormMensaje(request.POST, request.FILES)
        if form.is_valid():
            contenido = form.cleaned_data['file'].read().decode('utf-8')
            
            Data = {
                'Diccionario': contenido
            }
           
            Headers = {'Content-type': 'application/json'}
            data = requests.post(endpoint + 'agregarMensajes', json=Data, headers=Headers)
            return HttpResponseRedirect('/twitter/subida/')
    else:
        form = FormMensaje()
    return render(request, 'publicacion/form.html', {'form': form})

def PaginaCreador(request):
    return render(request, 'publicacion/creador.html', {})

def Configuracion(request):
    return render(request, 'publicacion/configuracion.html', {})

def verMensajes(request):
    contexto = {
        'msj': []
    }
    try:
        response = requests.get(endpoint + 'verMensajes')
        mensajes = response.json()
        contexto['msj']= mensajes
    except:
        print('Error')
    return render(request, 'publicacion/verMensajes.html', contexto)

def Documentation(request):
    context = {
        'STATIC_URL': '/static/',
    }
    return render (request, 'publicacion/document.html', context)

def verDatos(request):
    contexto = {
        'msj' : [],
        'tags' : [],
        'users' : []
    }
    
    try:
        response = requests.get(endpoint + 'consultarDatos') 
        datos = response.json()
        contexto['msj','tags', 'users'] = datos
    except:
        print('Error en la API')   
    return render(request, 'publicacion/verMensajes.html', contexto)



def cargamasiva(request):
    ctx = {
        'content': None,
        'response': None
    }
    if request.method == 'POST':
        form = FormMensaje(request.POST, request.FILES)  # Usamos el formulario personalizado
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']  # Accedemos al campo "file" del formulario
            xml_binary = uploaded_file.read()
            xml = xml_binary.decode('utf-8')
            ctx['content'] = xml
            response = requests.post(endpoint + 'agregarMensajes', data=xml_binary)
            

            if response.ok:
                ctx['response'] = 'Archivo XML cargado correctamente'
            else:
                ctx['response'] = 'Error en el servidor'
    else:
        form = FormMensaje()  # Creamos una instancia vacía del formulario
    ctx['form'] = form  # Añadimos el formulario al contexto
    return render(request, 'publicacion/form.html', ctx)

    