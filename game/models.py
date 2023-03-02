import datetime
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


def artwork_image_path(instance, filename):
    stem, ext = filename.rsplit(".", maxsplit=1)
    ext = ext.lower()
    if ext == "jpg":
        ext = "jpeg"
    path = f"images/artworks/{instance.id}/{stem.lower()}.{ext}"
    return path


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
    image = models.ImageField("Image", upload_to=artwork_image_path)
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


class Artist(models.Model):
    fullname = models.CharField("Full Name", max_length=150)
    answer = models.CharField("Answer", max_length=150)
    answer_slug = models.SlugField("Answer Slug", max_length=150)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField("Created at", default=timezone.now)

    class Meta:
        ordering = ["created_at"]

    def get_absolute_url(self):
        return reverse("game:artist_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.fullname

    def save(self, *args, **kwargs):
        self.answer_slug = slugify(self.answer)
        return super().save(*args, **kwargs)

    def check_guess(self, guess):
        return slugify(guess) == self.answer_slug
