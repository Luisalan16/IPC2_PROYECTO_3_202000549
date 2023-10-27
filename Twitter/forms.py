from django import forms

class formMensaje(forms.Form):
    archivo = forms.FileField()