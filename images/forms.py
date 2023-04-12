from django import forms
from .models import Imagen

class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ("title","img",) 
        labels = {"img": "Image upload"}

        widgets = { 'img': forms.ClearableFileInput(attrs={'class': 'file-upload-input', 'id': 'file-selector', "multiple": True}) }