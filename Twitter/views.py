from django.shortcuts import render, redirect
from .forms import *
from  django.http import HttpResponseRedirect, HttpResponse
import requests
from django.http import JsonResponse
import os
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import xml.etree.ElementTree as ET
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
        'mensajes': [],
        'fechas': [],  # Agregar una lista vacía para las fechas
    }
    try:
        response = requests.get(endpoint + 'verMensajes')
        data = response.json()
        contexto['mensajes'] = data['mensajes']
        contexto['fechas'] = data['fechas']  # Agregar las fechas al contexto

        print(contexto['mensajes'])
        print(contexto['fechas'])  # Para verificar que las fechas se han cargado correctamente

    except:
        print('Error')
    return render(request, 'publicacion/verMensajes.html', contexto)

def verTags(request):
    contexto = {
        'tags': [],
        'fechas': []
    }
    try:
        response = requests.get(endpoint + 'verHashtags')
        data = response.json()
        contexto['tags'] = data['tags']
        contexto['fechas'] = data['fechas'] 
    except:
        print('Error')
    return render(request, 'publicacion/verTags.html', contexto)

def verUsuarios(request):
    contexto = {
        'usuarios': [],
        'fechas': []
    }
    try:
        response = requests.get(endpoint + 'verUsuarios')
        data = response.json()
        contexto['usuarios'] = data['usuarios']
        contexto['fechas'] = data['fechas'] 
    except:
        print('Error')
    return render(request, 'publicacion/verUsuarios.html', contexto)

def verSentimientos(request):
    contexto = {
        'buenos': [],
        'malos': []
    }
    try:
        response = requests.get(endpoint + 'verPalabras')
        response.raise_for_status()
        data = response.json()
        
        # Verifica si 'malos' y 'buenos' están presentes en el diccionario
        if 'malos' in data:
            contexto['malos'] = data['malos']
        else:
            contexto['malos'] = []  # O proporciona un valor predeterminado

        if 'buenos' in data:
            contexto['buenos'] = data['buenos']
        else:
            contexto['buenos'] = []  # O proporciona un valor predeterminado

    except requests.exceptions.RequestException as e:
        print('Error al obtener datos de verSentimientos:', str(e))
    except Exception as e:
        print('Error inesperado:', str(e))

    return render(request, 'publicacion/verPalabras.html', contexto)




    """ contexto = {
        'mensajes': [],
    }
    try:
        response = requests.get(endpoint + 'verMensajes')
        mensajes = response.json()
        contexto['mensajes'] = mensajes['mensajes']  
        
        print(contexto['mensajes'])

    except:
        print('Error')
    return render(request, 'publicacion/verMensajes.html', contexto) """

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

def cargamasiva2(request):
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
            response = requests.post(endpoint + 'agregarConfiguracion', data=xml_binary)
            

            if response.ok:
                ctx['response'] = 'Archivo XML cargado correctamente'
            else:
                ctx['response'] = 'Error en el servidor'
    else:
        form = FormMensaje()  # Creamos una instancia vacía del formulario
    ctx['form'] = form  # Añadimos el formulario al contexto
    return render(request, 'publicacion/form2.html', ctx)

def resetear_base(request):
    if request.method == 'POST':
        try:
            # Llama al método resetearBaseDeDatos en tu lógica o modelo
            configuracion = Configuracion()
            configuracion.resetearBaseDeDatos()
            return redirect('publicacion/form.html')  # Reemplaza 'nombre_de_la_vista' con el nombre de la vista a la que quieres redirigir
        except Exception as e:
            return JsonResponse({'respuesta': 'Error al restablecer la base de datos'})
    else:
        return JsonResponse({'respuesta': 'Solicitud no válida'})

def grafico(request):
    return render(request, 'publicacion/grafico.html')

def generar_grafico(request):
    # Datos de ejemplo de fechas y mensajes
    fechas = ['2023-11-01', '2023-11-02', '2023-11-03']
    mensajes = ['Mensaje 1', 'Mensaje 2', 'Mensaje 3']

    # Crear un gráfico de barras
    plt.figure(figsize=(8, 4))  # Tamaño del gráfico
    plt.bar(fechas, mensajes, color='blue')  # Crear barras

    # Personalizar el gráfico
    plt.xlabel('Fecha')
    plt.ylabel('Mensaje')
    plt.title('Tabla de Mensajes')
    plt.xticks(rotation=45)  # Rotar las etiquetas de fecha para mayor legibilidad
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Agregar una cuadrícula horizontal

    # Guardar el gráfico en un objeto BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Generar la respuesta con la imagen del gráfico
    response = HttpResponse(buffer.read(), content_type='image/png')
    response['Content-Disposition'] = 'inline; filename=grafico.png'

    return response

def generar_reporte_pdf(request):
    
    contexto = {
        'tags': [],
        'fechas': []
    }
    try:
        response = requests.get(endpoint + 'verHashtags')
        data = response.json()
        contexto['tags'] = data['tags']
        contexto['fechas'] = data['fechas'] 
    except:
        print('Error al obtener datos de verTags')

    
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

   
    c.setFont("Helvetica", 18)
    c.drawString(100, 750, "Reporte de Mensajes")


    c.setFont("Helvetica", 12)
    y_offset = 700
    for fecha, mensaje in zip(contexto['fechas'], contexto['tags']):
        c.drawString(100, y_offset, f"Fecha: {fecha}")
        c.drawString(100, y_offset - 20, f"Mensaje: {mensaje}")
        y_offset -= 40


    c.showPage()
    c.save()

    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=reporte_mensajes.pdf'

    return response

