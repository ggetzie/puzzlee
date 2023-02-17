from typing import Dict, Any

from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView

from core.views import UserIsStaffMixin
from game.models import Artwork, Artist
from game.forms import CreateArtworkForm, CreateArtistForm


class ArtworkCreate(UserIsStaffMixin, CreateView):
    form_class = CreateArtworkForm
    template_name = "game/artwork_form.html"

    def get_initial(self) -> Dict[str, Any]:
        res = super().get_initial()
        res["added_by"] = self.request.user
        return res


class ArtworkDetail(UserIsStaffMixin, DetailView):
    model = Artwork


class ArtworkList(UserIsStaffMixin, ListView):
    model = Artwork
    paginate_by = 25


class ArtistCreate(UserIsStaffMixin, CreateView):
    form_class = CreateArtistForm
    template_name = "game/artist_form.html"

    def get_initial(self) -> Dict[str, Any]:
        res = super().get_initial()
        res["added_by"] = self.request.user
        return res


class ArtistList(UserIsStaffMixin, ListView):
    model = Artist
    paginate_by = 25


class ArtistDetail(UserIsStaffMixin, DetailView):
    model = Artist
