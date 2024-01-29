from typing import Dict, Any
from core.views import UserIsStaffMixin
from .forms import UserImageUploadForm
from .models import UserImage
from django.views.generic import CreateView, DetailView
from django.shortcuts import render


class UploadUserImage(UserIsStaffMixin, CreateView):
    form_class = UserImageUploadForm
    template_name = "makeitart/userimage_upload.html"

    def get_initial(self) -> Dict[str, Any]:
        res = super().get_initial()
        res["user"] = self.request.user
        return res


class UserImageDetail(UserIsStaffMixin, DetailView):
    model = UserImage
