from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

USER = get_user_model()


def get_image_path(instance, filename):
    _, ext = filename.rsplit(".", maxsplit=1)
    ext = ext.lower()
    if ext == "jpg":
        ext = "jpeg"
    path = f"raw/images/users/{instance.user.id}/{instance.id}.{ext}"
    return path


class UserImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    image = models.ImageField(upload_to="raw/images/users/")
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    phash = models.CharField(max_length=16, default="")
    average_hash = models.CharField(max_length=16, default="")
    dhash = models.CharField(max_length=16, default="")
    whash = models.CharField(max_length=16, default="")
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("makeitart:userimage_detail", kwargs={"pk": self.pk})
