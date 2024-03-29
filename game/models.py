import datetime
from typing import Literal
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

IMAGE_SIZE = Literal["320", "408", "576", "768", "992", "1200", "orig", "thumbnail"]
BREAKPOINTS = ("1200", "992", "768", "576", "408", "320")


def get_next_featured():
    artworks = Artwork.objects.order_by("-featured")
    if artworks.count() == 0:
        return datetime.date.today()
    last = artworks[0].featured
    return last + datetime.timedelta(days=1)


class Artwork(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    featured = models.DateField(
        "Next featured date", unique=True, default=get_next_featured
    )
    year = models.CharField(max_length=50)
    description = models.TextField(default="", blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField("Created at", default=timezone.now)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.title} - {self.artist}"

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.title}-{self.artist.fullname}-{self.year}")
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("game:artwork_detail", kwargs={"pk": self.pk})


def get_image_path(instance, filename):
    stem, ext = filename.rsplit(".", maxsplit=1)
    ext = ext.lower()
    if ext == "jpg":
        ext = "jpeg"
    path = f"raw/images/artworks/{instance.id}/{stem.lower()}.{ext}"
    return path


class ArtworkImage(models.Model):
    artwork = models.OneToOneField("Artwork", on_delete=models.CASCADE, null=True)
    detailpage = models.OneToOneField(
        "collect.DetailPage", on_delete=models.SET_NULL, null=True
    )
    source = models.URLField()
    image = models.ImageField(upload_to=get_image_path)
    phash = models.CharField(max_length=16, default="")
    average_hash = models.CharField(max_length=16, default="")
    dhash = models.CharField(max_length=16, default="")
    whash = models.CharField(max_length=16, default="")

    def __str__(self):
        if self.artwork:
            return f"image - {self.artwork.title}"
        elif self.detailpage:
            return f"image - {self.detailpage}"
        else:
            return f"ArtworkImage: {self.id}"

    def get_size(self, size: IMAGE_SIZE) -> str:
        # pylint: disable=no-member
        root = self.image.url.rsplit("/", maxsplit=1)[0].replace("/raw/", "/processed/")
        return f"{root}/{size}.jpeg"

    def get_thumb(self):
        return self.get_size("thumbnail")

    def get320(self):
        return self.get_size("320")

    def get576(self):
        return self.get_size("576")

    def get768(self):
        return self.get_size("768")

    def get1200(self):
        return self.get_size("1200")

    def get_orig(self):
        return self.get_size("orig")


class Artist(models.Model):
    fullname = models.CharField("Full Name", max_length=150)
    name_slug = models.SlugField("Name Slug", max_length=150, default="", unique=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField("Created at", default=timezone.now)

    class Meta:
        ordering = ["created_at"]

    def get_absolute_url(self):
        return reverse("game:artist_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.fullname}"

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.fullname)
        return super().save(*args, **kwargs)
