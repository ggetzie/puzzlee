import pathlib
import subprocess

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from game.models import ArtworkImage


@receiver(post_save, sender=ArtworkImage)
def optimize_image(sender, **kwargs):
    if settings.DEBUG:
        awi = kwargs["instance"]
        input_file = pathlib.Path(awi.image.path)
        output_dir = pathlib.Path(
            str(input_file.parent).replace("/raw/", "/processed/")
        )
        _ = subprocess.run(
            [
                "nnr-photos",
                "--local",
                f"--input={input_file}",
                f"--output={output_dir}",
                "--thumbSize=64",
                "--formats=jpeg",
            ],
            check=False,
        )
