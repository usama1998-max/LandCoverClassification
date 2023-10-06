import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Images
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from .forms import CreateUserForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image
import numpy as np
import tensorflow as tf
import cv2
from django.http import QueryDict


classes = [
    'AnnualCrop',
    'Forest',
    'HerbaceousVegetation',
    'Highway',
    'Industrial',
    'Pasture',
    'PermanentCrop',
    'Residential',
    'River',
    'SeaLake'
]

model = tf.keras.models.load_model("./modal/landcover_classifier")


def check_user_email(email: str) -> bool:
    try:
        User.objects.get(email=email)
        return True
    except ObjectDoesNotExist:
        return False


def home(request):
    request.session['dash_panel'] = "0"
    request.session.modified = True
    return render(request, "home.html", {"title": "Home"})


def register(request):
    cuf = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            if check_user_email(form.cleaned_data['email']) is True:
                messages.error(request, "Email already exists")
            else:
                form.save()

                messages.success(request, "Your account has been created, you can now login.")
                return redirect('signin')
        else:
            messages.error(request, form.errors)

    return render(request, "signup.html", {
                                                                "title": "Signup",
                                                                "uform": cuf
                                                               })


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('home')
        else:
            messages.error(request, "Username or password is incorrect!")

    return render(request, "signin.html", {"title": "Signin"})


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out")
    return redirect('home')


def profile(request):
    return render(request, "profile.html", {"title": f"Welcome {request.user.username}"})


def dashboard(request):
    imgs = Images.objects.filter(user=request.user)

    if request.method == 'POST':
        print(request.POST)

        if 'dash_panel' in request.POST:
            request.session['dash_panel'] = request.POST['dash_panel']
            request.session.modified = True

            return JsonResponse({"dash_panel": request.session['dash_panel']})

        if 'image_classify' in request.POST:
            print("Classification")

        if 'image_segment' in request.POST:

            user = User.objects.get(username=request.user.username)

            img = Images()
            img.img = request.FILES['img']
            img.user = user
            img.save()

            return redirect('dashboard')

    return render(request, "dashboard.html", {
        "title": "Dashboard",
        "dash_panel": request.session['dash_panel'],
        "imgs": imgs
    })


def image_classify(request):
    ...


def image_segment(request):
    ...