def generar_reporte_usuarios_pdf(request):
    # Obtén los datos de la vista 'verUsuarios'
    contexto = {
        'usuarios': [],
        'fechas': []
    }
    try:
        response = requests.get(endpoint + 'verUsuarios')
        data = response.json()
        contexto['usuarios'] = data['usuarios']
        contexto['fechas'] = data['fechas']
    except:
        print('Error al obtener datos de verUsuarios')

    # Crear un archivo PDF en memoria
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Agregar el título al PDF
    c.setFont("Helvetica", 18)
    c.drawString(100, 750, "Reporte de Usuarios")

    # Agregar los datos de la tabla al PDF
    c.setFont("Helvetica", 12)
    y_offset = 700
    for fecha, usuario in zip(contexto['fechas'], contexto['usuarios']):
        c.drawString(100, y_offset, f"Fecha: {fecha}")
        c.drawString(100, y_offset - 20, f"Usuario: {usuario}")
        y_offset -= 40

    # Guardar el PDF
    c.showPage()
    c.save()

    # Preparar el archivo PDF para su descarga
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=reporte_usuarios.pdf'

    return response

def generar_reporte_mensajes_pdf(request):
    # Obtén los datos de la vista 'verMensajes'
    contexto = {
        'mensajes': [],
        'fechas': []
    }
    try:
        response = requests.get(endpoint + 'verMensajes')
        data = response.json()
        contexto['mensajes'] = data['mensajes']
        contexto['fechas'] = data['fechas']
    except:
        print('Error al obtener datos de verMensajes')

    # Crear un archivo PDF en memoria
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Agregar el título al PDF
    c.setFont("Helvetica", 18)
    c.drawString(100, 750, "Reporte de Mensajes")

    # Agregar los datos de la tabla al PDF
    c.setFont("Helvetica", 12)
    y_offset = 700
    for fecha, mensaje in zip(contexto['fechas'], contexto['mensajes']):
        c.drawString(100, y_offset, f"Fecha: {fecha}")
        c.drawString(100, y_offset - 20, f"Mensaje: {mensaje}")
        y_offset -= 40

    # Guardar el PDF
    c.showPage()
    c.save()

    # Preparar el archivo PDF para su descarga
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=reporte_mensajes.pdf'

    return response

def generar_reporte_sentimientos_pdf(request):
    # Obtén los datos de la vista 'verSentimientos'
    contexto = {
        'buenos': [],
        'malos': []
    }
    try:
        response = requests.get(endpoint + 'verPalabras')
        data = response.json()
        contexto['buenos'] = data['buenos']
        contexto['malos'] = data['malos']
    except:
        print('Error al obtener datos de verSentimientos')

    # Crear un archivo PDF en memoria
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Agregar el título al PDF
    c.setFont("Helvetica", 18)
    c.drawString(100, 750, "Reporte de Sentimientos")

    # Agregar los datos de la tabla al PDF
    c.setFont("Helvetica", 12)
    y_offset = 700
    for palabra_buena, palabra_mala in zip(contexto['buenos'], contexto['malos']):
        c.drawString(100, y_offset, f"Palabra buena: {palabra_buena}")
        c.drawString(100, y_offset - 20, f"Palabra mala: {palabra_mala}")
        y_offset -= 40

    # Guardar el PDF
    c.showPage()
    c.save()

    # Preparar el archivo PDF para su descarga
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=reporte_sentimientos.pdf'

    return response

def generar_xml_de_salida(request):
    # Obten la información del contador de alguna manera.
    contador = [
        {"fecha": "01/01/2023", "mensajes": 10, "usuarios_mencionados": 5, "hashtags_incluidos": 3},
        {"fecha": "02/01/2023", "mensajes": 15, "usuarios_mencionados": 7, "hashtags_incluidos": 4},
    ]

    # Crear el elemento raíz del XML
    root = ET.Element('Informe')

    # Iterar sobre la información del contador y crear elementos para cada fecha
    for info in contador:
        fecha_element = ET.SubElement(root, 'FECHA')
        fecha_element.text = info['fecha']

        mensajes_element = ET.SubElement(root, 'Cantidad_de_mensajes_recibidos')
        mensajes_element.text = str(info['mensajes'])

        usuarios_element = ET.SubElement(root, 'Cantidad_de_usuarios_mencionados')
        usuarios_element.text = str(info['usuarios_mencionados'])

        hashtags_element = ET.SubElement(root, 'Cantidad_de_hashtags_incluidos')
        hashtags_element.text = str(info['hashtags_incluidos'])

    # Crear un objeto ElementTree
    tree = ET.ElementTree(root)

    # Crear una respuesta HTTP con el contenido del XML
    response = HttpResponse(content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename=reporte_mensajes.xml'
    tree.write(response, encoding='utf-8')

    return response