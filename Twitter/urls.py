from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaginaInicio, name="PaginaInicio"), # Home
    path('twitter/', views.Home, name="Inicio"), # pagina principal
    path('twitter/subida/', views.cargamasiva, name="Twitter-Inicio"), #pagina para subir xml
    path('twitter/contenido-twitter/', views.verMensajes, name="Contenido-Twitter"), # ver los mensajes
    path('twitter/tags-twitter/', views.verTags, name="Tags"), # ver los hashtags
    path('twitter/usuarios-twitter/', views.verUsuarios, name="Usuarios"), # ver los usuarios
    path('twitter/palabras-twitter/', views.verSentimientos, name="Sentimientos"), # ver las palabras
    path('twitter/archivo-configuracion/', views.cargamasiva2, name="Configuracion"), # pagina para subir configuracion
    path('twitter/creador/', views.PaginaCreador, name="Creador"), # pagina del creador
    path('twitter/documentacion/', views.Documentation, name="Documentacion"), # pagina de la documentacion
    path('twitter/subida/Reset', views.resetear_base, name='Resetear-Base'),
    path('grafico/', views.grafico, name='grafico'),
    path('generar_grafico/', views.generar_grafico, name='generar_grafico'),
     path('generar_reporte_pdf/', views.generar_reporte_pdf, name='generar_reporte_pdf'),
     path('generar_reporte_usuarios_pdf/', views.generar_reporte_usuarios_pdf, name='generar_reporte_usuarios_pdf'),
     path('generar_reporte_mensajes_pdf/', views.generar_reporte_mensajes_pdf, name='generar_reporte_mensajes_pdf'),
]