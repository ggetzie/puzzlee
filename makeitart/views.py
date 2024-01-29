from typing import Dict, Any
from .forms import UserImageUploadForm
from .models import UserImage
from core.views import UserIsStaffMixin
from game.models import ArtworkImage
from django.views.generic import CreateView, DetailView
from django.shortcuts import render
from imagehash import hex_to_hash


class UploadUserImage(UserIsStaffMixin, CreateView):
    form_class = UserImageUploadForm
    template_name = "makeitart/userimage_upload.html"

    def get_initial(self) -> Dict[str, Any]:
        res = super().get_initial()
        res["user"] = self.request.user
        return res


class UserImageDetail(UserIsStaffMixin, DetailView):
    model = UserImage

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        ais = ArtworkImage.objects.exclude(
            phash="", average_hash="", dhash="", whash=""
        )
        ui = self.get_object()
        ui_phash = hex_to_hash(ui.phash)
        ui_average_hash = hex_to_hash(ui.average_hash)
        ui_dhash = hex_to_hash(ui.dhash)
        ui_whash = hex_to_hash(ui.whash)
        diffs = [
            (
                hex_to_hash(ai.phash) - ui_phash,
                hex_to_hash(ai.average_hash) - ui_average_hash,
                hex_to_hash(ai.dhash) - ui_dhash,
                hex_to_hash(ai.whash) - ui_whash,
                ai,
            )
            for ai in list(ais)
        ]
        context["closest_phash"] = sorted(diffs, key=lambda x: x[0])[0]
        context["closest_average_hash"] = sorted(diffs, key=lambda x: x[1])[0]
        context["closest_dhash"] = sorted(diffs, key=lambda x: x[2])[0]
        context["closest_whash"] = sorted(diffs, key=lambda x: x[3])[0]
        return context
