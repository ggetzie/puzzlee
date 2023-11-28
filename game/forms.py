from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div
from django import forms
from django.utils.text import slugify

from game.models import Artwork, Artist


class CreateArtworkForm(forms.ModelForm):
    artist_fullname = forms.CharField(max_length=150, label="Artist Full Name")

    class Meta:
        model = Artwork
        fields = ("title", "year", "description", "added_by")
        widgets = {"added_by": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "game:artwork_create"
        self.helper.form_class = "pz-form"
        self.helper.attrs = {"autocomplete": "off"}
        self.helper.add_layout(
            Layout(
                "title",
                "artist_fullname",
                "artist_answer",
                "year",
                "image",
                "description",
                "added_by",
                Div(
                    Submit("submit", "Submit"),
                    css_class="mb-3 d-flex justify-content-end",
                ),
            )
        )

    def save(self, *args, **kwargs):
        user = self.cleaned_data["added_by"]
        artist, _ = Artist.objects.get_or_create(
            name_slug=slugify(self.cleaned_data["artist_fullname"]),
            defaults={
                "fullname": self.cleaned_data["artist_fullname"],
                "added_by": user,
            },
        )
        artwork = Artwork(
            title=self.cleaned_data["title"],
            artist=artist,
            image=self.cleaned_data["image"],
            year=self.cleaned_data["year"],
            description=self.cleaned_data["description"],
            added_by=user,
        )
        artwork.save()
        return artwork


class CreateArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ("fullname",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "game:artist_create"
        self.helper.form_class = "pz-form"
        self.helper.add_input(Submit("submit", "Submit"))

    def save(self, *args, **kwargs):
        user = self.cleaned_data["added_by"]
        artist = Artist(
            fullname=self.cleaned_data["fullname"],
            added_by=user,
        )
        artist.save()
        return artist
