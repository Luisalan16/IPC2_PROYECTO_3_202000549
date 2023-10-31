from django import forms

class FormMensaje(forms.Form):
    file = forms.FileField(label='Cargar archivo XML')
