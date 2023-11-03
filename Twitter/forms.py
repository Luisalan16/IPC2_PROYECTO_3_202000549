from django import forms

# Formulario para subir archivos
class FormMensaje(forms.Form):
    file = forms.FileField(label='Cargar archivo XML')

