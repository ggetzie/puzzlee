from django.db import models
from django.urls import reverse


class ListPage(models.Model):
    url = models.URLField()
    html = models.TextField(blank=True, default="")
    title = models.CharField(max_length=100, default="")
    last_visited = models.DateTimeField(blank=True, null=True)
    response_code = models.PositiveSmallIntegerField(blank=True, null=True)
    institution = models.CharField(max_length=20, default="")

    class Meta:
        ordering = ("institution", "url")

    def __str__(self):
        return self.title if len(self.title) > 0 else self.url

    def get_absolute_url(self):
        return reverse("collect:listpage_detail", kwargs={"pk": self.pk})


class DetailPage(models.Model):
    url = models.URLField()
    html = models.TextField(blank=True, default="")
    title = models.CharField(max_length=500, default="")
    attribution = models.CharField(max_length=1000, default="")
    parent = models.ForeignKey(ListPage, on_delete=models.SET_NULL, null=True)
    last_visited = models.DateTimeField(blank=True, null=True)
    response_code = models.PositiveSmallIntegerField(blank=True, null=True)
    tokens = models.ManyToManyField("AttributionToken")
    approved = models.PositiveSmallIntegerField(
        choices=((0, "Rejected"), (1, "Unset"), (2, "Approved")), default=1
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("collect:detailpage_detail", kwargs={"pk": self.pk})


class AttributionToken(models.Model):
    value = models.CharField(max_length=200)

    class Meta:
        ordering = ("value",)

    def __str__(self):
        return self.value[:100]

    def get_absolute_url(self):
        return reverse("collect:attributetoken_detail", kwargs={"pk": self.pk})
