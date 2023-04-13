from django import forms
from .models import Imagen

class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ("title","img",) 
        labels = {"img": "Subir imagen"}

        widgets = {'img': forms.ClearableFileInput(attrs={'class': 'file-upload-input', 'id': 'file-selector', "multiple": True}) }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ("title", "doc",)
        labels = {"doc": "Subir documento"}

        widgets = {'doc': forms.ClearableFileInput(attrs={'class': 'file-upload-input', 'id': 'file-selector', "multiple": True})}