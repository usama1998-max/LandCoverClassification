from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Images
from django.contrib.auth import login, logout, authenticate
from .forms import CreateUserForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import tensorflow as tf
import cv2
from django.core.paginator import Paginator
import numpy as np


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


def segment_image(img_url, username):
    img = cv2.imread(img_url, 0)
    rimg = cv2.resize(img, (500, 500))
    _, thresholded1 = cv2.threshold(rimg, 140, 255, cv2.THRESH_BINARY_INV)
    _, thresholded2 = cv2.threshold(rimg, 150, 255, cv2.THRESH_TRIANGLE)
    _, labels1 = cv2.connectedComponents(thresholded1)
    _, labels2 = cv2.connectedComponents(thresholded2)
    preview1 = np.zeros((rimg.shape[0], rimg.shape[1], 3), dtype=np.uint8)
    preview2 = np.zeros((rimg.shape[0], rimg.shape[1], 3), dtype=np.uint8)
    preview1[labels1 == 0] = (0, 255, 0)
    preview2[labels2 == 0] = (0, 0, 255)

    file_path = img_url.split('/')
    filename = file_path[-1].split('.')[0]

    cv2.imwrite(f"../media/land_{filename}_{username}.png", preview1)
    cv2.imwrite(f"../media/water_{filename}_{username}.png", preview2)


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
    paginator = Paginator(imgs, 12)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)

    if request.method == 'POST':
        print(request.POST)

        if 'dash_panel' in request.POST:
            request.session['dash_panel'] = request.POST['dash_panel']
            request.session.modified = True
            return JsonResponse({"dash_panel": request.session['dash_panel']})

        if 'upload_img' in request.POST:
            if len(request.FILES) > 0:

                user = User.objects.get(username=request.user.username)

                img = Images()
                img.img = request.FILES['img']
                img.user = user
                img.save()
                print("Image Uploaded")
                messages.success(request, "Image Uploaded successfully, Check recent image tab.")
            else:
                messages.error(request, "You need to upload image first")

            return redirect('dashboard')

        if 'image_classify' in request.POST:

            return redirect('dashboard')

        if 'image_segment' in request.POST:

            return redirect('dashboard')



    return render(request, "dashboard.html", {
        "title": "Dashboard",
        "dash_panel": request.session['dash_panel'],
        "imgs": page,
        "page_no": page
    })


def image_classify(request):
    ...


def image_segment(request):
    ...
