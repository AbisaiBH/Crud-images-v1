from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.conf import settings
from .models import Imagen
from .forms import ImagenForm, DocumentForm

from PIL import Image
import os

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username = request.POST['username'],
                    password = request.POST['password1'],
                )
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'La clave no coincide'
        })
    
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                "error": 'El usuario o clave no coinciden',
            })
        else:
            login(request, user)
            return redirect('home')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def upload(request):
    opt = 0
    if request.method == 'POST':
        var = request.POST.get('opcion')
        if var == '1':
            opt = 1
            form = ImagenForm()
            return render(request, 'upload.html', {'form': form, 'opt': opt})
        elif var == '2':
            opt = 2
            form = DocumentForm()
            return render(request, 'upload.html', {'form': form, 'opt': opt})
        title = request.POST.get('title')
        img = request.FILES.getlist('img')
        doc = request.FILES.getlist('doc')
        usg = request.user
        if len(img) == 0:
            for doces in doc:
                documt = Imagen.objects.create(title = title, doc = doces, user = usg)
                return redirect('list')
        if len(doc) == 0:
            for image in img:
                imagen = Imagen.objects.create(title = title, img = image, user = usg)
                compress(imagen)
                return redirect('gallery')      
    else:
        form = ImagenForm()
    return render(request, 'upload.html', {'form': form, 'opt': opt})

@login_required
def gallery(request):
    img = Imagen.objects.filter(user = request.user, doc = "")
    return render(request, 'gallery.html', {'img': img})

@login_required
def list(request):
    doc = Imagen.objects.filter(user = request.user, img = "")
    return render(request, 'list.html', {'doc': doc})

@login_required
def gallery_delete(request, img_id):
    imag = get_object_or_404(Imagen, pk=img_id)
    if request.method == 'POST':
        os.remove(imag.img.path)
        imag.delete()
        return redirect('gallery')
@login_required
def list_delete(request, doc_id):
    docs = get_object_or_404(Imagen, pk=doc_id)
    if request.method == 'POST':
        os.remove(docs.doc.path)
        docs.delete()
        return redirect('list')

def compress(obj):
    originimg = Imagen.objects.get(id=obj.id)
    pilimg = Image.open(originimg.img.path)
    ruta_org = originimg.img.path
    ruta_com = os.path.join(settings.MEDIA_ROOT)
    ruta_comprimido = os.path.join(ruta_com, f"{originimg.title.split('.')[0]}.webp")

    pilimg.save(ruta_comprimido, 'webp', quality=80)
    
    with open(ruta_comprimido, 'rb') as f:
        originimg.img.save(f"{originimg.title.split('.')[0]}.webp", f, save=True)

    os.remove(ruta_org)
    os.remove(ruta_comprimido)