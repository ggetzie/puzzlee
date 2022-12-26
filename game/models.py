from django.db import models


def artwork_image_path(instance, filename):
    stem, ext = filename.rsplit(".", max_split=1)
    ext = ext.lower()
    if ext == "jpg":
        ext = "jpeg"
    path = f"images/artworks/{instance.id}/{stem.lower()}.{ext}"


class Artwork(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    image = models.ImageField("Image", upload_to=artwork_image_path)
    featured = models.DateField("Next featured date", unique=True)
    description = models.TextField(default="", blank=True)


class Artist(models.Model):
    fullname = models.CharField("Full Name", max_length=150)
    answer = models.CharField("Answer", max_length=200)
