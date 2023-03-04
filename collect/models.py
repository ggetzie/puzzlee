from django.db import models


class ListPage(models.Model):
    url = models.URLField()
    html = models.TextField(blank=True, default="")
    title = models.CharField(max_length=100, default="")
    last_visited = models.DateTimeField(blank=True, null=True)
    response_code = models.PositiveSmallIntegerField(blank=True, null=True)
    institution = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.title if len(self.title) > 0 else self.url


class DetailPage(models.Model):
    url = models.URLField()
    html = models.TextField(blank=True, default="")
    title = models.CharField(max_length=500, default="")
    attribution = models.CharField(max_length=1000, default="")
    parent = models.ForeignKey(ListPage, on_delete=models.SET_NULL, null=True)
    last_visited = models.DateTimeField(blank=True, null=True)
    response_code = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.title
