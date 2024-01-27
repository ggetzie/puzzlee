import csv
from .models import ArtworkImage


def load_hashes(hashes_path):
    with open(hashes_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            artwork_id = int(row["artwork_id"])
            print(f"updating {artwork_id}")
            ArtworkImage.objects.filter(id=artwork_id).update(
                phash=row["phash"],
                average_hash=row["average_hash"],
                dhash=row["dhash"],
                whash=row["whash"],
            )
