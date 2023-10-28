import os

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Images, ImageSegment
from django.contrib.auth import login, logout, authenticate
from .forms import CreateUserForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import tensorflow as tf
import cv2
from django.core.paginator import Paginator
import numpy as np


trained_model = tf.keras.models.load_model("./modal/landcover_classifier")


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
    print("Working on segment...")

    land_img = f"land_{filename}_{username}.png"
    water_img = f"water_{filename}_{username}.png"

    cv2.imwrite("D:/PycharmProjects/LandCoverClassification/media/user_imgs_segment/"+land_img, preview1)
    cv2.imwrite("D:/PycharmProjects/LandCoverClassification/media/user_imgs_segment/"+water_img, preview2)

    return [land_img, water_img]


def classify_image(img_url):
    sample = cv2.imread(img_url)
    sample = cv2.cvtColor(sample, cv2.COLOR_BGR2RGB)
    nsam = tf.image.resize(sample, (128, 128))
    prediction = trained_model.predict(np.expand_dims(nsam / 255, 0))
    label = np.argmax(prediction)
    return classes[int(label)]


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


    try:
        img_class = Images.objects.get(user=request.user, img=request.session['img_class'])
        image_classification = request.session['img_pred']
    except Exception:
        img_class = None
        image_classification = None

    try:
        img = Images.objects.get(id=request.session['img_id'])
        image_seg = ImageSegment.objects.get(img_id=img)
    except Exception:
        image_seg = None

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

        if 'classify' in request.POST:
            request.session['dash_panel'] = "1"

            img_class = Images.objects.get(id=request.POST.get('classify'))

            image_classification = classify_image("D:/PycharmProjects/LandCoverClassification/" + img_class.img.url)

            request.session['img_class'] = img_class.img.name
            request.session['img_pred'] = image_classification
            request.session.modified = True
            messages.success(request, f"We found your image belongs to {image_classification} class")

            return redirect('dashboard')

        if 'image_segment' in request.POST:

            return redirect('dashboard')

        if 'del' in request.POST:
            image = Images.objects.get(id=request.POST.get('del'))
            image_segm = ImageSegment.objects.get(img_id=image)

            os.remove("D:/PycharmProjects/LandCoverClassification/media/user_imgs_segment/" + image_segm.land.name)

            os.remove("D:/PycharmProjects/LandCoverClassification/media/user_imgs_segment/" + image_segm.water.name)
            image_segm.delete()

            os.remove("D:/PycharmProjects/LandCoverClassification" + image.img.url)
            image.delete()

            request.session['img_class'] = None
            request.session['img_pred'] = None
            request.session['img_id'] = None
            request.session.modified = True

            messages.success(request, "Image removed successfully")
            return redirect('dashboard')

        if "analyse" in request.POST:
            request.session['dash_panel'] = "2"

            image = Images.objects.get(id=request.POST.get('analyse'))
            image_path = "D:/PycharmProjects/LandCoverClassification"+image.img.url

            img_s = segment_image(image_path, request.user.username)

            try:
                image_seg = ImageSegment.objects.get(img_id=int(request.session['img_seg_id']))
                request.session['img_id'] = image_seg.img_id.id
                request.session.modified = True
                messages.success(request, "Image exist")
            except Exception:
                image_seg = ImageSegment()
                image_seg.img_id = image
                image_seg.land = img_s[0]
                image_seg.water = img_s[1]
                image_seg.save()
                messages.success(request, "Segmentation created!")

                request.session['img_id'] = image_seg.img_id.id
                request.session.modified = True

            return redirect('dashboard')

    return render(request, "dashboard.html", {
        "title": "Dashboard",
        "dash_panel": request.session['dash_panel'],
        "imgs": page,
        "page_no": page,
        "image_segments": image_seg,
        "selected_image_classification": img_class,
        "prediction": image_classification
    })


def image_classify(request):
    ...


def image_segment(request):
    ...
