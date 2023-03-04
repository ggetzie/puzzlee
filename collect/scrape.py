import time

import requests
from django.utils import timezone
from selenium.webdriver import Firefox

from collect.models import ListPage


def fetch_list_pages(institution):
    unvisited = ListPage.objects.filter(
        last_visited__isnull=True, institution=institution
    )
    with Firefox() as driver:
        for list_page in unvisited:
            driver.get(list_page.url)
            list_page.html = driver.page_source
            list_page.last_visited = timezone.now()
            list_page.save()
            time.sleep(2)
