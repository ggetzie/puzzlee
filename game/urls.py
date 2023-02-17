from django.urls import include, path
import game.views as views

app_name = "game"

artwork_urls = [
    path("", view=views.ArtworkList.as_view(), name="artwork_list"),
    path("add/", view=views.ArtworkCreate.as_view(), name="artwork_create"),
    path("<int:pk>/", view=views.ArtworkDetail.as_view(), name="artwork_detail"),
]

artist_urls = [
    path("", view=views.ArtistList.as_view(), name="artist_list"),
    path("add/", view=views.ArtistCreate.as_view(), name="artist_create"),
    path("<int:pk>/", view=views.ArtistDetail.as_view(), name="artist_detail"),
]

urlpatterns = [
    path("artwork/", include(artwork_urls)),
    path("artist/", include(artist_urls)),
]
