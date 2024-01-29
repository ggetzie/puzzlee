from .models import UserImage

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div
from django import forms
from PIL import Image
import imagehash


class UserImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ("image", "user")
        widgets = {"user": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "makeitart:userimage_upload"
        self.helper.add_layout(
            Layout(
                "image",
                "user",
                Div(
                    Submit("submit", "Submit"),
                    css_class="mb-3 d-flex justify-content-end",
                ),
            )
        )

    def save(self, *args, **kwargs):
        im = Image.open(self.cleaned_data["image"])

        user_image = UserImage(
            image=self.cleaned_data["image"],
            phash=imagehash.phash(im),
            average_hash=imagehash.average_hash(im),
            dhash=imagehash.dhash(im),
            whash=imagehash.whash(im),
            user=self.cleaned_data["user"],
        )
        user_image.save()
        return user_image
