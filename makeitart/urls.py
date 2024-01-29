from django.urls import include, path
import makeitart.views as views

app_name = "makeitart"

urlpatterns = [
    path("upload", view=views.UploadUserImage.as_view(), name="userimage_upload"),
    path(
        "image/<uuid:pk>", view=views.UserImageDetail.as_view(), name="userimage_detail"
    ),
]
