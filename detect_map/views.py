from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializer import UserSerializer, UserLoginSerializer
from django.contrib.auth import login, logout, authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from PIL import Image
import numpy as np
import tensorflow as tf
import cv2

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


def refresh_user_tkn(user):
    token = RefreshToken.for_user(user)

    return {"refresh": str(token), "access": str(token.access_token)}


@api_view(["POST"])
def register(request):
    us = UserSerializer(data=request.data)

    if us.is_valid() is True:
        user = User(username=request.data['username'])
        hash_pass = make_password(request.data['password'])
        user.password = hash_pass
        user.save()

        tkn = refresh_user_tkn(user)
        return Response({"status": "success", "msg": "User created successfully", "token": tkn})
    else:
        print(us.errors)
        return Response(us.errors)


@api_view(["POST"])
def login_user(request):
    uls = UserLoginSerializer(data=request.data)
    if uls.is_valid() is True:
        username = uls.data['username']
        password = uls.data['password']

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            uid = User.objects.get(username=user)
            tkn = refresh_user_tkn(user)
            return Response({"status": "success",
                             "token": tkn,
                             "msg": "You are now logged in!",
                             "username": str(uid.username)})
        else:
            return Response({"status": "error", "msg": "Invalid Credentials"})
    else:
        return Response(uls.errors)


@api_view(["GET", "POST"])
def logout_user(request):
    return Response({"msg": "User"})


@api_view(["POST"])
def image_classify(request):
    try:
        file = request.FILES['media']
        img = Image.open(file)
        img_arr = np.array(img)
        nsam = tf.image.resize(img_arr, (128, 128))
        ndims = np.expand_dims(nsam/255, 0)
        prediction = model.predict(ndims)
        label = np.argmax(prediction)
        category = classes[int(label)]

        return Response({"msg": "success", "category": category})
    except Exception as e:
        print(e)
        return Response({"msg": "Server Error"})


@api_view(["GET", "POST"])
def image_segment(request):
    return Response({"msg": "User"})

