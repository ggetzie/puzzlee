from django.urls import include, path
import game.views as views

app_name = "game"

artwork_urls = [
    path("", view=views.ArtworkList.as_view(), name="artwork_list"),
    path("add/", view=views.ArtworkCreate.as_view(), name="artwork_create"),
    path("<int:pk>/", view=views.ArtworkDetail.as_view(), name="artwork_detail"),
]

urlpatterns = [path("artwork/", include(artwork_urls))]
