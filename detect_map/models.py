from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.FileField(upload_to="user_imgs", default="")
    date = models.DateTimeField(auto_now_add=True, null=True)


class ImageSegment(models.Model):
    img_id = models.OneToOneField(Images, on_delete=models.CASCADE, primary_key=True)
    segment = models.FileField(upload_to="user_imgs_segment", default="")


class ImageSimilarity(models.Model):
    img1 = models.OneToOneField(Images, on_delete=models.CASCADE, primary_key=True)
    img2 = models.FileField(upload_to="user_imgs_similarity", default="")
    img_result = models.FileField(upload_to="user_imgs_similarity", default="", null=True, blank=True)
    img_similarity_score = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)


class ImageRGB(models.Model):
    img_id = models.OneToOneField(Images, on_delete=models.CASCADE, primary_key=True)
    rgb = models.FileField(upload_to="rgb_imgs", default="")
    canny = models.FileField(upload_to="rgb_imgs", default="")

