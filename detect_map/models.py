from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.FileField(upload_to="user_imgs", default="")
    date = models.DateTimeField(auto_now_add=True, null=True)


class ImageSegment(models.Model):
    img_id = models.OneToOneField(Images, on_delete=models.CASCADE, primary_key=True)
    land = models.FileField(upload_to="user_imgs_segment", default="")
    water = models.FileField(upload_to="user_imgs_segment", default="")


