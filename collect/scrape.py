import time

import requests
from django.utils import timezone
from selenium.webdriver import Firefox

from collect.models import ListPage, DetailPage


def fetch_list_pages(institution):
    unvisited = ListPage.objects.filter(institution=institution)
    with Firefox() as driver:
        for list_page in unvisited:
            driver.get(list_page.url)
            time.sleep(3)
            list_page.html = driver.page_source
            list_page.last_visited = timezone.now()
            list_page.save()


def fetch_detailpages_met():
    # qs = qs.filter(attribution__regex=r",\D*\d{4}")
    unvisited = DetailPage.objects.filter(
        parent__institution="met",
        attribution__regex=r",\D*\d{4}",
        last_visited__isnull=True,
    )
    with Firefox() as driver:
        for page in unvisited:
            driver.get(page.url)
            time.sleep(2)
            page.html = driver.page_source
            page.last_visited = timezone.now()
            page.save()
