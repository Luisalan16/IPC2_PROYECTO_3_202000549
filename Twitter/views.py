from django.shortcuts import render, redirect
from .forms import formMensaje
from  django.http import HttpResponseRedirect
import requests

# Create your views here.
def PaginaInicio(request):
    return render(request, 'publicacion/index.html', {})

def Home(request):
    return render(request, 'publicacion/inicio.html', {})

def PaginaSubida(request):
    if request.method == 'POST':
        form = formMensaje(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES['archivo'].read().decode('utf-8'))
            url = 'http://127.0.0.1:5000/agregarMensajes'
            Data = {
                'Diccionario': request.FILES['archivo'].read().decode('utf-8')
            }
            data = requests.post(url,Data )
        return HttpResponseRedirect('/twitter/contenido-twitter')
    else:
        form = formMensaje()
        return render(request, 'publicacion/form.html', {'formu': form})

def PaginaCreador(request):
    return render(request, 'publicacion/creador.html', {})

def Configuracion(request):
    return render(request, 'publicacion/configuracion.html', {})

def verMensajes(request):
    contexto = {
        'mensajes': []
    }
    try:
        response = requests.get(endpoint = 'http://127.0.0.1:5000' + 'verMensajes')
        mensajes = response.json()
        contexto['mensajes']= mensajes
    except:
        print('Error')
    return render(request, 'publicacion/verMensajes.html', contexto)

def Documentation(request):
    context = {
        'STATIC_URL': '/static/',
    }
    return render (request, 'publicacion/document.html', context)