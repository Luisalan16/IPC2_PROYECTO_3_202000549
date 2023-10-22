from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaginaInicio, name="PaginaInicio"),
    path('twitter/', views.PaginaSubida, name="Twitter-Incio"),
]