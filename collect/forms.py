from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Submit
from django import forms
from django.utils.text import slugify
from collect.models import DetailPage
from game.models import Artwork, Artist, ArtworkImage


class SetStatusForm(forms.Form):
    detailpage = forms.ModelChoiceField(queryset=DetailPage.objects.all())
    approved = forms.ChoiceField(choices=DetailPage.APPROVED_CHOICES)

    def save(self):
        dp = self.cleaned_data["detailpage"]
        dp.approved = self.cleaned_data["approved"]
        dp.save()


class ApproveForm(forms.Form):
    detailpage = forms.ModelChoiceField(
        queryset=DetailPage.objects.all(), widget=forms.HiddenInput()
    )
    title = forms.CharField(max_length=150)
    artist_fullname = forms.CharField(max_length=150, label="Artist Name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id_approval_form"
        self.helper.layout = Layout(
            Fieldset("", "detailpage", "title", "artist_fullname", "artist_answer"),
            Div(
                Submit(
                    "submit",
                    "Submit",
                    css_id="id_approval_submit",
                ),
                css_class="d-flex flex-row justify-content-end",
            ),
        )

    def save(self, user):
        dp = self.cleaned_data["detailpage"]
        dp.approved = 2
        dp.save()
        artist, _ = Artist.objects.get_or_create(
            name_slug=slugify(self.cleaned_data["artist_fullname"]),
            defaults={
                "fullname": self.cleaned_data["artist_fullname"],
                "added_by": user,
            },
        )
        artwork = Artwork.objects.create(
            title=self.cleaned_data["title"], artist=artist, year=dp.year
        )
        dp.artworkimage.artwork = artwork
        dp.artworkimage.save()
