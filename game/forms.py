from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field
from django import forms

from game.models import Artwork, Artist


class CreateArtworkForm(forms.ModelForm):
    artist_fullname = forms.CharField(max_length=150, label="Artist Full Name")
    artist_answer = forms.CharField(
        max_length=150,
        label="Artist Answer",
        help_text="The portion of the artist's name to use as the answer to the puzzle",
    )

    class Meta:
        model = Artwork
        fields = ("title", "year", "image", "description", "added_by")
        widgets = {"added_by": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "game:artwork_create"
        self.helper.form_class = "pz-form"
        self.helper.add_layout(
            Layout(
                "title",
                "artist_fullname",
                "artist_answer",
                Field("year", css_class="number-input"),
                "image",
                "description",
                "added_by",
                Div(
                    Submit("submit", "Submit"),
                    css_class="mb-3 d-flex justify-content-end",
                ),
            )
        )


class CreateArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ("fullname", "answer")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "game:artist_create"
        self.helper.form_class = "pz-form"
        self.helper.add_input(Submit("submit", "Submit"))
