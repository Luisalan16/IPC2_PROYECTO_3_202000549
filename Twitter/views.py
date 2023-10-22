from django.shortcuts import render

# Create your views here.
def PaginaInicio(request):
    return render(request, 'publicacion/index.html', {})

def PaginaSubida(request):
    return render(request, 'publicacion/plantilla.html', {})