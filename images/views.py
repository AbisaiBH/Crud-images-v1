from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Imagen
from .forms import ImagenForm

from PIL import Image
import os

# Create your views here.

def home(request):
    return render(request, 'home.html')

def upload(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        img = request.FILES.getlist('img')
        for image in img:
            imagen = Imagen.objects.create(title = title, img = image)
            compress(imagen)
        return redirect('upload')      
    else:
        form = ImagenForm()
    return render(request, 'upload.html', {'form': form})

def gallery(request):
    img = Imagen.objects.all()
    return render(request, 'gallery.html', {'img': img})

def gallery_delete(request, img_id):
    imag = get_object_or_404(Imagen, pk=img_id)
    if request.method == 'POST':
        os.remove(imag.img.path)
        imag.delete()
        return redirect('gallery')

def compress(obj):
    originimg = Imagen.objects.get(id=obj.id)
    pilimg = Image.open(originimg.img.path)
    ruta_org = originimg.img.path
    ruta_com = os.path.join(settings.MEDIA_ROOT, 'webp')
    ruta_comprimido = os.path.join(ruta_com, f"{originimg.title.split('.')[0]}.webp")

    pilimg.save(ruta_comprimido, 'webp', quality=80)
    
    with open(ruta_comprimido, 'rb') as f:
        originimg.img.save(f"{originimg.title.split('.')[0]}.webp", f, save=True)
        
    os.remove(ruta_org)
    os.remove(ruta_comprimido)