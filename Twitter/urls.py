from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaginaInicio, name="PaginaInicio"),
    path('twitter/', views.Home, name="Incio"),
    path('twitter/subida', views.PaginaSubida, name="Twitter-Incio"),
    path('twitter/contenido-twitter', views.verMensajes, name="Contenido-Twitter"),
    path('twitter/archivo-configuracion/', views.Configuracion, name="Configuracion"),
    path('twitter/creador/', views.PaginaCreador, name="Creador"),
    path('twitter/documentacion/', views.Documentation, name="Documentacion"),
]