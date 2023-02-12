from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from django import forms

from game.models import Artwork


class CreateArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ("title", "artist", "year", "image", "description", "added_by")
        widgets = {"added_by": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "game:artwork_create"
        self.helper.form_class = "pz-form"
        self.helper.add_input(Submit("submit", "Submit", css_class="float-end"))
